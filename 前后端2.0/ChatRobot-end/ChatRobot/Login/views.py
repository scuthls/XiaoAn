from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

#登录页面，接收前端JS返回的微信号等数据
class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)#drf接受请求值用data
        return Response({"status":True})

