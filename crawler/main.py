import schedule
import os
import time
import datetime


def crawl_dep():
    cmd = 'scrapy crawl dep_info -o dep_info_' + datetime.datetime.today().strftime('%Y%m%d') + ".json"
    os.system(cmd)


def crawl_arr():
    cmd = 'scrapy crawl arr_info -o arr_info_' + datetime.datetime.today().strftime('%Y%m%d') + ".json"
    os.system(cmd)


'''定时每日 10:00 爬取'''
schedule.every().day.at("10:00").do(crawl_dep)
schedule.every().day.at("10:00").do(crawl_arr)

while True:
    print("Ten seconds later......")
    schedule.run_pending()
    # 等待十秒
    time.sleep(10)
