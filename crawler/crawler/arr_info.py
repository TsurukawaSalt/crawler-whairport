import scrapy


class ArrItem(scrapy.Item):
    # define the fields for your item here like:
    # arr
    flight_number = scrapy.Field()  # 航班号
    stopover_station = scrapy.Field()  # 经停站
    departure = scrapy.Field()  # 起飞地
    end_time = scrapy.Field()  # 到达时间
    terminal = scrapy.Field()  # 航站楼
    baggage_area = scrapy.Field()  # 行李领取
    arrival_area = scrapy.Field()  # 到达区
    state = scrapy.Field()  # 状态
    flight_time = scrapy.Field()  # 实际飞行时间

