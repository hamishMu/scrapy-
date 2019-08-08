# -*- coding: utf-8 -*-
"""

"""
import scrapy
from plmm.items import PlmmItem
import os
import requests
import time


class PlmmspiderSpider(scrapy.Spider):  # 需要继承scrapy.Spider类
    name = 'plmmspider'  # 定义蜘蛛名
    allowed_domains = ['www.plmm.com.cn']
    host = 'https://www.plmm.com.cn'
    # start_urls = ['http://plmm.com.cn/']
    start_urls = ['http://www.plmm.com.cn/xinggan/',
                  #'http://www.plmm.com.cn/qingchun/',
                  #'http://www.plmm.com.cn/xiaohua/',
                  #'http://www.plmm.com.cn/chemo/',
                  #'http://www.plmm.com.cn/qipao/',
                  ]

    def parse(self, response):
        url_tag_list = response.xpath('//div[@class="goods-item"]')
        next_url = self.host + response.xpath('//span[@id="npage"]/a/@href').extract_first()
        print(next_url)
        for url_tag in url_tag_list:
            url = url_tag.xpath('span/h3/a/@href').extract_first()
            url = 'http:' + url
            title = url_tag.xpath('span/h3/a/text()').extract_first()
            item = PlmmItem()
            item['url'] = url
            item['title'] = title
            #if next_url is not None:
                #yield response.follow(url=next_url, callback=self.parse)
            yield scrapy.Request(url=str(url), headers=self.settings['HEADERS'],
                                 callback=self.parse_detail,
                                 meta={'item': item})

    def parse_detail(self, response):

        item = response.meta['item']
        text = response.xpath('//body/div[4]/div/div[1]/p/text()').extract_first()
        item['text'] = text
        images = []
        image_tag_list = response.xpath('//article/div/ul/a')
        for image_tag in image_tag_list:
            print("image_name:", image_tag)
            image_src = image_tag.xpath('img/@src').extract_first()
            image_src_list = image_src.split("@")
            image_src = image_src_list[0]
            image_src = "http:" + image_src
            image_name = image_tag.xpath('img/@alt').extract_first()
            images.append({image_name:image_src})
            #item['image_src'] = image_src
            #item['image_name'] = image_name
            image_root_path = r"D:\mizi"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
                            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
            }
            image_path = image_root_path + '\\' + item['title']
            if not os.path.exists(image_path):
                os.makedirs(image_path, exist_ok=True)
            os.chdir(image_path)
            res = requests.get(image_src, headers=headers)
            result = res.content
            with open(image_name + ".jpg", 'wb')as f:
                f.write(result)
            time.sleep(2)
            item['images'] = images
        yield item
        """
    
        # 进行图片的保存
        image_root_path = r"D:\mizi"
        image_path = image_root_path + '\\' + item['title']
        if not os.path.exists(image_path):
            os.makedirs(image_path, exist_ok=True)
        os.chdir(image_path)
        w_image_src = item['image_src']
        w_image_name = item['image_name']
        res = requests.get(w_image_src, headers=self.settings['HEADERS'])
        result = res.content
        with open(w_image_name + ".jpg", 'wb')as f:
            f.write(result)
        time.sleep(2)
        """

