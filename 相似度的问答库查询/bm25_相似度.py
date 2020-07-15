import jieba
import re
from gensim.summarization import bm25


#   返回停用词
def get_stopwords_list():
    f = open(r'./stopwords', 'r', encoding='utf-8')
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
    question_answer_dict = {}
    with open('./data/question.txt', 'r', encoding='utf-8') as question_file:
        with open('./data/answer.txt', 'r', encoding='utf-8') as answer_file:
            while True:
                question = question_file.readline()
                answer = answer_file.readline()
                if question and answer:
                    question = question.strip()
                    answer = answer.strip()
                    final_question = get_final_input(question)
                    question_list.append(final_question)
                    question_answer_dict[answer] = final_question
                else:
                    break
    question_file.close()
    answer_file.close()
    return question_list, question_answer_dict


#   从value索引到key
def get_key(dic, value):
    return [k for k, v in dic.items() if v == value]


#   通过bm25的相似度匹配问题
def get_fitness_answer(input_seq):
    input_seq = get_final_input(input_seq)
    question_list, question_answer_direct = get_bm_data()

    bm25Model = bm25.BM25(question_list)
    scores = bm25Model.get_scores(input_seq)
    max_score = max(scores)
    idx = scores.index(max(scores))

    answer = get_key(question_answer_direct, question_list[idx])
    answer = str(answer[0])
    return max_score, answer
