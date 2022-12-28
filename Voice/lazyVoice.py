import PySimpleGUI as sg
import pyttsx3
import time

# 语音包序号，默认第一个(中文)
voiceIdx = 0

# 主题色
sg.theme('DarkAmber')

# 窗口布局
layout = [
    [sg.Text('请输入需要转换为语音的文字')],
    [sg.Multiline('', size=(100, 10), key='textContent')],
    [sg.Text('调整速率')],
    [sg.Slider(range=(100, 400), default_value=200, size=(50, 15), orientation='horizontal', font=('Helvetica', 12),
               key='rateNumber')],
    [sg.Text('语音选项')],
    [sg.Radio('中文', 'S1', enable_events=True, key='id0', default=True),
     sg.Radio('日语', 'S1', enable_events=True, key='id1'),
     sg.Radio('英语', 'S1', enable_events=True, key='id2'),
     sg.Radio('中文(香港)', 'S1', enable_events=True, key='id3'),
     sg.Radio('中文(台湾)', 'S1', enable_events=True, key='id4'), ],
    [sg.Button('试听', key='ttsButton1'), sg.Button('转换为MP3', key='ttsButton2'), ]
]

# 创建窗口
window = sg.Window('文字转语音工具', layout)

# 循环处理事件
while True:
    event, values = window.read()

    # 用户点击X关闭窗口或点击退出按钮
    if event == sg.WIN_CLOSED:
        break

    if event == 'id0':
        voiceIdx = 0
    if event == 'id1':
        voiceIdx = 1
    if event == 'id2':
        voiceIdx = 2
    if event == 'id3':
        voiceIdx = 3
    if event == 'id4':
        voiceIdx = 4
    print(voiceIdx)

    if event == 'ttsButton1' or event == 'ttsButton2':
        # 初始化
        tts = pyttsx3.init()

        # 获取新旧 RATE
        rate = tts.getProperty('rate')
        newRate = int(values['rateNumber'])
        # 修改 RATE
        tts.setProperty('rate', newRate)

        # # 获取 VOICES
        voices = tts.getProperty('voices')

        # # 修改 VOICE
        tts.setProperty('voice', voices[voiceIdx].id)

        # 获取文字
        textContent = values['textContent']

        # 试听
        if event == 'ttsButton1':
            tts.say(textContent)
            tts.runAndWait()
            tts.stop()

        # 并转换为MP3
        if event == 'ttsButton2':
            mp3Filename = str(voiceIdx) + '_' + str(time.time()) + ".mp3"
            info = '转换成功，详见：' + mp3Filename
            tts.save_to_file(textContent, mp3Filename)
            tts.runAndWait()
            sg.popup('', info, '', title='提示')

window.close()
