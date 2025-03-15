import requests
import pandas as pd
import os

# 请求头
headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "proxy-connection": "keep-alive",
    "x-requested-with": "XMLHttpRequest"
}

# 创建存储PDF文件的文件夹
os.makedirs('announcements', exist_ok=True)


# 获取公告数据的函数
def fetch_announcements(start_date, end_date, page_num=1, page_size=100):
    url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
    body = {
        "pageNum": page_num,
        "pageSize": page_size,
        "column": "szse",
        "tabName": "fulltext",
        "plate": "",
        "stock": "",
        "searchkey": "",
        "secid": "",
        "category": "category_ndbg_szsh",
        "trade": "",
        "seDate": f"{start_date}~{end_date}",
        "sortName": "",
        "sortType": "",
        "isHLtitle": "true"
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, data=body)

    if response.status_code == 200:
        data = response.json()
        if 'announcements' in data:
            announcements_list = []
            for announcement in data['announcements']:
                sec_code = announcement.get("secCode", "")
                sec_name = announcement.get("secName", "")
                title = announcement.get("announcementTitle", "")
                download_url = f"http://static.cninfo.com.cn/{announcement.get('adjunctUrl', '')}"
                announcements_list.append([sec_code, sec_name, title, download_url])
            print(f"Fetched {len(announcements_list)} announcements. hasMore is {data['hasMore']}")
            return announcements_list, data['hasMore']
        else:
            print("No announcements found.")
            return [], False
    else:
        print(f"Request failed with status code: {response.status_code}")
        return [], False


# 下载PDF文件的函数
def download_pdf(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {filename}, Status code: {response.status_code}")


# 主函数
def main():
    start_date = "2024-02-13"
    end_date = "2024-03-01"
    page_size = 30
    page_num = 1
    all_announcements = []

    while True:
        announcements, has_more = fetch_announcements(start_date, end_date, page_num=page_num, page_size=page_size)
        if announcements:
            all_announcements.extend(announcements)
            if not has_more:
                break
            page_num += 1
        else:
            break

    if all_announcements:
        # 使用 pandas 创建 DataFrame
        df = pd.DataFrame(all_announcements, columns=["公司代码", "公司名称", "年报标题", "下载地址"])

        # 将 DataFrame 保存到 Excel 文件中
        df.to_excel("announcements.xlsx", index=False)
        print("数据已保存到 announcements.xlsx 文件中")

        # 下载 PDF 文件
        for announcement in all_announcements:
            sec_code, sec_name, title, download_url = announcement
            title = title.replace("/", "_")
            filename = f"announcements/{sec_code}_{sec_name}_{title}.pdf"
            download_pdf(download_url, filename)


# 执行主函数
if __name__ == "__main__":
    main()

