import scrapy
from crawler.arr_info import ArrItem
import datetime


class ArrSpider(scrapy.Spider):
    name = 'arr_info'
    allowed_domains = ['www.whairport.com']

    header = 'http://www.whairport.com/jc/ch/arr/arrGlList.jhtml?begin_seach=y&_pageSize=10&_pageNo='
    page = '1'
    mid = '&AIRPLANE=&TERM_ID=&DAY_SEL='
    date = ''
    tail = '&FROM_TIME=0000&TO_TIME=2359&AIRPORT=&AIRLINE='

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
            item = ArrItem()
            # 基本信息
            flight_number = basic_info.xpath(".//strong[@id='column3-0']/text()").extract()
            stopover_station = basic_info.xpath(".//span[@id='column2-0']/text()").extract()
            departure = basic_info.xpath(".//span[@id='column2-0']/text()").extract()
            end_time = basic_info.xpath(".//strong[@id='column1-1']/text()").extract()
            terminal = basic_info.xpath(".//strong[@id='column5-0']/text()").extract()
            baggage_area = basic_info.xpath(".//strong[@id='column7-0']/text()").extract()
            arrival_area = basic_info.xpath(".//strong[@id='column8-0']/text()").extract()
            state = basic_info.xpath(".//span[@id='column9-0']/text()").extract()
            # 存在为空的信息
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
                item['baggage_area'] = baggage_area[0]
            if len(arrival_area) == 0:
                item['arrival_area'] = '暂无'
            else:
                item['arrival_area'] = arrival_area[0]
            item['state'] = state[0].replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')

            # 详细信息：实际飞行时间
            flight_time = detail_info.xpath(".//span[@class='fm-heading-time']/text()").extract()
            # 只有第一个才是 实际飞行时间
            item['flight_time'] = flight_time[1].replace('\n', '').replace('\r', '').replace(' ', '').replace('\t', '')

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
