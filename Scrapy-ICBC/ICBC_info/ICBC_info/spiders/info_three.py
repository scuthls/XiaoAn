# -*- coding: utf-8 -*-
#这个代码用来爬取金投网上工商银行的理财资讯_最新版+日期
import scrapy
class InfoThreeSpider(scrapy.Spider):
    name = 'info_three'
    allowed_domains = ['bank.cngold.org']
    start_urls = ['https://bank.cngold.org/gsc/index.html']
    for i in range(2,12):
         l = 'https://bank.cngold.org/gsc/list_446_{}.html'.format(str(i))
         start_urls.append(l)

    def parse(self, response):
        a=response.css('div.lWrapCon')
        url_list=a.css("a::attr(href)").extract()
        url_date=a.css(".fr::text").extract()
        for i in range(len(url_list)):
            yield scrapy.Request(url=url_list[i], meta={'key':url_date[i]},callback=self.parse2,dont_filter=True)
        

        ## 是否还有下一页，如果有的话，则继续
        # next_pages = response.xpath('//div[@align="right"]//@href').extract()

        # if next_pages:
        #     next_page = 'http://www.icbc.com.cn'+next_pages[0]
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
    def parse2(self,response):
        date=response.meta['key']
        content=response.css('.article_con *::text').extract()
        title=response.css('.heading1 h1::text').extract_first()
        filename="标题：%s-日期：%s"%(title,date)
        if filename is None:
            filename=response.css('.heading1').extract()[0]
        with open(filename,"a+",encoding="utf-8") as f:
            for i in content:
                i.replace(u'\xa0', u'')
                f.write(i)      
            f.close()
        next_page = response.css('.listPage a::attr(href)').extract_first()

        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse2)