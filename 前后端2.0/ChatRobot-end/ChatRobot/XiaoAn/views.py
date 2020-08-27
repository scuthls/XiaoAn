from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from XiaoAn import question_classifier
from XiaoAn import question_parser
from XiaoAn import answer_search  #导入自写库
from XiaoAn import api1
from XiaoAn import bm251
from XiaoAn import KDaily
import requests
import json
# api1
handler = api1.ChatBotGraph()

# class TestView(APIView):
#     def post(self,request,*args,**kwargs):
#         data = request.data
#         print(data)
#         question = data['que']
#         status = data['status']
#         answers = handler.chat_main(question)
#         print(answers) 
#         #修改格式
#         return Response({"text":answers})
# api2

handler_two = bm251.QA_chatbot()
# class TestView(APIView):
#     def post(self,request,*args,**kwargs):
#         data = request.data
#         print(data)
#         question = data['que']
#         answer,chooses = handler_two.generate_question(question)
#         return Response({"text":chooses,"answer":answer})#在聊天界面展示的问题

#api3

# class TestView(APIView):
#     def post(self,request,*args,**kwargs):
#         api = "6b2db33d931048ccb876a491f334c4f6"
#         url = 'http://www.tuling123.com/openapi/api?key=' + api + '&info='
#         data = request.data
#         print(data)
#         info = data['que']
#         page = requests.get(url + info)
#         json_dic = json.loads(page.text)
#         answer = json_dic['text']
#         print('小安: ',answer)
#         return Response({"text":answer})

# api4 
# class TestView(APIView):
#     def post(self,request,*args,**kwargs):
#         data = request.data
#         print(data)
#         info = data['que']
#         ts_code = info    #例如输入000001.SZ,请在股票代码后加上交易所缩写如000001.SZ、600000.SH（仅支持这两个交易所的股票查询）：
#         #画年K线图
#         url1 = KDaily.K(ts_code,0)  #0代表画年K线图
#         #画月K线图
#         url2 = KDaily.K(ts_code,1)    #1代表画月K线图
#         #画周K线图
#         url3 = KDaily.K(ts_code,2)   #1代表画月K线图
#         urls = [url1,url2,url3]
#         print(urls)
#         return Response({"text":urls})

class TestView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        print(data)
        question = data['que']
        status = data['status']

        if status == 1:
            answers = handler.chat_main(question)
            print("调用了1")
            print(answers)
            if answers == "这个问题知识库中暂时没有，知识库将持续更新，敬请期待！":
                status = 2
            else:
                return Response({"text": answers, "status": status})
        if status == 2:
            answer, chooses = handler_two.generate_question(question)
            print("调用了2")
            if chooses == "抱歉！问答库未为您匹配到相关的问题，问答库将持续更新，敬请期待！":
                status = 3
            else:
                return Response({"text": chooses, "answer": answer, "status": status})  # 在聊天界面展示的问题
        if status == 3:
            print("调用了3")
            api = "6b2db33d931048ccb876a491f334c4f6"
            url = 'http://www.tuling123.com/openapi/api?key=' + api + '&info='
            page = requests.get(url + question)
            json_dic = json.loads(page.text)
            answer = json_dic['text']
            print('小安: ', answer)
            return Response({"text": answer, "status": status})
        # if status == 4:
        #     ts_code = question    #例如输入000001.SZ,请在股票代码后加上交易所缩写如000001.SZ、600000.SH（仅支持这两个交易所的股票查询）：
        # #画年K线图
        #     url1 = KDaily.K(ts_code,0)  #0代表画年K线图
        # #画月K线图
        #     url2 = KDaily.K(ts_code,1)    #1代表画月K线图
        # #画周K线图
        #     url3 = KDaily.K(ts_code,2)   #1代表画月K线图
        #     urls = [url1,url2,url3]
        #     print(urls)
        #     return Response({"text":urls})
                

