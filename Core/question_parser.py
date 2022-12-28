"""
@Project : Match The Category Of Question.
@Time : 2022/12/04
@Author : YU.J.P
@Version: 1.0
@CopyRight: 2022(Yu.J.P)
"""


########################################################################################################################


class QuestionPaser:
    @classmethod
    def build_entityDict(cls, args):
        """
        构建实体字典
        :param args:
        :return:
        """
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    @classmethod
    def cql_transfer(cls, question_type, entities):
        """
        针对不同的问题，分开进行处理
        :param question_type:
        :param entities:
        :return:
        """
        if not entities:
            return []
        # 查询语句
        cql = []

        # 查询上映 tag
        if question_type == 'online_time':
            cql = ["match(s:song) where s.title='{0}' return s.releasedate, s.title".format(i) for i in entities]

        # 风格
        elif question_type == 'song_genre':
            cql = ["match(s:song)-[r:`是`]->(b) where s.title=\"{0}\" return b.name,s.title".format(i) for i in
                   entities]

        # 歌曲简介 tag
        elif question_type == 'album':
            cql = ["match(s:song) where s.title='{0}' return s.title, s.introduction".format(i) for i in
                   entities]

        # 查找歌手 tag
        elif question_type == 'who_sing':
            cql = ["match(n:singer)-[r:`唱`]->(s:song) where s.title=\"{0}\" return s.title, n.name".format(i) for i
                   in entities]

        # 歌手简介 tag
        elif question_type == 'who_singer':
            cql = ["match(n:singer)-[]->() where n.name=\"{0}\" return n.name, n.introduction".format(i) for i in
                   entities]

        # 歌词 tag
        elif question_type == 'word':
            cql = ["match(n:song) where n.title=\"{0}\" return n.title, n.word".format(i) for i in entities]

        # 歌曲对专辑 tag
        elif question_type == 'song_zhuanji':
            cql = ["match(n:song) where n.title=\"{0}\" return n.title, n.zhuanji".format(i) for i in entities]

        # 专辑对歌曲 tag
        elif question_type == 'zhuanji_song':
            cql = ["match(n:song) where n.zhuanji=\"{0}\" return n.zhuanji, n.title".format(i) for i in entities]

        # 歌手对专辑 tag
        elif question_type == 'singer_zhuanji':
            cql = ["match(n:singer)-[r:`唱`]->(s:song) where n.name =\"{0}\" return s.zhuanji, n.name".format(i)
                   for i in entities]

        # 歌手对歌曲 tag
        elif question_type == 'singer_song':
            cql = ["match(n:singer)-[r:`唱`]->(s:song) where n.name =\"{0}\" return s.title, n.name".format(i)
                   for i in entities]

        return cql

    @classmethod
    def parser_main(cls, res_classify):
        """
        解析主函数
        :param res_classify:
        :return:
        """
        # 提取出实体
        args = res_classify['args']
        entity_dict = cls.build_entityDict(args)
        # 提取出查询类型
        question_types = res_classify['question_types']
        # 返回查询语句的序列
        cqls = []
        for question_type in question_types:
            cql_ = {'question_type': question_type}
            cql = []
            if question_type == 'online_time':
                cql = cls.cql_transfer(question_type, entity_dict.get('song'))
            elif question_type == 'song_genre':
                cql = cls.cql_transfer(question_type, entity_dict.get('song'))
            elif question_type == 'album':
                cql = cls.cql_transfer(question_type, entity_dict.get('song'))
            elif question_type == 'who_sing':
                cql = cls.cql_transfer(question_type, entity_dict.get('song'))
            elif question_type == 'who_singer':
                cql = cls.cql_transfer(question_type, entity_dict.get('singer'))
            elif question_type == 'word':
                cql = cls.cql_transfer(question_type, entity_dict.get('song'))
            elif question_type == 'song_zhuanji':
                cql = cls.cql_transfer(question_type, entity_dict.get('song'))
            elif question_type == 'zhuanji_song':
                cql = cls.cql_transfer(question_type, entity_dict.get('song'))
            elif question_type == 'singer_zhuanji':
                cql = cls.cql_transfer(question_type, entity_dict.get('singer'))
            elif question_type == 'singer_song':
                cql = cls.cql_transfer(question_type, entity_dict.get('singer'))
            if cql:
                cql_['cql'] = cql
                cqls.append(cql_)
        return cqls


########################################################################################################################


if __name__ == '__main__':
    handler = QuestionPaser()
