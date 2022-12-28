import requests
from lxml import etree
import re
import csv
import numpy as np


def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62'}
    res = requests.get(url, headers=headers).text
    html = etree.HTML(res)
    return html


# 获取歌单的id
def get_url_list_id(html):
    id = html.xpath('//a[@class="msk"]/@href')
    for i in range(len(id)):
        id[i] = re.sub('\D', '', id[i])
    return id


# 获取歌单内音乐的id
def get_music_id(music_list_id):
    html = get_html(f'https://music.163.com/playlist?id={music_list_id}')
    id = html.xpath('//ul[@class="f-hide"]//li//a/@href')
    for i in range(len(id)):
        id[i] = re.sub('\D', '', id[i])
    return id


# 获取歌曲信息
def get_music_info(id):
    html = get_html(f'https://music.163.com/song?id={id}')
    # print(etree.tostring(html).decode('utf-8'))
    data = {
        'music_name': html.xpath('//em[@class="f-ff2"]/text()')[0],
        'singer': html.xpath('//p[@class="des s-fc4"][1]/span/@title')[0],
        'music_id': id,
    }
    return data


if __name__ == '__main__':
    data_count = 0
    for page in range(1):
        url = f'https://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={page*35}'
        # url = 'https://music.163.com/#/discover/playlist/?cat=%E5%8D%8E%E8%AF%AD&order=hot'
        html = get_html(url)

        # 获取到当前页面的歌单id
        url_list_id = get_url_list_id(html)
        print(url_list_id)

        # 普通方法
        for i in range(len(url_list_id)):
            # 获取到当前歌单中所有歌曲的id
            music_id = get_music_id(url_list_id[i])
            # 遍历id，获取到每一首音乐的信息
            for j in range(len(music_id)):
                music_info = get_music_info(music_id[j])
                print(music_info)
                # 将获取到的信息存储到本地
                data_count += 1
                print('\r', f'页码：{page+1}\t歌单：{i+1}\t歌曲：{j+1}/{len(music_id)}\t总数：{data_count}', end='', flush=True)
