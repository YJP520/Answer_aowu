"""
@Project : The Mian Running Process.
@Time : 2022/12/04
@Author : YU.J.P
@Version: 1.0
@CopyRight: 2022(Yu.J.P)
"""
import random

# 分类模块
from Core.question_classifier import QuestionClassifier
# 生成查询语句
from Core.question_parser import QuestionPaser
# 生成回答
from Core.answer_search import AnswerSearcher
# 语音输出
import pyttsx3
# Colors
from Plug_in.Colors import Color


########################################################################################################################


# 问答类
class Aowu:
    def __init__(self):
        self.classifier = QuestionClassifier()  # 分类
        self.searcher = AnswerSearcher()  # 生成回答
        # 语音初始化
        self.engine = pyttsx3.init()
        self.reader_init(250)

    def reader_init(self, rate=150, volume=1.0, index=0):
        """
        机器朗读初始化
        """
        self.engine = pyttsx3.init()
        # RATE
        self.engine.setProperty('rate', rate)  # setting up new voice rate
        # VOLUME
        self.engine.setProperty('volume', volume)  # setting up volume level between 0 and 1
        # VOICE
        voices = self.engine.getProperty('voices')  # getting details of current voice
        self.engine.setProperty('voice', voices[index].id)  # changing index, changes voices. o for male

    def cute_sorry(self, select):
        if select == 0:
            return 'Sorry, 这个问题好难理解呀！不过我会更加努力学习的！'
        elif select == 1:
            return '抱歉, 这个问题好难理解呀！不过我会更加努力学习的！'
        elif select == 2:
            return '对不起, 这个问题好难理解呀！不过我会更加努力学习的！'
        elif select == 3:
            return '喵喵喵, 这个问题好难理解呀！不过我会更加努力学习的！'
        elif select == 4:
            return '真不好意思, 这个问题好难理解呀！不过我会更加努力学习的！'
        else:
            return 'Sorry, 这个问题好难理解呀！不过我会更加努力学习的！'

    def answer(self, question):
        # 如果不能回答问题
        error = self.cute_sorry(random.randint(0, 4))
        # print(Color.yellow, error)
        # error = '喵喵喵, 你的问题好难理解呀！不过我会更加努力学习的！'
        # 提示 标准问题
        # standard_answer = ''
        # print(standard_answer)

        # 获取实体类别 问题中的属性类别
        res_classify = self.classifier.classify(question)
        if not res_classify:
            print(Color.blue, "Aowu:", Color.red, error)
            return error
            # self.engine.say("。" + error)
            # self.engine.runAndWait()
        else:
            print(Color.carmine, '类别：', res_classify)

            # 生成查询语句
            res_cql = QuestionPaser.parser_main(res_classify)
            print(Color.yellow, 'cql语句', res_cql)

            # 返回查询结果
            final_answers = self.searcher.search_main(res_cql)
            # print(Color.blue, "Aowu:", final_answers[0])

            if not final_answers:
                print(Color.blue, "Aowu:", Color.red, error)
                return error
            # 语音助手
            else:
                print(Color.blue, "Aowu:", final_answers[0])
                return final_answers[0]
                # self.engine.say(final_answers[0][0: 100])
                # self.engine.runAndWait()


########################################################################################################################

if __name__ == '__main__':
    # problems = ["十面埋伏和功夫的评分", "十面埋伏和功夫的上映时间", "十面埋伏和功夫的风格", "十面埋伏和功夫的简介",
    #             "十面埋伏和功夫的演员", "李连杰和成龙的简介",
    #             "成龙和李连杰和周星驰合作的电影", "成龙和李连杰和周星驰总共演了多少的电影", "成龙和李连杰合作的电影",
    #             "周星驰和李连杰的生日是？", "我女朋友是谁？"]

    aowu = Aowu()
    name = ''
    while name == '':
        print(Color.red, "Your Name:", end='')
        name = input()
    while True:
        print(Color.yellow, name, ":", end='')
        question = input()
        if question != '':
            aowu.answer(question)
