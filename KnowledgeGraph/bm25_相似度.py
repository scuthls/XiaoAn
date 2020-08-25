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


#   通过bm25的相似度匹配问题
def get_fitness_answer(input_seq):
    input_seq = get_final_input(input_seq)
    question_list, question_answer_direct, qa_dict, answer_list = get_bm_data()

    bm25Model = bm25.BM25(question_list)
    scores = bm25Model.get_scores(input_seq)
    sorted_scores = sorted(scores)

    one = scores.index(sorted_scores[-1])
    two = scores.index(sorted_scores[-2])
    three = scores.index(sorted_scores[-3])

    answer = []
    question = []
    answer.append(get_key(question_answer_direct, question_list[one]))
    answer.append(get_key(question_answer_direct, question_list[two]))
    answer.append(get_key(question_answer_direct, question_list[three]))

    question.append(get_key(qa_dict, answer_list[one]))
    question.append(get_key(qa_dict, answer_list[two]))
    question.append(get_key(qa_dict, answer_list[three]))

    return answer, question


def generate_question(input_seq):
    answer, question = get_fitness_answer(input_seq)
    choose = '问答库中的相似问题\n'
    for i in range(3):
        choose += "{}".format(i+ 1) +'、' + question[i][0]
    choose +=  "4、 以上都不是我要找的"
    return answer,choose



def choose_question(answer,input_choose):
    if int(input_choose) == 4:
        answer = '很抱歉，问答库中没有相似的问题'
        return answer
    elif 0 < int(input_choose) < 4:
        return answer[int(input_choose)-1][0]
    else:
        return "无效输入，请重新提问"


if __name__ == '__main__':
    while 1:
        question = input('用户:')
        answer,chooses = generate_question(question)
        print('小安:', chooses)
        choose = input('用户:')
        answer = choose_question(answer,choose)
        print('小安:', answer)
