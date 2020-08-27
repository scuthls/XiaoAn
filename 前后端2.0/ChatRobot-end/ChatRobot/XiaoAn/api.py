from bm25_相似度 import *
from api1 import *

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer1 = handler.chat_main(question)
        answer2 = choose_question(question)
        if answer1 =="这个问题知识库中暂时没有，知识库将持续更新，敬请期待！":
            choose = input('用户:')
            answer3 = choose_question(answer, choose)
            print('小安:', answer3)
        else:
            print('小安:', answer1)
        print("可以提出下一个问题")