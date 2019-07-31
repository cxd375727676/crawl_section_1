import requests
import bs4
from bs4 import BeautifulSoup


def get_university_rank(num):
    # 输入top num 大学排名信息
    lst = []      # 列表的列表，存储爬取的数据
    r = requests.get("http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html")
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    
    # <tbody>标签记录了所有信息
    # <tbody>的每个子标签<tr>记录相应大学的全部信息，分散在<td>标签中
    for tr in soup.find("tbody").children:
        if isinstance(tr, bs4.element.Tag):
            university_info = tr.find_all("td")   # 记录每所大学信息的全部<td>标签列表
            university_list = [university_info[0].string,
                               university_info[1].string,
                               university_info[3].string]       # 记录每所大学排名、名称、得分的列表
            lst.append(university_list)
    
    print_type = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(print_type.format("排名","学校名称","总分", chr(12288)))   # chr(12288) 是中文空格
    for i in range(num):
        print(print_type.format(lst[i][0], lst[i][1], lst[i][2], chr(12288)))


if __name__ == '__main__':
    num = int(input("Input the total amounts of universities you want to know the rank : "))  # eg: 输入10
    get_university_rank(num)
