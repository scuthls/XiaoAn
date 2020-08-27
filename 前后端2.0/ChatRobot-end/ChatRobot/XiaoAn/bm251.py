import jieba
import re
from gensim.summarization import bm25


#   返回停用词
def get_stopwords_list():
    f = open(r'./data1/stopwords', 'r', encoding='utf-8')
    a = f.readline()
    a = [i.strip() for i in f]
    f.close()
    return a


#   删除标点符号
def punctuation_delete(line):
    string = re.sub(" [+_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）,.?!]", "", line)
    return string


#   删除停用词
def stopwords_delete(line):
    stopwords = {}.fromkeys(get_stopwords_list())
    final_question = []
    for word in line:
        if word not in stopwords:
            final_question.append(word)
    return final_question


#   预处理输入的话，就是把上面三个函数集成
def get_final_input(input_seq):
    input_seq.strip()
    input_seq = punctuation_delete(input_seq)
    input_seq = jieba.cut(input_seq, cut_all=True)
    final_input_seq = stopwords_delete(input_seq)
    return final_input_seq


#   得到问题列表和问答对列表
def get_bm_data():
    question_list = []
    answer_list = []
    question_answer_dict = {}
    qa_dict = {}
    with open('./data1/question.txt', 'r', encoding='utf-8') as question_file:
        with open('./data1/answer.txt', 'r', encoding='utf-8') as answer_file:
            while True:
                question = question_file.readline()
                answer = answer_file.readline()
                if question and answer:
                    question = question.strip()
                    answer = answer.strip()

                    qa_dict[question] = answer
                    final_question = get_final_input(question)

                    question_list.append(final_question)
                    answer_list.append(answer)

                    question_answer_dict[answer] = final_question
                else:
                    break
    question_file.close()
    answer_file.close()
    return question_list, question_answer_dict, qa_dict, answer_list


#   从value索引到key
def get_key(dic, value):
    return [k for k, v in dic.items() if v == value]


question_list, question_answer_direct, qa_dict, answer_list = get_bm_data()


#   通过bm25的相似度匹配问题
def get_fitness_answer(input_seq):
    #     通过bm25的相似度匹配问题
    input_seq = get_final_input(input_seq)

    bm25Model = bm25.BM25(question_list)
    average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())
    scores = bm25Model.get_scores(input_seq,average_idf)

    sorted_scores = list(set(scores))
    sorted_scores.sort()

    answer = []
    question = []

    if sorted_scores[-1] > 0:
        one = scores.index(sorted_scores[-1])
        answer.append(get_key(question_answer_direct, question_list[one]))
        question.append(get_key(qa_dict, answer_list[one]))

        if sorted_scores[-2] > 0:
            two = scores.index(sorted_scores[-2])
            answer.append(get_key(question_answer_direct, question_list[two]))
            question.append(get_key(qa_dict, answer_list[two]))

            if sorted_scores[-3] > 0:
                three = scores.index(sorted_scores[-3])
                answer.append(get_key(question_answer_direct, question_list[three]))
                question.append(get_key(qa_dict, answer_list[three]))

    return answer, question


class QA_chatbot:
    def generate_question(self,input_seq):
        answer, question = get_fitness_answer(input_seq)
        long = len(answer)
        if long > 0:
            chooses = '问答库中的相似问题：'
            for i in range(long):
                chooses += "\n{0}".format(i + 1) + '、' + question[i][0]
            chooses += "\n{0}、以上都不是我要找的".format(long+1)
        else:
            chooses = '抱歉！问答库未为您匹配到相关的问题，问答库将持续更新，敬请期待！'    #代表问答库无相似问题的回答
        return answer, chooses

    def choose_question(self,answer, input_choose):
        long = len(answer)
        if int(input_choose) == long + 1:
            answer = '很抱歉，问答库中没有相似的问题，问答库将持续更新，敬请期待！'
            return answer
        elif 0 < int(input_choose) < long+1:
            return answer[int(input_choose) - 1][0]
        else:
            return "无效输入，请重新提问。"




if __name__ == '__main__':
    handler = QA_chatbot()
    while 1:
        question = input('用户:')
        answer,chooses = handler.generate_question(question)
        print('小安:', chooses)
        choose = input('用户:')
        answer = handler.choose_question(answer,choose)
        print('小安:', answer)
