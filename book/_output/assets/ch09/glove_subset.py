import numpy as np
import os

def create_glove_subset():
    """
    从完整的GloVe词向量文件中，提取一个小的子集，用于教学演示。
    这个子集包含动物、颜色、数字和一些常用概念，
    可以很好地展示词向量的语义聚集特性（如“物以类聚”）。
    """
    # 定义文件路径，相对于项目根目录
    glove_file = 'book/assets/ch09/glove.6B.50d.txt'
    subset_file = 'book/assets/ch09/glove_subset.txt'

    # 定义需要提取的词语列表
    # 动物
    animals = ["cat", "dog", "horse", "lion", "tiger", "bear", "elephant", "monkey", "bird", "fish"]
    # 颜色
    colors = ["red", "green", "blue", "yellow", "black", "white", "orange", "purple", "pink", "brown"]
    # 数字
    numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "zero"]
    # 经典概念，用于展示 "king" - "man" + "woman" ≈ "queen" 等关系
    concepts = ["king", "queen", "man", "woman", "boy", "girl", "prince", "princess"]
    # 科技公司
    tech_companies = ["apple", "microsoft", "google", "amazon", "facebook"]

    words_to_extract = set(animals + colors + numbers + concepts + tech_companies)

    # 检查GloVe文件是否存在
    if not os.path.exists(glove_file):
        print(f"错误: GloVe文件未在 '{glove_file}' 找到。")
        print("请从 https://nlp.stanford.edu/projects/glove/ 下载 'glove.6B.zip' 并解压到 book/assets/ch09/ 目录下。")
        return

    print(f"正在从 {glove_file} 读取词向量...")
    
    extracted_lines = []
    try:
        with open(glove_file, 'r', encoding='utf-8') as f:
            for line in f:
                # 快速获取第一个词
                word = line.split(' ', 1)[0]
                if word in words_to_extract:
                    extracted_lines.append(line)
                    # 找到所有词后可以提前退出，提高效率
                    if len(extracted_lines) == len(words_to_extract):
                        break
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return

    print(f"成功找到 {len(extracted_lines)} 个匹配的词向量。")
    
    # 确保输出目录存在
    output_dir = os.path.dirname(subset_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 将提取到的词向量写入新文件
    try:
        with open(subset_file, 'w', encoding='utf-8') as f:
            for line in extracted_lines:
                f.write(line)
        print(f"已将词向量子集保存到: {subset_file}")
    except Exception as e:
        print(f"写入文件时发生错误: {e}")

if __name__ == "__main__":
    create_glove_subset()

