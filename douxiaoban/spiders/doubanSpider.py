# -*- coding: utf-8 -*-
import scrapy
from douxiaoban.items import DouxiaobanItem


class DoubanspiderSpider(scrapy.Spider):
    name = 'doubanSpider'  # 爬虫名  别和项目名称搞混了
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250/']  # 入口URL

    def parse(self, response):  # 解析
        # print(response.text)
        movieList = response.xpath(
            '//div[@class="article"]//ol[@class="grid_view"]/li')
        for itemList in movieList:
            doubanItem = DouxiaobanItem()

            doubanItem['serialNumber'] = itemList.xpath(
                ".//div[@class='pic']/em/text()").extract_first()

            doubanItem['movieName'] = itemList.xpath(
                ".//div[@class='hd']/a/span[1]/text()").extract_first()

            content = itemList.xpath(".//div[@class='info']//p[1]/text()").extract()
            # 这里的内容是<p>中间用<br>打断了,现在用循环处理一下
            for iContent in content:
                doubanItem['introduce'] = "".join(iContent.split())
                # print(doubanItem)

            doubanItem['start'] = itemList.xpath(
                ".//div[@class='bd']/div[@class='star']/span[2]/text()").extract_first()

            doubanItem['evaluate'] = itemList.xpath(
                "//div[@class='bd']/div[@class='star']/span[4]/text()").extract_first()

            doubanItem['describtion'] = itemList.xpath(
                "//div[@class='bd']/p[@class='quote']/span/text()").extract_first()
            yield doubanItem #扔到 pipeline 去
        nextLink = response.xpath("//span[@class='next']/link/@href").extract()
        if nextLink:
            nextLink = nextLink[0] 
            yield scrapy.Request("https://movie.douban.com/top250"+nextLink,callback = self.parse)
            