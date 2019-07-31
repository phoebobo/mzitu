# -*- coding: utf-8 -*-
import scrapy

from mzitu.items import MzituItem

class MeizituSpider(scrapy.Spider):
    name = 'meizitu'  # 项目名，启动时候用的
    allowed_domains = ['mzitu.com']

    # 列表页，也就是起始网址  这里设置的是1到153页
    start_urls = ['http://www.mzitu.com/xinggan/page/{}/'.format(str(x)) for x in range(1, 153)]

    def parse(self, response):
        li_list = response.xpath("//ul[@id='pins']/li")
        print('#######################')
        print(response.request.url)

        for obj in li_list:
            # 获取详情链接
            det_url = obj.xpath("./a/@href").extract_first()
            # 遍历访问详情页
            yield scrapy.Request(url=det_url, callback=self.second_handler)


    def second_handler(self, response):
        # 二级页面
        item = MzituItem()
        # 获取页数链接进行访问
        offset = int(response.xpath('//div[@class="pagenavi"]/a/span/text()')[4].extract())
        # 生成链接访问 遍历链接访问
        for i in [response.url + "/{}".format(str(x)) for x in range(1, offset + 1)]:
            item['Referer'] = i
            # 将meta传入链接  访问三级页面
            yield scrapy.Request(url=i, meta={'meta_1': item}, callback=self.parse_ponse)


    def parse_ponse(self, response):
        # 获取itme资源
        item = response.meta['meta_1']
        # 获取图片地址
        item["imge_url"] = response.xpath('//div[@class="main-image"]/p/a/img/@src')[0].extract()
        # 获取图片目录
        item["title"] = response.xpath('//div[@class="main-image"]/p/a/img/@alt')[0].extract()
        # 抛出
        yield item
