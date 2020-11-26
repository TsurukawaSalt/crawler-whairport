# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # dep
    flight_number = scrapy.Field()  # 航班号
    stopover_station = scrapy.Field()  # 经停站
    destination = scrapy.Field()  # 目的地
    start_time = scrapy.Field()  # 出发时间
    terminal = scrapy.Field()  # 航站楼
    check_in_counter = scrapy.Field()  # 值机柜台
    boarding_gate = scrapy.Field()  # 登机口
    state = scrapy.Field()  # 状态
    flight_time = scrapy.Field()  # 实际飞行时间

    # arr
    # flight_number = scrapy.Field()  # 航班号
    # stopover_station = scrapy.Field()  # 经停站
    departure = scrapy.Field()  # 起飞地
    end_time = scrapy.Field()  # 到达时间
    # terminal = scrapy.Field()  # 航站楼
    baggage_area = scrapy.Field()  # 行李领取
    arrival_area = scrapy.Field()  # 到达区
    # state = scrapy.Field()  # 状态

    # pass
