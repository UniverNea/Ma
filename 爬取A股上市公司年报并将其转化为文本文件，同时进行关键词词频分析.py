import requests
from bs4 import BeautifulSoup
import os
import jieba
from collections import Counter

# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 定义获取年报链接的函数
def get_annual_report_links(stock_code):
    url = f'http://www.cninfo.com.cn/new/hisAnnouncement/query'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        if '年度报告' in a.text:
            links.append(a['href'])
    return links

# 定义下载年报并保存为文本文件的函数
def download_and_save_report(url, file_name):
    response = requests.get(url, headers=headers)
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(response.text)

# 定义分析关键词词频的函数
def analyze_keyword_frequency(file_name, keywords):
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
    words = jieba.lcut(text)
    word_count = Counter(words)
    keyword_frequency = {keyword: word_count[keyword] for keyword in keywords}
    return keyword_frequency

# 主函数
def main():
    stock_code = '000001'  # 以平安银行为例
    report_links = get_annual_report_links(stock_code)
    if not os.path.exists('reports'):
        os.makedirs('reports')
    for i, link in enumerate(report_links):
        file_name = f'reports/report_{i+1}.txt'
        download_and_save_report(link, file_name)
        keywords = ['风险', '利润', '增长']  # 自定义关键词
        frequency = analyze_keyword_frequency(file_name, keywords)
        print(f'Report {i+1} Keyword Frequency: {frequency}')

if __name__ == '__main__':
    main()

#代码说明：获取年报链接：get_annual_report_links 函数通过爬取指定股票代码的年报链接。
#关键词词频分析：analyze_keyword_frequency 函数使用 jieba 进行中文分词，并统计指定关键词的词频。
#主函数：main 函数整合了上述功能，遍历所有年报链接，下载并分析关键词词频。
#注意事项：
#需要安装 requests, beautifulsoup4, jieba 等库。
#代码中的 stock_code 和 keywords 可以根据实际需求进行修改。
#由于爬取的是公开数据，请确保遵守相关网站的使用条款和法律法规。