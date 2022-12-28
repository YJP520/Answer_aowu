"""
@Project : Spider For Getting information.
@Time : 2022/12/05
@Author : YU.J.P
@Version: 1.0
@CopyRight: 2022(Yu.J.P)
"""

# 自动化爬取
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv


########################################################################################################################


def auto_spider():
    """
    自动化爬虫 - ChromeDriver
    :param url: 待爬取网址
    :param keyword: 关键词
    :return: None
    """
    path = 'singer.csv'
    fp = open(path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(fp)
    # 写入表头
    titleList = ('singer_id', 'name', '歌手简介')
    writer.writerow(titleList)
    # 写入数据
    id = 1

    browser = webdriver.Chrome()
    # 种子站点
    url = 'https://y.qq.com/n/ryqq/singer_list'
    # 访问指定网页
    browser.get(url)
    # 隐式等待 确保内容结点完全加载出来
    browser.implicitly_wait(3)

    # # 定位搜索框
    # # 找到id属性为key的标签
    # input_tag = browser.find_element(by='id', value='key')
    # # 模拟键盘输入关键词
    # input_tag.send_keys(keyword)
    # # 模拟键盘输入enter键
    # input_tag.send_keys(Keys.ENTER)

    # 数据抓取
    # 查找多节点 查找到所有的li标签
    names = browser.find_elements(By.CLASS_NAME, 'singer_list_txt__item')
    # 地址 名字 价格 评论
    for good in names:
        # 地址
        # link = good.find_element(By.TAG_NAME, value='a').get_attribute('href')
        # 名字 css选择器
        name = good.find_element(By.CSS_SELECTOR, value='a').text
        # 评论
        # comment = good.find_element(By.CSS_SELECTOR, value='.p-commit a').text
        titleList = (id, name)
        print(titleList)
        writer.writerow(titleList)
        id += 1

    # 等待5秒钟
    time.sleep(30)
    fp.close()

########################################################################################################################


def operate_csv():
    """
    csv 文件操作
    :return:
    """
    path = 'song.csv'
    fp = open(path, 'w', newline='')
    writer = csv.writer(fp)
    # 写入表头
    titleList = ('1', '2', '3', '4', '5')
    writer.writerow(titleList)
    # 写入数据

    fp.close()


def write_song_csv():
    """
    song.csv 数据写入操作
    :return:
    """
    path = 'song.csv'
    fp = open(path, 'w', newline='')
    writer = csv.writer(fp)
    # 写入表头
    titleList = ('song_id', 'title', '歌词', '歌曲简介', '专辑', '发行时间')
    writer.writerow(titleList)
    # 写入数据

    fp.close()


def write_singer_csv():
    """
    singer.csv 数据写入操作
    :return:
    """
    path = 'singer.csv'
    fp = open(path, 'w', newline='')
    writer = csv.writer(fp)
    # 写入表头
    titleList = ('singer_id', 'name', '歌手简介')
    writer.writerow(titleList)
    # 写入数据

    fp.close()


def write_genre_csv():
    """
    genre.csv 数据写入操作
    :return:
    """
    path = 'genre.csv'
    fp = open(path, 'w', newline='')
    writer = csv.writer(fp)
    # 写入表头
    titleList = ('genre_id', 'genre')
    writer.writerow(titleList)
    # 写入数据
    writer.writerow((1, "华语"))
    writer.writerow((2, "欧美"))
    writer.writerow((3, "日语"))
    writer.writerow((4, "韩语"))
    fp.close()


def write_song_to_genre_csv():
    """
    song_to_genre.csv 数据写入操作
    :return:
    """
    path = 'song_to_genre.csv'
    fp = open(path, 'w', newline='')
    writer = csv.writer(fp)
    # 写入表头
    titleList = ('song_id', 'genre_id')
    writer.writerow(titleList)
    # 写入数据

    fp.close()


def write_song_to_singer_csv():
    """
    song_to_singer.csv 数据写入操作
    :return:
    """
    path = 'song_to_singer.csv'
    fp = open(path, 'w', newline='')
    writer = csv.writer(fp)
    # 写入表头
    titleList = ('song_id', 'singer_id')
    writer.writerow(titleList)
    # 写入数据

    fp.close()


########################################################################################################################


# MIAN
if __name__ == "__main__":
    auto_spider()

    # operate_csv()
    # write_song_csv()
    # write_singer_csv()
    # write_genre_csv()
    # write_song_to_genre_csv()
    # write_song_to_singer_csv()

    print("Finished...")
    pass
