# from django.db import models

# #用于记录资讯所属的银行
# class Bank(models.Model):
#     name=models.CharField(max_length=50)
#     def __str__(self):
#         return self.name
# #资讯详细信息
# class Info(models.Model):
#     #标题
#     title=models.CharField(max_length=50)
#     #所属银行
#     belong_bank=models.ForeignKey(Bank,on_delete=models.DO_NOTHING)
#     #内容
#     content=models.TextField()
#     #发布日期
#     # date_time=models.DateTimeField()
#     cate_time=models.CharField(max_length=50)
#     def __str__(self):
#         return self.title