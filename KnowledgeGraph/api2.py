from bm25_相似度 import *

if __name__ == '__main__':

    while 1:
        question = input('用户:')
        answer,chooses = generate_question(question)
        print('小安:', chooses)
        choose = input('用户:')
        answer = choose_question(answer,choose)
        print('小安:', answer)
