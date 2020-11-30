# :spider: crawler-whairport

This is my first web-crawler program, used to crawl the data from 'http://www.whairport.com/'.



## :book: Usage

#### :clock10: 定时爬取

**命令**

在`main.py`中设置了定时任务，于每日`10:00`定时爬取数据。

```shell
cd ./crawler
python main.py
```

**输出**

生成两份文件：

1. `dep_info_[yyyymmdd]`：武汉天河国际机场国内机场出发时间表

2. `arr_info_[yyyymmdd]`：武汉天河国际机场国内机场到达时间表

#### :writing_hand: 自定义

**命令**

```shell
cd ./crawler
# 输出当天武汉天河国际机场国内机场出发时间表
scrapy crawl dep_info -o {file_name.json}

# 输出当天武汉天河国际机场国内机场到达时间表
scrapy crawl arr_info -o {file_name.json}

#  以上，file_name为输出的文件名
```



## :open_file_folder: Requirements

Please see `./crawler/requirements.txt`

:point_down: How to install ?

```shell
pip install -r requirements.txt
```