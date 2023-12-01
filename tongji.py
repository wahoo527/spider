import csv

csv_file = '要闻.csv'

title_lengths = []  # 存储新闻标题长度
locations = []  # 存储新闻发布地点

# 读取CSV文件
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        title = row[1]
        location = row[4]
        title_lengths.append(len(title))
        locations.append(location)

# 计算新闻标题平均长度
avg_title_length = sum(title_lengths) / len(title_lengths)

# 统计新闻发布地点
location_counts = {}
for location in locations:
    if location in location_counts:
        location_counts[location] += 1
    else:
        location_counts[location] = 1

# 输出结果
print(f"新闻标题平均长度: {avg_title_length:.2f}")
print("新闻发布地点统计:")
a=0

for location, count in location_counts.items():
    if location:
        print(f"{location}: {count}")
    else:
        print(f"无地点: {count}")
    # a=a+count
    # print(a)
