# Define your item pipelines here

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re
from time import clock_getres, clock_gettime
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class EalatihrPipeline:
    def process_item(self, productItem, spider):
        return productItem

class ItemCleaningPipeline:
    def process_item(self, productItem, spider):
        productItem['specsTable'] = [item.strip() for item in productItem['specsTable']]
        key_list = ['key', 'value']
        n = len(productItem['specsTable'])
        productItem['specsTable'] = [{key_list[0]:productItem['specsTable'][i], key_list[1]:productItem['specsTable'][i+1]} for i in range(0, n, 2)]
        productItem['category'] = [category for category in reversed(productItem['category'])]
        productItem['category'] = productItem['category'].pop()
        productItem['oldPrice'] = productItem['oldPrice'] if productItem['oldPrice'] else 'null'
        return productItem

class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('ealatihr_out_2.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, productItem, spider):
        line = json.dumps(ItemAdapter(productItem).asdict()) + "\n"
        self.file.write(line)
        return productItem