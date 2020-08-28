# -*- coding: utf-8 -*-
#这个代码用来爬取理财产品说明书pdf版，在网站的75-80页
import scrapy
from ..items import PdfItem
import urllib.parse

class DescriptionSpider(scrapy.Spider):
    name = 'des'
    allowed_domains = ['indonesia.icbc.com.cn']
    start_urls = ['http://indonesia.icbc.com.cn/icbc/%e5%85%ac%e5%8f%b8%e4%b8%9a%e5%8a%a1/%e7%90%86%e8%b4%a2%e4%ba%a7%e5%93%81/%e5%80%ba%e5%b8%82%e9%80%9a%e4%ba%a7%e5%93%81%e4%bf%a1%e6%81%af/default.htm']
    for i in range(75,81):
         l = 'http://indonesia.icbc.com.cn/icbc/%e5%85%ac%e5%8f%b8%e4%b8%9a%e5%8a%a1/%e7%90%86%e8%b4%a2%e4%ba%a7%e5%93%81/%e5%80%ba%e5%b8%82%e9%80%9a%e4%ba%a7%e5%93%81%e4%bf%a1%e6%81%af/default-PageList-{}.htm'.format(str(i))
         start_urls.append(l)

    def parse(self, response):
        a=response.css('div.box_normal')
        url_list=a.css(".ChannelSummaryList-insty a::attr(href)").extract()
        for url in url_list:
                url = 'http://indonesia.icbc.com.cn'+url
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse2,dont_filter=True)
    def parse2(self,response):
        for link in response.css('#MyFreeTemplateUserControl a::attr(href)').extract():
            if link.endswith('.pdf'):
                item=PdfItem()
                urls=urllib.parse.urljoin(response.url,link)
                path = link.split('/')[-1]
                item['file_name']=path
                item['file_url']=urls
                yield item

                  

        


