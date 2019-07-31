# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['http://quote.eastmoney.com/stock_list.html']  # 初始url：东方财富网获取所有A股代码

    def parse(self, response):
        """ 对start_urls返回的response对象进行解析
        这里需要提取股票代码并发起后续requests请求
        采用css选择器 """
        for href in response.css('a::attr(href)').extract()[1000: 1050]:   # 此处只爬取部分股票
            try:
                stock_code = re.findall(r"[s][hz]\d{6}", href)[0]
                url = "https://gupiao.baidu.com/stock/" + stock_code + ".html"
                yield scrapy.Request(url, callback=self.parse_stock)
            except:
                continue

    def parse_stock(self, response):
        """ 对个股页面的返回对象进行解析
        这里需要提取个股信息并产生数据"""
        soup = BeautifulSoup(response.text, "html.parser")
        stock_info = soup.find('div', attrs={'class': 'stock-bets'})  # div标签记录个股信息
        stock_name = stock_info.find_all(attrs={'class': 'bets-name'})[0].text.split()[0]
        # dt是包含键的tag， dd是包含值的tag
        key_tag_list = stock_info.find_all('dt')
        value_tag_list = stock_info.find_all('dd')
        stock_info_dict = {key.text: value.text for key, value in zip(key_tag_list, value_tag_list)}
        stock_info_dict["股票名称"] = stock_name
        yield stock_info_dict
