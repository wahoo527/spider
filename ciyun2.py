import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from nltk.corpus import stopwords

# 下载停用词列表
import nltk
nltk.download('stopwords')

# 从CSV文件加载数据
def load_data_from_csv(file_path, column_name):
    df = pd.read_csv(file_path)
    df[column_name] = df[column_name].astype(str)  # 将列转换为字符串类型
    return df[column_name]

# 分词并去除停用词
def tokenize(text):
    seg_list = jieba.cut(text)
    filtered_words = [word for word in seg_list if word not in stopwords.words('chinese')]
    return " ".join(filtered_words)

# 生成词云
def generate_word_cloud(text):
    font_path = "msyh.ttf"  # 字体文件路径
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# 主函数
def main():
    file_path = '要闻.csv'  # 你的CSV文件路径
    column_name = '标题'  # 你要提取的列名

    # 从CSV文件加载数据
    text = load_data_from_csv(file_path, column_name)

    # 分词并去除停用词
    text = text.apply(tokenize)

    # 生成词云
    generate_word_cloud(text.str.cat())

if __name__ == '__main__':
    main()
