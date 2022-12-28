"""
@Project : Create Graph of Knowledge.
@Time : 2022/12/03
@Author : YU.J.P
@Version: 1.0
@CopyRight: 2022(Yu.J.P)
"""

import csv
from py2neo import Graph, Node, Relationship, NodeMatcher

########################################################################################################################


def createGraph():
    """
    导入知识图谱数据库
    :return:
    """
    # graph直接写账号密码会不安全
    g = Graph('http://localhost:7474', user='neo4j', password='123456')
    # 创建config以及db.cfg用来存储信息

    # # 添加电影类型结点
    # with open('data_csv/genre.csv', 'r', encoding='utf-8') as f:
    #     reader = csv.reader(f)
    #     for item in reader:
    #         # 第一行的标签不是咱们需要的内容，line_num表示文件的第几行
    #         if reader.line_num == 1:
    #             continue
    #         print("当前行数：", reader.line_num, "当前内容", item)
    #         test_node_1 = Node("Genre", id=item[0], name=item[1])
    #         g.merge(test_node_1, "Genre", "id")

    # 添加歌曲内容结点 song_id	title	专辑	歌词	歌曲简介	发行时间	歌手
    with open('data_csv/song.csv', 'r', encoding='gbk') as f:
        reader = csv.reader(f)
        for item in reader:
            # 第一行的标签不是咱们需要的内容，line_num表示文件的第几行
            if reader.line_num == 1:
                continue
            print("当前行数：", reader.line_num, "当前内容", item)
            test_node_1 = Node("song", id=item[0], title=item[1], zhuanji=item[2], word=item[3],
                               introduction=item[4], releasedate=item[5])
            g.merge(test_node_1, "song", "id")

    # 添加歌手结点
    with open('data_csv/singer.csv', 'r', encoding='gbk') as f:
        reader = csv.reader(f)
        for item in reader:
            # 第一行的标签不是咱们需要的内容，line_num表示文件的第几行
            if reader.line_num == 1:
                continue
            print("当前行数：", reader.line_num, "当前内容", item)
            test_node_1 = Node("singer", id=item[0], name=item[1], introduction=item[2])
            g.merge(test_node_1, "singer", "id")

    matcher = NodeMatcher(g)
    findNode = matcher.match('singer', id='1').first()
    print(findNode)

    # 添加歌曲与歌手的关系
    with open('data_csv/song_to_singer.csv', 'r', encoding='gbk') as f:
        reader = csv.reader(f)
        for item in reader:
            # 第一行的标签不是咱们需要的内容，line_num表示文件的第几行
            if reader.line_num == 1:
                continue
            print("当前行数：", reader.line_num, "当前内容", item)
            findNode = matcher.match('song', id=item[0]).first()
            endNode = matcher.match('singer', id=item[1]).first()
            # 添加关系
            relationships = Relationship(endNode, '唱', findNode)
            g.merge(relationships, "", "id")

    # # 添加电影与类型的关系
    # with open('data_csv/movie_to_genre.csv', 'r', encoding='utf-8') as f:
    #     reader = csv.reader(f)
    #     for item in reader:
    #         # 第一行的标签不是咱们需要的内容，line_num表示文件的第几行
    #         if reader.line_num == 1:
    #             continue
    #         print("当前行数：", reader.line_num, "当前内容", item)
    #         findNode = matcher.match('Movie', id=item[0]).first()
    #         endNode = matcher.match('Genre', id=item[1]).first()
    #         # 添加关系
    #         relationships = Relationship(findNode, '是', endNode)
    #         g.merge(relationships, "", "id")

########################################################################################################################


def createWordList():
    """
    创建词表
    :return:
    """
    # with open('data_csv/genre.csv', 'r', encoding='utf-8') as f:
    #     l_genre = []
    #     reader = csv.reader(f)
    #     for item in reader:
    #         # 第一行的标签不是咱们需要的内容，line_num表示文件的第几行
    #         if reader.line_num == 1:
    #             continue
    #         # print("当前行数：",reader.line_num,"当前内容",item)
    #         # 只要类别
    #         print("当前行数：", reader.line_num, "当前内容", item[1])
    #         if item[1] not in l_genre:
    #             l_genre.append(item[1])

    with open('data_csv/song.csv', 'r', encoding='gbk') as f:
        l_movie = []
        reader = csv.reader(f)
        for item in reader:
            # 第一行的标签不是咱们需要的内容，line_num表示文件的第几行
            if reader.line_num == 1:
                continue
            # print("当前行数：",reader.line_num,"当前内容",item)
            # 只要电影名字
            print("当前行数：", reader.line_num, "当前内容", item[1])
            if item[1] not in l_movie:
                l_movie.append(item[1])

    with open('data_csv/singer.csv', 'r', encoding='gbk') as f:
        l_person = []
        # 数据集除了第一行代表属性外，第一列为实体1，第二列为实体2，第三列是两者英文关系，第四列为两者中文关系
        reader = csv.reader(f)
        for item in reader:
            # 第一行的标签不是咱们需要的内容，line_num表示文件的第几行
            if reader.line_num == 1:
                continue
            # print("当前行数：",reader.line_num,"当前内容",item)
            # 只要演员
            print("当前行数：", reader.line_num, "当前内容", item[1])
            if item[1] not in l_person:
                l_person.append(item[1])

    # f_genre = open('data_word/genre.txt', 'w+')
    # f_genre.write('\n'.join(list(l_genre)))
    # f_genre.close()

    f_movie = open('data_word/song.txt', 'w+')
    f_movie.write('\n'.join(list(l_movie)))
    f_movie.close()

    f_person = open('data_word/singer.txt', 'w+')
    f_person.write('\n'.join(list(l_person)))
    f_person.close()

########################################################################################################################


def graphSearch():
    """
    查询 结点 关系
    :return:
    """
    g = Graph("http://localhost:7474/", user='neo4j', password='123456')
    matcher = NodeMatcher(g)
    print(matcher.match("Singer", name="封茗囧菌").first())

########################################################################################################################


if __name__ == "__main__":
    # First Step
    createGraph()

    # Second Step
    # createWordList()

    # graphSearch()
    pass
