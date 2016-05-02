# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy
#from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from timecoverspider import settings
import requests

class MyImagesPipeline(object):

    def process_item(self, item, spider):
        
        print "begin pipeline process"

        if 'file_urls' in item:
            print "get file urls"
            images = []

            dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            for url in item['file_urls']:
                image_file_name = item['title'].replace(' ', '_')
                file_path = '%s/%s' % (dir_path, image_file_name)
                images.append(file_path)

                with open(file_path, 'wb') as hd:
                    response = requests.get(url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break

    # def get_media_requests(self, item, info):
    #     for image_url in item['file_urls']:
    #         yield Request(image_url)

    # def item_completed(self, results, item, info):
    #     image_paths = [ x['path'] for ok, x in results if ok]

    #     if not image_paths:
    #         raise DropItem("item contains no images")

    #     new_path = "/Users/Patrick/Git/time-magazine-scrape/tmp.jpg"
    #     os.rename(new_path)
    #     return item

    # def file_path(self, request, response=None, info=None):
    #     item = request.meta['item']
    #     title = item['title'].replace(' ', '_')
    #     file_name = u'full/test/' + title
    #     return file_name
    # def process_item(self, item, spider):
    #     return item
