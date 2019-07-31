# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# 导入这个包为了移动文件
import shutil

from mzitu.items import DetailItem
import scrapy
# 导入项目设置
from scrapy.utils.project import get_project_settings
# 导入scrapy框架的图片下载类
from scrapy.pipelines.images import ImagesPipeline

import os


class ImagesPipelinse(ImagesPipeline):
    #def process_item(self, item, spider):
    #    return item
    # 获取settings文件里设置的变量值
    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")
    # 重写ImagesPipeline类的此方法
    ''' # 标题  也是设置目录
    title = scrapy.Field()
    # 图片地址
    imge_url = scrapy.Field()
    # 请求头
    Referer = scrapy.Field()
    # 图片名称
    image_Path = scrapy.Field()'''
    # 发送图片下载请求
    def get_media_requests(self, item, info):
        image_url = item["imge_url"]
        # headers是请求头主要是防反爬虫
        headers={'Referer': item['Referer'], 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        yield scrapy.Request(image_url, headers=headers)

    def item_completed(self, result, item, info):
        image_path = [x["path"] for ok, x in result if ok]
        # 定义分类保存的路径
        img_path = "%s/%s" % (self.IMAGES_STORE, item['title'])
        # # 目录不存在则创建目录
        if os.path.exists(img_path) == False:
            os.mkdir(img_path)
        # 将文件从默认下路路径移动到指定路径下
        shutil.move(self.IMAGES_STORE + "/" +image_path[0], img_path + "/" +image_path[0][image_path[0].find("full/")+6:])
        item['image_Path'] = img_path + "/" + image_path[0][image_path[0].find("full/")+6:]
        return item


class MyPipelines(object):
    # 测试
    def process_item(self, item, spider):
        if isinstance(item, DetailItem):
            # 意思是这个管道只处理detailitem，需要设置优先级,值越小越优先
            return item