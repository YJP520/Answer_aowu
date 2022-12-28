"""
@Project : Answer the question.
@Time : 2022/12/04
@Author : YU.J.P
@Version: 1.0
@CopyRight: 2022(Yu.J.P)
"""

from py2neo import Graph

########################################################################################################################


class AnswerSearcher:
    def __init__(self):
        self.g = Graph('http://localhost:7474', user='neo4j', password='123456')

    def answer_prettify(self, question_type, answers):
        """
        根据对应的qustion_type，调用相应的回复模板
        :param question_type:
        :param answers:
        :return:
        """
        final_answer = None  # 最终的答案
        if not answers:
            return ''

        # 上映时间（测试完成，单个和多个）
        if question_type == 'online_time':
            l_ = []
            for i in answers:
                if i['s.title'] not in l_:
                    l_.append(i['s.title'])
                    final_answer = '{0}的上线时间是：{1}'.format(i['s.title'], i['s.releasedate'])

        # 风格（测试完成，单个和多个）
        elif question_type == 'song_genre':
            dict_ = {}
            # print(answers)
            for i in answers:
                if i['m.title'] not in dict_:
                    dict_[i['m.title']] = i['b.name']
                else:
                    dict_[i['m.title']] += ("、" + i['b.name'])
            # print(dict_)
            for i in dict_:
                final_answer = "{0}的类型是：{1}".format(i, dict_[i])

        # 简介（测试完成，单个和多个）
        elif question_type == 'album':
            l_ = []
            for i in answers:
                if i['s.title'] not in l_:
                    l_.append(i['s.title'])
                    final_answer = '{0}的简介是：{1}'.format(i['s.title'], i['s.introduction'])

        # 歌手
        elif question_type == 'who_sing':
            dict_ = {}
            # print(answers)
            for i in answers:
                if i['s.title'] not in dict_:
                    dict_[i['s.title']] = i['n.name']
                else:
                    dict_[i['s.title']] += ("、" + i['n.name'])
            # print(dict_)
            res = []
            for i in dict_:
                res.append("{0}的演唱者：{1}".format(i, dict_[i]))
            final_answer = res[0]

        # 歌手简介（测试完成，单个和多个）
        elif question_type == 'who_singer':
            l_ = []
            # print(answers)
            for i in answers:
                if i['n.name'] not in l_:
                    l_.append(i['n.name'])
                    # 添加找不到的处理
                    if i['n.introduction'] != '':
                        final_answer = '{0}的简介,{1}'.format(i['n.name'], i['n.introduction'])
                    else:
                        final_answer = "找不到{0}的介绍".format(i['n.name'])

        # 歌词
        elif question_type == 'word':
            for i in answers:
                final_answer = '{0}的歌词：\n{1}'.format(i['n.title'], i['n.word'])

        # 歌曲对专辑
        elif question_type == 'song_zhuanji':
            for i in answers:
                final_answer = '{0}的所属专辑：\n{1}'.format(i['n.title'], i['n.zhuanji'])

        # 专辑对歌曲
        elif question_type == 'zhuanji_song':
            for i in answers:
                final_answer = '{0}专辑下有曲目：\n{1}'.format(i['n.title'], i['n.zhuanji'])

        # 歌手对专辑
        elif question_type == 'singer_zhuanji':
            l_ = ''
            for i in answers:
                l_ += '《' + i['s.zhuanji'] + '》, '
            final_answer = '{0}的所有专辑：\n{1}'.format(answers[0]['n.name'], l_)

        # 歌手对歌曲
        elif question_type == 'singer_song':
            l_ = ''
            for i in answers:
                l_ += '《' + i['s.title'] + '》, '
            final_answer = '{0}演唱的歌曲：\n{1}'.format(answers[0]['n.name'], l_)

        # 返回回答
        return final_answer

    def search_main(self, cqls):
        """
        执行cypher查询，并返回相应结果
        :param cqls:
        :return:
        """
        final_answers = []
        for cql_ in cqls:
            queries = cql_['cql']
            question_type = cql_['question_type']
            # 得到返回的答案集
            answers = []
            for query in queries:
                # 执行查询语句
                res = self.g.run(query).data()
                answers += res
            # 处理答案集，获得最佳答案
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

########################################################################################################################


if __name__ == '__main__':
    searcher = AnswerSearcher()
