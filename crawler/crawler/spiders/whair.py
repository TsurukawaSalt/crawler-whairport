import scrapy
from crawler.items import CrawlerItem

class WhairSpider(scrapy.Spider):
    name = 'whair'
    allowed_domains = ['www.whairport.com']
    # start_urls = ['http://www.whairport.com/']
    header = 'http://www.whairport.com/jc/ch/dep/depGlList.jhtml?begin_seach=y&_pageSize=10&_pageNo='
    page = '1'
    other = '&AIRPLANE=&TERM_ID=&DAY_SEL='
    year = '2020'
    month = '11'
    day = '25'
    from_time = '0000'
    to_time = '2359'
    tail = '&AIRPORT=&AIRLINE=&scheduleList=149'
    kind = 'dep'

    def __init__(self, kind='dep', date='26', fromtime='00', totime='24', *args, **kwargs):
        super(WhairSpider, self).__init__(*args, **kwargs)
        # 只能往前查看5天，如11.26日能查看的最早的时间为11.21
        if int(totime) <= int(fromtime):
            self.day = date
            self.from_time = fromtime
            self.to_time = str(int(fromtime) + 1)
            print('time error! reset totime to (fromtime+1)')
        else:
            self.day = date
            self.from_time = fromtime
            self.to_time = totime
        print(self.from_time)
        print(self.to_time)
        if kind == 'arr':
            self.kind = 'arr'
            self.header = 'http://www.whairport.com/jc/ch/arr/arrGlList.jhtml?begin_seach=y&_pageSize=10&_pageNo='
            self.tail = '&AIRPORT=&AIRLINE='

    def start_requests(self):
        target_url = self.header + self.page + self.other + self.year + self.month + self.day + '&FROM_TIME=' + self.from_time + '&TO_TIME' + self.to_time + self.tail
        if self.kind == 'dep':
            yield scrapy.Request(target_url, callback=self.dep_parse)
        else:
            yield scrapy.Request(target_url, callback=self.arr_parse)

    def dep_parse(self, response):
        basic_info_list = response.xpath("//div[@class='flight-info-basic-link']")
        detail_info_list = response.xpath("//div[@class='tr-like flight-info-detail']")
        # items=[]

        for basic_info, detail_info in zip(basic_info_list, detail_info_list):
            item = CrawlerItem()
            # 基本信息
            flight_number = basic_info.xpath(".//strong[@id='column3-1']/text()").extract()
            stopover_station = basic_info.xpath(".//span[@id='column2-0']/text()").extract()
            destination = basic_info.xpath(".//span[@id='column2-1']/text()").extract()
            start_time = basic_info.xpath(".//strong[@id='column1-1']/text()").extract()
            terminal = basic_info.xpath(".//strong[@id='column5-1']/text()").extract()
            check_in_counter = basic_info.xpath(".//div[@id='column6-1']/strong/text()").extract()
            boarding_gate = basic_info.xpath(".//strong[@id='column7-1']/text()").extract()
            state = basic_info.xpath(".//span[@id='column8-1']/text()").extract()
            # 赋值
            item['flight_number'] = flight_number[0]
            if stopover_station[0] == '\xa0':
                item['stopover_station'] = '无'
            else:
                item['stopover_station'] = stopover_station[0].replace('\xa0', '')
            if len(destination) == 0:
                item['destination'] = '无'
            else:
                item['destination'] = destination[0]
            if len(start_time) == 0:
                item['start_time'] = '无'
            else:
                item['start_time'] = start_time[0].replace(' ', '')
            if len(terminal) == 0:
                item['terminal'] = '无'
            else:
                item['terminal'] = terminal[0]
            if len(check_in_counter) == 0:
                item['check_in_counter'] = '暂无'
            else:
                item['check_in_counter'] = check_in_counter[0]  # 可能没有（航班取消 or 计划）
            if len(boarding_gate) == 0:
                item['boarding_gate'] = '暂无'
            else:
                item['boarding_gate'] = boarding_gate[0]  # 可能没有（航班取消 or 计划）
            if len(state) == 0:
                item['state'] = '无'
            else:
                item['state'] = state[0].replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')

            # 详细信息
            flight_time = detail_info.xpath(".//div[@class='fm-info-content']//span[@class='fm-heading-time']/text()").extract()
            item['flight_time'] = flight_time[0].replace(" ", '')

            # 保存
            yield item

        page_node = response.xpath(".//li[contains(@class,'pagenation-list-item on')]")
        current_page = page_node[0].xpath("./a/text()").extract_first()
        print("current page: " + current_page)
        next_page = int(current_page) + 1
        # 查看 最后一页 的javaScript
        end_sign = response.xpath(".//a[@class='ico next']/@href").extract_first()
        print(end_sign)
        if end_sign != "javascript:void(0);":
            next_url = self.header + str(next_page) + self.other + self.year + self.month + self.day + '&FROM_TIME=' + self.from_time + '&TO_TIME' + self.to_time + self.tail
            yield scrapy.Request(next_url, callback=self.dep_parse)

    def arr_parse(self, response):
        basic_info_list = response.xpath("//div[@class='flight-info-basic-link']")

        for basic_info in basic_info_list:
            item = CrawlerItem()
            # 基本信息
            flight_number = basic_info.xpath(".//strong[@id='column3-0']/text()").extract()
            stopover_station = basic_info.xpath(".//span[@id='column2-0']/text()").extract()
            departure = basic_info.xpath(".//span[@id='column2-0']/text()").extract()
            end_time = basic_info.xpath(".//strong[@id='column1-1']/text()").extract()
            terminal = basic_info.xpath(".//strong[@id='column5-0']/text()").extract()
            baggage_area = basic_info.xpath(".//strong[@id='column7-0']/text()").extract()
            arrival_area = basic_info.xpath(".//strong[@id='column8-0']/text()").extract()
            state = basic_info.xpath(".//span[@id='column9-0']/text()").extract()

            # 赋值
            item['flight_number'] = flight_number[0]
            if stopover_station[0] == '\xa0':
                item['stopover_station'] = '无'
            else:
                item['stopover_station'] = stopover_station[0].replace('\xa0', '')
            item['departure'] = departure[1]
            item['end_time'] = end_time[0].replace(' ', '')
            item['terminal'] = terminal[0].replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')
            if len(baggage_area) == 0:
                item['baggage_area'] = '暂无'
            else:
                item['baggage_area'] = baggage_area[0]  # 可能没有（航班取消 or 计划）
            if len(arrival_area) == 0:
                item['arrival_area'] = '暂无'
            else:
                item['arrival_area'] = arrival_area[0]  # 可能没有（航班取消 or 计划）
            item['state'] = state[0].replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')

            # 保存
            yield item

        page_node = response.xpath(".//li[contains(@class,'pagenation-list-item on')]")
        current_page = page_node[0].xpath("./a/text()").extract_first()
        print("current page: " + current_page)
        next_page = int(current_page) + 1

        end_sign = response.xpath(".//a[@class='ico next']/@href").extract_first()
        print(end_sign)
        if end_sign != "javascript:void(0);":
            next_url = self.header + str(next_page) + self.other + self.year + self.month + self.day + '&FROM_TIME=' + self.from_time + '&TO_TIME' + self.to_time + self.tail
            yield scrapy.Request(next_url, callback=self.arr_parse)
