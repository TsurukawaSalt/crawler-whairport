import schedule
import os
import time
import datetime

# 定时爬取


def crawl_dep():
    cmd = 'scrapy crawl dep_info -o dep_info_' + datetime.datetime.today().strftime('%Y%m%d') + ".json"
    os.system(cmd)


def crawl_arr():
    cmd = 'scrapy crawl arr_info -o arr_info_' + datetime.datetime.today().strftime('%Y%m%d') + ".json"
    os.system(cmd)


schedule.every().day.at("10:00").do(crawl_dep)
schedule.every().day.at("10:00").do(crawl_arr)

while True:
    print("heart beat")
    schedule.run_pending()
    time.sleep(10)
