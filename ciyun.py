import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 从CSV文件加载数据
def load_data_from_csv(file_path, column_name):
    df = pd.read_csv(file_path)
    df[column_name] = df[column_name].astype(str)  # 将列转换为字符串类型
    return df[column_name]

# 生成词云
def generate_word_cloud(text):
    # 设置TrueType字体路径
    font_path = "msyh.ttf"  # 字体文件路径
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(' '.join(text))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# 主函数
def main():
    file_path = '北京.csv'  # 你的CSV文件路径
    column_name = '标题'  # 你要提取的列名

    # 从CSV文件加载数据
    text = load_data_from_csv(file_path, column_name)

    # 生成词云
    generate_word_cloud(text)

if __name__ == '__main__':
    main()
