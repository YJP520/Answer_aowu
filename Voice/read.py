"""
@Project : Answer_aowu
@Time : 2022/11/30
@Author : YU.J.P
@Version: 1.0
@CopyRight: 2022(Yu.J.P)
"""

import pyttsx3

########################################################################################################################


def test_pyttsx3(string):
    """
    机器朗读
    """
    engine = pyttsx3.init()

    # RATE
    rate = engine.getProperty('rate')  # getting details of current speaking rate
    print(rate)  # printing current voice rate
    engine.setProperty('rate', 150)  # setting up new voice rate

    # VOLUME
    volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
    print(volume)  # printing current volume level
    engine.setProperty('volume', 1.0)  # setting up volume level between 0 and 1

    # VOICE
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[0].id)  # changing index, changes voices. o for male
    # engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female

    engine.say(string)
    engine.runAndWait()
    engine.stop()

    # Saving Voice to a file
    engine.save_to_file(string3, 'test.mp3')
    engine.runAndWait()


def chick_voice():
    """
    检查语音包
    """
    tts = pyttsx3.init()
    voices = tts.getProperty('voices')
    for voice in voices:
        print('id = {} \nname = {} \n'.format(voice.id, voice.name))


def reader(content, rate=150, volume=1.0, index=0):
    """
    机器朗读
    """
    engine = pyttsx3.init()
    # RATE
    engine.setProperty('rate', rate)  # setting up new voice rate
    # VOLUME
    engine.setProperty('volume', volume)  # setting up volume level between 0 and 1
    # VOICE
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[index].id)  # changing index, changes voices. o for male
    # read
    engine.say(content)
    engine.runAndWait()
    engine.stop()
    # Saving Voice to a file
    # engine.save_to_file(string3, 'test.mp3')
    # engine.runAndWait()


# MIAN
if __name__ == "__main__":

    string = "。寒蝉凄切，对长亭晚，骤雨初歇。都门帐饮无绪，留恋处，兰舟摧发。执手相看泪眼，竟无语凝噎。念去去千里烟波，暮霭沈沈楚天阔。" \
             "多情自古伤离别，更那堪冷落清秋节。今宵酒醒何处，杨柳岸、晓风残月。此去经年，应是良辰好景虚设。便纵有千种风情，更与何人说。"

    # 苏轼《江神子·黄昏犹是雨纤纤》
    string2 = "。黄昏犹是雨纤纤。晓开帘，欲平檐。江阔天低、无处认青帘。孤坐冻吟谁伴我？揩病目，捻衰髯。" \
              "使君留客醉厌厌。水晶盐，为谁甜？手把梅花、东望忆陶潜。雪似故人人似雪，虽可爱，有人嫌。"

    string3 = ".曾经有一份真诚的爱情摆在我的面前，但是我没有珍惜。等到了失去的时候才后悔莫及，尘世间最痛苦的事莫过于此。" \
              "如果上天可以给我一个机会再来一次的话，我会对你说三个字‘我爱你’。如果非要把这份爱加上一个期限，我希望是一万年！"

    test_pyttsx3(string)
    # chick_voice()
    pass
