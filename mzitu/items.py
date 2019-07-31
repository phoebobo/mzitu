# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MzituItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 标题  也是设置目录
    title = scrapy.Field()
    # 图片地址
    imge_url = scrapy.Field()
    # 请求头
    Referer = scrapy.Field()
    # 图片名称
    image_Path = scrapy.Field()


