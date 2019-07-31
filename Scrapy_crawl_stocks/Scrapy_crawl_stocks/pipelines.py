# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import jsonlines


class ScrapyCrawlStocksPipeline(object):
    def open_spider(self, spider):
        """ spider开启时调用"""
        self.file = jsonlines.open("stocks_info.jsonl", "w")

    def close_spider(self, spider):
        """ spider关闭时调用"""
        self.file.close()

    def process_item(self, item, spider):
        """ 数据保存方式，返回数据"""
        try:
            jsonlines.Writer.write(self.file, item)
        except:
            pass
        return item
