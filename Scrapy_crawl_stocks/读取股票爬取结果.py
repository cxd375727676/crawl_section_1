# 读取stocks_info.jsonl文件并清理，转化为pandas数据框
import jsonlines
import pandas as pd
import numpy as np


stocks_info = []
with jsonlines.open(r'.\Scrapy_crawl_stocks\stocks_info.jsonl', 'r') as rf:
    for stock_info in rf:
        stocks_info.append(stock_info)
stocks_info = pd.DataFrame(stocks_info)   # 原始数据


def handle_1(x):
    """ 内盘、外盘、成交量有“手”与“万手”之分，统一以“万手”为单位，转化为数值 """
    if isinstance(x, str):
        if x.endswith("万手"):
            return float(x[:-2])
        elif x.endswith("手"):
            return float(x[:-1]) / 10000
    else:
        return x     # np.nan


def handle_2(x):
    """ 委比、振幅、换手率去掉百分号, 总市值、总股本、流通市值、流通股本去掉亿 """
    if isinstance(x, str):
        if x[-1] in ['亿', '%']:
            return x[:-1]
    else:
        return x


def handle_3(x):
    """ 成交额有万、亿单位，统一以万为单位"""
    if isinstance(x, str):
        if x.endswith('亿'):
            return (float(x[:-1])) * 10000
        if x.endswith('万'):
            return float(x[:-1])
    else:
        return x


cleaned_info = stocks_info.copy()
cleaned_info = cleaned_info.applymap(lambda x: x.strip())                     # 删去空白等字符
cleaned_info.set_index("股票名称", inplace=True)
cleaned_info = cleaned_info.applymap(lambda x: np.nan if x == '--' else x)    # '--'转为np.nan
for indicator in ['内盘', '外盘', '成交量']:
    cleaned_info[indicator] = cleaned_info[indicator].map(handle_1)
for indicator in ['委比', '振幅', '换手率', '总市值', '总股本', '流通市值', '流通股本']:
    cleaned_info[indicator] = cleaned_info[indicator].map(handle_2)
cleaned_info['成交额'] = cleaned_info['成交额'].map(handle_3)
cleaned_info = cleaned_info.astype(float)                                # 最后全部转换为浮点型
