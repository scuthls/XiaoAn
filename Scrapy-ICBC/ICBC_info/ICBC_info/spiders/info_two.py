# -*- coding: utf-8 -*-
#这个代码用来爬取工商银行官网的理财资讯
import scrapy


class InfoTwoSpider(scrapy.Spider):
    name = 'info_two'
    allowed_domains = ['www.icbc.com.cn/']
    start_urls = ['http://www.icbc.com.cn/ICBC/%e7%bd%91%e4%b8%8a%e7%90%86%e8%b4%a2/%e7%90%86%e8%b4%a2%e8%b5%84%e8%ae%af/%e4%b8%93%e5%ae%b6%e8%bf%b0%e8%af%84/',
    'http://www.icbc.com.cn/icbc/%e7%bd%91%e4%b8%8a%e7%90%86%e8%b4%a2/%e7%90%86%e8%b4%a2%e8%b5%84%e8%ae%af/%e5%ae%b6%e5%ba%ad%e9%92%b1%e7%bb%8f/default.htm',
    'http://www.icbc.com.cn/icbc/%e7%bd%91%e4%b8%8a%e7%90%86%e8%b4%a2/%e7%90%86%e8%b4%a2%e8%b5%84%e8%ae%af/%e5%ae%b6%e5%ba%ad%e9%92%b1%e7%bb%8f/default-PageList-2.htm',
    'http://www.icbc.com.cn/icbc/%e7%bd%91%e4%b8%8a%e7%90%86%e8%b4%a2/%e7%90%86%e8%b4%a2%e8%b5%84%e8%ae%af/%e5%ae%b6%e5%ba%ad%e9%92%b1%e7%bb%8f/default-PageList-1.htm']

    def parse(self, response):
        a=response.css('div.yy')
        url_list=a.css(".ChannelSummaryList-insty a::attr(href)").extract()
        for url in url_list:
                url = 'http://www.icbc.com.cn'+url
                yield scrapy.Request(url=url, callback=self.parse2,dont_filter=True)
    def parse2(self,response):
        content=response.css('#MyFreeTemplateUserControl *::text').extract()
        title=response.css('#NCPHRICH_TitleHtmlPlaceholderDefinition::text').extract()
        filename=title[0]
        with open(filename,"a+") as f:
            for i in content:
                f.write(i)      
            f.close()