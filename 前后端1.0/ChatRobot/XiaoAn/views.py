from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product


class TestView(APIView):
    def post(self,request,*args,**kwargs):
        data = request.data
        print(data)
        pr = Product.objects.get(product_name=data['que'])
        return Response({"text": pr.product_time})
        # if request.data==Product.product_name:
        #     data = request.data
        #     pr = Product.objects.get(product_name=data)
        #     return Response({"text": pr.product_time})
        # else:
        #     return Response({"text":"数据库中没有匹配的value"})
