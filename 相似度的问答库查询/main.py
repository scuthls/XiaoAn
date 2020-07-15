from sim_seq import *

if __name__ == '__main__':
    sim = Word2vecSim()
    while 1:
        question = input('用户:')
        final_answer = sim.sim_main(question)
        print('小安', final_answer)
        print('可以解决你的问题吗？')
        x = input("请输入1表示可以，2表示不可以：")
        if x == '1':
            print("感谢您的提问")
        elif x == '2':
            print("很抱歉知识库中的知识不能回答您的问题")
        print("可以提出下一个问题")
