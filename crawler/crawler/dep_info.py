import scrapy


class DepItem(scrapy.Item):
    # define the fields for your item here like:
    # dep
    flight_number = scrapy.Field()  # 航班号
    stopover_station = scrapy.Field()  # 经停站
    destination = scrapy.Field()  # 目的地
    start_time = scrapy.Field()  # 出发时间
    terminal = scrapy.Field()  # 航站楼
    check_in_counter = scrapy.Field()  # 值机柜台
    boarding_gate = scrapy.Field()  # 登机口
    state = scrapy.Field()  # 状态
    flight_time = scrapy.Field()  # 预计飞行时间
