# -*- coding: utf-8 -*-
import scrapy


class DaimaSpider(scrapy.Spider):
    name = 'daima'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        pass
