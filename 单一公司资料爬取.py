Python 3.12.8 (v3.12.8:2dc476bcb91, Dec  3 2024, 14:43:20) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license()" for more information.
>>> import requests
... import pandas as pd
... 
... params = {
...     "stock": "600519",  # 股票代码（如贵州茅台）
...     "category": "category_ndbg_szsh;category_bndbg_szsh",  # 年报+半年报类别
...     "trade": "金融业",  # 可选行业分类
...     "pagenum": 1,
...     "pagesize": 30,
...     "seDate": f"{当前年份-3}-01-01~{当前日期}"  # 动态生成近三年时间范围
... }
... headers = {
...     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
...     "Referer": "http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice"
