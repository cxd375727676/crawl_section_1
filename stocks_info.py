import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback


def get_html_text(url, code="utf-8"):
    """ 人工查看页面的编码方式，提高速度"""
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""


def get_all_stocks():
    """ 获取所有上交所、深交所股票代码 """
    stock_list = []
    all_stock_url = "http://quote.eastmoney.com/stock_list.html"  # 东方财富网
    all_stock_soup = BeautifulSoup(get_html_text(all_stock_url), "html.parser")
    for tag_a in all_stock_soup.find_all("a"):     # 股票代码在a标签的属性里，以sz或sh打头后面接六位数字
        try:
            href = tag_a.attrs["href"]     # 含有股票代码的链接字符串
            stock_list.append(re.findall(r"s[hz]\d{6}", href)[0])
        except:
            continue
    return stock_list


def get_stocks_info(stock_list):
    stocks_info = {}
    count = 0
    for stock in stock_list:
        individual_stock_url = "https://gupiao.baidu.com/stock/" + stock + ".html"
        html = get_html_text(individual_stock_url)
        try:
            if html != "":
                soup = BeautifulSoup(html, "html.parser")
                stock_info = soup.find('div',attrs={'class': 'stock-bets'})   # div标签记录个股信息
                stock_name = stock_info.find_all(attrs={'class': 'bets-name'})[0].text.split()[0]
                # dt是包含键的tag， dd是包含值的tag
                key_tag_list = stock_info.find_all('dt')
                value_tag_list = stock_info.find_all('dd')
                stock_info_dict = {key.text: value.text for key, value in zip(key_tag_list, value_tag_list)}
                stock_info_dict["股票名称"] = stock_name
                stocks_info[stock] = stock_info_dict
        except:
            traceback.print_exc()
            continue
        finally:
            count += 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(stock_list)), end="")
    return pd.DataFrame(stocks_info).T


if __name__ == '__main__':
    stocks = get_all_stocks()
    some_stocks = stocks[1000: 1050]  # 暂时查看部分股票数据
    df = get_stocks_info(some_stocks)
    df.to_excel(r".\output\part_stocks_info.xlsx")
