# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename,dirname,join
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class PdfPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item['file_url'],meta={'title':item['file_name']})
    def file_path(self,request,response=None,info=None):
        p_url=urlparse(request.url).path
        p_name=request.meta.get('title')
        return join(basename(dirname(p_url)),basename(p_name))
