"""
@Project : Classify The Question BY Simple.
@Time : 2022/12/04
@Author : YU.J.P
@Version: 1.0
@CopyRight: 2022(Yu.J.P)
"""

import os
import ahocorasick

########################################################################################################################


class QuestionClassifier:
    def __init__(self):
        # 特征词路径
        # self.person_path = "Core/data_word/person.txt"
        # self.movie_path = "Core/data_word/movie.txt"
        # self.genre_path = "Core/data_word/genre.txt"
        self.singer_path = "Core/data_word/singer.txt"
        self.song_path = "Core/data_word/song.txt"

        # 加载特征词 encoding="utf-8"
        self.singer_wds = [i.strip() for i in open(self.singer_path, encoding="gbk") if i.strip()]
        self.song_wds = [i.strip() for i in open(self.song_path, encoding="gbk") if i.strip()]
        # self.genre_wds = [i.strip() for i in open(self.genre_path, encoding="utf-8") if i.strip()]
        self.add_wos = ['aowu', 'AOWU', '你']

        # self.region_words = set(self.person_wds + self.movie_wds + self.genre_wds)
        self.region_words = set(self.singer_wds + self.song_wds + self.add_wos)

        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()

        # 问句疑问词
        # 剧情和演员简介容易冲突
        # 发布时间
        self.q2_qwds = ['发布', '发', '发专辑', '首映', '上映时间', '首映时间', '首播', '播出', '上线', '时间']
        # 风格
        self.q3_qwds = ['风格', '格调', '类型']
        # 专辑简介
        self.q4_qwds = ['专辑简介', '剧情', '内容', '故事', '简介', '情节', '梗概']
        # 歌手
        self.q5_qwds = ['歌手', '唱的', '演唱', '唱过', '哪些人', '哪一个']
        # 歌手简介
        self.q6_qwds = ['是谁', '介绍', '简介', '谁是', '详细信息', '信息']
        # 歌词
        self.q7_qwds = ['歌词', '词', '句子']
        # 歌曲对专辑
        self.q8_qwds = ['所属专辑', '属于', '对应专辑']
        # 专辑对歌曲
        self.q9_qwds = ['对应歌曲', '下有', '哪首歌']
        # 歌手对专辑
        self.q10_qwds = ['有哪些专辑', '唱过哪些专辑', '哪些专辑', '所有专辑']
        # 歌手对歌曲
        self.q11_qwds = ['哪些歌', '有哪些', '多少歌曲']

        print('classify model init finished...')

    def build_actree(self, wordlist):
        """
        造actree，加速过滤
        :param wordlist:
        :return:
        """
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    def build_wdtype_dict(self):
        """
        构造词对应的实体类型
        :return:
        """
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.singer_wds:
                wd_dict[wd].append('singer')
            if wd in self.song_wds:
                wd_dict[wd].append('song')
            # if wd in self.genre_wds:
            #     wd_dict[wd].append('gener')
        return wd_dict

    def check_words(self, wds, sent):
        """
        基于特征词进行分类
        :param wds:
        :param sent:
        :return:
        """
        for wd in wds:
            if wd in sent:
                return True
        return False

    def check_question(self, question):
        """
        问句过滤
        :param question:
        :return:
        """
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        return final_dict

    def classify(self, question):
        """
        分类主函数 实体及所属类别
        :param question:
        :return:
        """
        data = {}
        # 抽取问题中的属性类型
        dict = self.check_question(question)
        if not dict:
            return {}
        data['args'] = dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in dict.values():
            types += type_
        question_types = []

        # 上线时间
        if self.check_words(self.q2_qwds, question) and ('song' in types):
            question_type = 'online_time'
            question_types.append(question_type)
        # 歌曲风格
        if self.check_words(self.q3_qwds, question) and ('song' in types):
            question_type = 'song_genre'
            question_types.append(question_type)
        # 专辑简介
        if self.check_words(self.q4_qwds, question) and ('song' in types):
            question_type = 'album'
            question_types.append(question_type)
        # 演唱
        if self.check_words(self.q5_qwds, question) and ('song' in types):
            question_type = 'who_sing'
            question_types.append(question_type)
        # 歌手简介
        if self.check_words(self.q6_qwds, question) and ('singer' in types):
            question_type = 'who_singer'
            question_types.append(question_type)
        # 歌词
        if self.check_words(self.q7_qwds, question) and ('song' in types):
            question_type = 'word'
            question_types.append(question_type)
        # 歌曲对专辑
        if self.check_words(self.q8_qwds, question) and ('song' in types):
            question_type = 'song_zhuanji'
            question_types.append(question_type)
        # 专辑对歌曲
        if self.check_words(self.q9_qwds, question) and ('song' in types):
            question_type = 'zhuanji_song'
            question_types.append(question_type)
        # 歌手对专辑
        if self.check_words(self.q10_qwds, question) and ('singer' in types):
            question_type = 'singer_zhuanji'
            question_types.append(question_type)
        # 歌手对歌曲
        if self.check_words(self.q11_qwds, question) and ('singer' in types):
            question_type = 'singer_song'
            question_types.append(question_type)

        # 如果为空 默认搜索简介
        if not question_types:
            question_type = 'album'
            question_types.append(question_type)
            question_type = 'who_singer'
            question_types.append(question_type)
        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        return data


########################################################################################################################


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
