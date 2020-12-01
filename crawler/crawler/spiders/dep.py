import scrapy
from crawler.dep_info import DepItem
import datetime


class DepSpider(scrapy.Spider):
    name = 'dep_info'
    allowed_domains = ['www.whairport.com']

    header = 'http://www.whairport.com/jc/ch/dep/depGlList.jhtml?begin_seach=y&_pageSize=10&_pageNo='
    page = '1'
    mid = '&AIRPLANE=&TERM_ID=&DAY_SEL='
    date = ''
    tail = '&FROM_TIME=0000&TO_TIME=2359&AIRPORT=&AIRLINE=&scheduleList=149'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 获取今日日期 设置url
        self.date = datetime.date.today().strftime('%Y%m%d')
        # print(self.date)

    def start_requests(self):
        # 拼接url
        target_url = self.header + self.page + self.mid + self.date + self.tail
        yield scrapy.Request(target_url, callback=self.parse)

    def parse(self, response):
        basic_info_list = response.xpath("//div[@class='flight-info-basic-link']")
        detail_info_list = response.xpath("//div[@class='tr-like flight-info-detail']")

        for basic_info, detail_info in zip(basic_info_list, detail_info_list):
            item = DepItem()
            # 基本信息
            flight_number = basic_info.xpath(".//strong[@id='column3-1']/text()").extract()
            stopover_station = basic_info.xpath(".//span[@id='column2-0']/text()").extract()
            destination = basic_info.xpath(".//span[@id='column2-1']/text()").extract()
            start_time = basic_info.xpath(".//strong[@id='column1-1']/text()").extract()
            terminal = basic_info.xpath(".//strong[@id='column5-1']/text()").extract()
            check_in_counter = basic_info.xpath(".//div[@id='column6-1']/strong/text()").extract()
            boarding_gate = basic_info.xpath(".//strong[@id='column7-1']/text()").extract()
            state = basic_info.xpath(".//span[@id='column8-1']/text()").extract()
            # 存在为空的信息
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
        next_page = int(current_page) + 1
        # 查看 最后一页 的javaScript
        end_sign = response.xpath(".//a[@class='ico next']/@href").extract_first()
        if end_sign != "javascript:void(0);":
            # 表示并非最后一页
            next_url = self.header + str(next_page) + self.mid + self.date + self.tail
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            # 最后一页
            print("total " + current_page + ' pages.')
