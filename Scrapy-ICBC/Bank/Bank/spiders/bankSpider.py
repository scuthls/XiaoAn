from scrapy.spiders import Spider
import scrapy
from Bank.items import BankItem

class bankSpider(Spider):
    name = 'bank'
    start_urls = ['https://www.rong360.com/licai-bank/list/p1']

    def parse(self, response):

        item = BankItem()
        trs = response.css('tr')[1:]

        for tr in trs:
            item['name'] = tr.xpath('td[1]/a/text()').extract_first()
            item['bank'] = tr.xpath('td[2]/p/text()').extract_first()
            item['currency'] = tr.xpath('td[3]/text()').extract_first()
            item['startDate'] = tr.xpath('td[4]/text()').extract_first()
            item['endDate'] = tr.xpath('td[5]/text()').extract_first()
            item['period'] = tr.xpath('td[6]/text()').extract_first()
            item['proType'] = tr.xpath('td[7]/text()').extract_first()
            item['profit'] = tr.xpath('td[8]/text()').extract_first()
            item['amount'] = tr.xpath('td[9]/text()').extract_first()

            yield item

        next_pages = response.css('a.next-page')

        if len(next_pages) == 1:
            next_page_link = next_pages.xpath('@href').extract_first() 
        else:
            next_page_link = next_pages[1].xpath('@href').extract_first()

        if next_page_link:
            next_page = "https://www.rong360.com" + next_page_link
            yield scrapy.Request(next_page, callback=self.parse)