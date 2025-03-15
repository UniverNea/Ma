import fitz  # PyMuPDF
import jieba
from collections import Counter
import re

# 定义关键词
keywords = ["AI", "人工智能", "深度学习"]

# 提取 PDF 文本
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# 分词并统计词频
def analyze_text(text, keywords):
    # 使用 jieba 分词
    words = jieba.lcut(text)
    # 统计所有词的词频
    word_count = Counter(words)
    # 统计关键词的词频
    keyword_freq = {keyword: word_count[keyword] for keyword in keywords}
    return keyword_freq

# 计算相关性得分（基于词频和共现频率）
def calculate_relevance_score(text, keywords):
    # 分词
    words = jieba.lcut(text)
    # 统计关键词的词频
    keyword_freq = {keyword: words.count(keyword) for keyword in keywords}
    # 统计关键词的共现频率
    co_occurrence = {keyword: 0 for keyword in keywords}
    window_size = 10  # 共现窗口大小
    for i in range(len(words) - window_size):
        window = words[i:i + window_size]
        for keyword in keywords:
            if keyword in window:
                co_occurrence[keyword] += 1
    # 计算相关性得分（词频 + 共现频率）
    relevance_score = {keyword: keyword_freq[keyword] + co_occurrence[keyword] for keyword in keywords}
    return relevance_score

# 主函数
def main(pdf_path):
    # 提取 PDF 文本
    text = extract_text_from_pdf(pdf_path)
    # 计算相关性得分
    relevance_score = calculate_relevance_score(text, keywords)
    # 打印结果
    print("关键词相关性得分：")
    for keyword, score in relevance_score.items():
        print(f"{keyword}: {score}")

# 运行主函数
if __name__ == "__main__":
    pdf_path = "/Users/sher.m/Downloads/测试PDF/001309.PDF"  # 替换为你的 PDF 文件路径
    main(pdf_path)