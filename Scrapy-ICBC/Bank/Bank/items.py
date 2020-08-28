# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BankItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    bank = scrapy.Field()
    currency = scrapy.Field()
    startDate = scrapy.Field()
    endDate = scrapy.Field()
    period = scrapy.Field()
    proType = scrapy.Field()
    profit = scrapy.Field()
    amount = scrapy.Field()