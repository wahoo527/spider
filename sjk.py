import csv
import sqlite3

def create_table(cursor):
    cursor.execute('''DROP TABLE IF EXISTS data''')  # 删除已存在的表
    cursor.execute('''CREATE TABLE data
                      (URL TEXT, 标题 TEXT, 发布时间 TEXT, 新闻来源 TEXT, 发布地点 TEXT, 新闻内容 TEXT)''')

def insert_data(cursor, row):
    cursor.execute('INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)', row)

def import_csv_to_sqlite(csv_file, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    create_table(cursor)

    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_data = csv.reader(file)

        next(csv_data)  # Skip header row if present
        for row in csv_data:
            insert_data(cursor, row)

    conn.commit()
    conn.close()


csv_file = '北京.csv'
db_file = '北京.db'
import_csv_to_sqlite(csv_file, db_file)

