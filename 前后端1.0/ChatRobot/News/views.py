# from django.shortcuts import render_to_response,get_object_or_404
# from .models import Bank,Info
# from django.conf import settings
# from django.core.paginator import Paginator

# 此方法为分页器方法
# def get_news_list(news_all_list,request):
#     paginator=Paginator(news_all_list,settings.EACH_PAGE_NEWS_NUM)
#     page_num=request.GET.get('page',1)#获取url的页面参数(GET请求)
#     page_of_news = paginator.get_page(page_num)
#     current_page = page_of_news.number #获取当前页码
#     page_range = list(range(max(1,current_page-2),current_page))+ \
#         list(range(current_page,min(current_page+2,page_of_news.paginator.num_pages)+1))

#     #加上省略页码标记
#     if page_range[0]-1 >=2:
#         page_range.insert(0,'...')
#     if page_of_news.paginator.num_pages-page_range[-1] >=2:
#         page_range.append('...')
#     #加上首页和尾页
#     if page_range[0] != 1:
#         page_range.insert(0,1)
#     if page_range[-1] != page_of_news.paginator.num_pages:
#         page_range.append(page_of_news.paginator.num_pages)
#     context={}
#     context['news']=page_of_news.object_list
#     context['page_of_news'] = page_of_news
#     #在context里面加入键值对，news为键，值为数组类型，存放所有的news
#     context['bank']=Bank.objects.all()
#     context['page_range']=page_range
#     context['time']=Info.objects.dates('time','day',order="DESC")
#     return context
#新闻列表，自动根据日期获取前十条新闻，拉取页面会接着显示前十条
# def news_list(request):
#     news_all_list=Info.objects.all()
#     context = get_news_list(news_all_list,request)  
#     return render_to_response('news_list.html',context)
# #新闻详情
# def news_detail(request,info_pk):
#     context={}
#     info=get_object_or_404(Info,pk=info_pk)#pk是主键
#     context['info']=info
#     response=render_to_response('news_detail.html',context)
#     return response