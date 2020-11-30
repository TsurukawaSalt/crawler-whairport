# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import codecs
import json
import datetime
from crawler.dep_info import DepItem
from crawler.arr_info import ArrItem


class CrawlerPipeline:
    # def __init__(self):
    #     self.json_file = codecs.open(datetime.datetime.now().strftime('%Y-%m-%d') + '.json', 'w+', encoding='UTF-8')
    #
    # def open_spider(self, spider):
    #     self.json_file.write('[\n')
    #
    # def process_item(self, item, spider):
    #     item_json = json.dumps(dict(item), ensure_ascii=False)
    #     self.json_file.write('\t' + item_json + ',\n')
    #     return item
    #
    # def close_spider(self, spider):
    #     self.json_file.seek(-2, os.SEEK_END)
    #     self.json_file.truncate()
    #     self.json_file.write('\n]')
    #     self.json_file.close()
    def process_item(self, item, spider):
        return item
