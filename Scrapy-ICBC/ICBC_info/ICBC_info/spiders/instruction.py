# -*- coding: utf-8 -*-
import scrapy


class InstructionSpider(scrapy.Spider):
    name = 'instruct'
    allowed_domains = ['http://indonesia.icbc.com.cn/icbc/%e5%85%ac%e5%8f%b8%e4%b8%9a%e5%8a%a1/%e7%90%86%e8%b4%a2%e4%ba%a7%e5%93%81/%e5%80%ba%e5%b8%82%e9%80%9a%e4%ba%a7%e5%93%81%e4%bf%a1%e6%81%af/default-PageList-75.htm']
    start_urls = []
    for i in range(1,76):
         l = 'http://indonesia.icbc.com.cn/icbc/%e5%85%ac%e5%8f%b8%e4%b8%9a%e5%8a%a1/%e7%90%86%e8%b4%a2%e4%ba%a7%e5%93%81/%e5%80%ba%e5%b8%82%e9%80%9a%e4%ba%a7%e5%93%81%e4%bf%a1%e6%81%af/default-PageList-{}.htm'.format(str(i))
         start_urls.append(l)

    def parse(self, response):
        a=response.css('div.box_normal')
        url_list=a.css(".ChannelSummaryList-insty a::attr(href)").extract()
        for url in url_list:
                url = 'http://indonesia.icbc.com.cn'+url
                yield scrapy.Request(url=response.urljoin(url), callback=self.parse2,dont_filter=True)
    def parse2(self,response):
        b=response.css('#MyFreeTemplateUserControl')
        content=b.xpath('//p/text()').extract()
        title=response.css('#NCPHRICH_TitleHtmlPlaceholderDefinition::text').extract_first()
        filename=title
        with open(filename,"a+",encoding="utf-8") as f:
            for i in content:
                i.replace(u'\xa0', u'')
                f.write(i)      
            f.close()

