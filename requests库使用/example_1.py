import requests


def get_html_text(url):
    try:
        headers = {'user-agent': 'Mozilla/5.0'}   # 伪装浏览器
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()   # 不是200引发异常
        r.encoding = r.apparent_encoding  # 前者是从headers中charset字段提取，缺失则是ISO；后者是从文本中推断的解析方式。
        return r.text
    except:
        return "产生异常"