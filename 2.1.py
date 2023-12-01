import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import random
from lxml import etree
import requests

# 创建ChromeDriver实例
driver = webdriver.Chrome(executable_path='E:\Downloads\chromedriver_win321\chromedriver.exe')
driver.maximize_window()

# 手动指定模块链接
module_links = {
    '要闻': 'https://xw.qq.com/',
    '北京': 'https://xw.qq.com/a/area/bj',
    '财经': 'https://new.qq.com/ch/finance/',
    '科技': 'https://new.qq.com/ch/tech/',
    '娱乐': 'https://new.qq.com/ch/ent/',
    '国际': 'https://new.qq.com/ch/world/',
    '军事': 'https://new.qq.com/ch/milite/',
    '游戏': 'https://xw.qq.com/m/game',
    '乐活': 'https://xw.qq.com/m/lehuo'
}

# 要爬取的条数
news_count = 100

# 存储爬取的数据
news_data = []

# 遍历每个模块链接
for module, module_link in module_links.items():
    driver.execute_cdp_cmd("Emulation.setUserAgentOverride", {
        "userAgent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
    })
    driver.get(module_link)

    # 模拟页面滚动加载更多新闻
    for x in range(25):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(1, 5))

    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    tree = etree.HTML(data)

    # //*[@id="__xw_next_view_root"]/div[1]/section[2]/div/div/div/a 爬要闻用这个
    # //*[@id="__xw_next_view_root"]/div/div[2]/div/div[2]/div[2]/div/a 爬其它用这个
    tar_news_list = tree.xpath('//*[@id="__xw_next_view_root"]/div/div[2]/div/div[2]/div[2]/div/a')
    count = 0
    count1 =0
    for news_list1 in tar_news_list:
        if count1 >= news_count:
            break
        count += 1

        # 跳过置顶(不需要时改成0）
        zhiding=0
        if count <= zhiding:
            continue

        element_html = etree.tostring(news_list1, encoding='unicode')
        news_list = BeautifulSoup(element_html, 'lxml')

        # 解析新闻数据
        news_url_elem = news_list.find('a')
        if news_url_elem and 'href' in news_url_elem.attrs:
            news_url = news_url_elem['href']
        else:
            continue  # 跳过没有有效链接的新闻
        # news_title = news_list.find('a').text
        driver.execute_cdp_cmd("Emulation.setUserAgentOverride", {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        })

        # 点击新闻链接进入详细页面
        driver.get(news_url)
        time.sleep(random.randint(1, 3))  # 等待页面加载，可根据需要调整等待时间

        # 获取详细页面的数据
        detail_data = driver.page_source
        detail_soup = BeautifulSoup(detail_data, 'lxml')
        news_title_elem=detail_soup.find('div', class_='content-article')
        news_title = news_title_elem.find('h1').text if news_title_elem else ""
        # clean_title = news_title.replace("<h1>", "").replace("</h1>", "")

        # 解析详细页面数据
        media_name_elem = detail_soup.find('p', class_='media-name')
        news_source = media_name_elem.text.strip() if media_name_elem else ""
        news_location_elem = detail_soup.find('p', class_='media-meta')
        if news_location_elem:
            spans = news_location_elem.find_all('span')
            for span in spans:
                if '发布于' in span.text:
                    news_location = span.text.replace('发布于', '').strip()
                    break
                else:
                    news_location = ""
        else:
            news_location = ""

        news_content_elem = detail_soup.find('div', class_='content-article')

        # 解析第一张图片链接
        news_image = ""
        if news_content_elem:
            img_elem = news_content_elem.find('img', class_='content-picture')
            if img_elem and 'src' in img_elem.attrs:
                img_url = img_elem['src']
                # 下载图片并保存到本地
                if not img_url.startswith('http'):
                    img_url = 'http:' + img_url  # 添加缺失的协议
                response = requests.get(img_url)
                image_path = f"要闻/{count1}.jpg"  # 图片保存路径
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                news_image = image_path
        else:
            news_image = ""
        news_content = ""
        if news_content_elem:
            paragraphs = news_content_elem.find_all('p', class_='one-p')
            for paragraph in paragraphs:
                if paragraph.find('img', class_='content-picture'):
                    img_elem = paragraph.find('img', class_='content-picture')
                    if 'src' in img_elem.attrs:
                        img_url = img_elem['src']
                        if not img_url.startswith('http'):
                            img_url = 'http:' + img_url  # 补全缺失的协议
                        news_content += f"【图片】{img_url}\n"
                news_content += paragraph.text.strip() + '\n'
        else:
            news_content =""

        # news_content = news_content_elem.text.strip() if news_content_elem else ""

        media_meta_elem = detail_soup.find('p', class_='media-meta')
        if media_meta_elem:
            time_elem = media_meta_elem.find_all('span')[0]
            news_time = str(time_elem.text) if time_elem else ""
            news_time = news_time.replace("/", '-')

        # 添加到爬取结果列表
        if news_content:
            count1 +=1
            news_data.append([news_url, news_title, news_time, news_source, news_location, news_content])
            print(f"第：{count1}条")
            print(news_title)


# 保存为CSV文件
csv_header = ['URL', '标题', '发布时间', '新闻来源', '发布地点', '新闻内容']
csv_file = '游戏.csv'

try:
    with open(csv_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerows(news_data)
    print(f"爬取完成，数据已保存到'{csv_file}'文件中")

except Exception as e:
    print(f"保存CSV文件时出现异常：{str(e)}")

# 关闭浏览器
driver.quit()
