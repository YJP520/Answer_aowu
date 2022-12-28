from urllib.request import urlopen

import pyttsx3
import pyaudio
import wave

from bs4 import BeautifulSoup
from tqdm import tqdm
import sys
import json
import base64
import time
import requests

for Jarvis in range(100):
    def record_audio(wave_out_path, record_second):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1  # 2
        RATE = 16000  # 44100
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        wf = wave.open(wave_out_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        print("* recording")
        for i in tqdm(range(0, int(RATE / CHUNK * record_second))):
            data = stream.read(CHUNK)
            wf.writeframes(data)
        print("* done recording")
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()


    record_audio("output.wav", record_second=5)  # 录音时间可以自定义

    # 百度语音识别：根据output.wav文件生成识别的文字

    IS_PY3 = sys.version_info.major == 3

    if IS_PY3:
        from urllib.request import urlopen
        from urllib.request import Request
        from urllib.error import URLError
        from urllib.parse import urlencode

        timer = time.perf_counter
    else:
        from urllib import urlopen
        from urllib import Request
        from urllib import URLError
        from urllib import urlencode

        if sys.platform == "win32":
            timer = time.clock
        else:
            # On most other platforms the best timer is time.time()
            timer = time.time

    API_KEY = '************************'
    SECRET_KEY = '*********************************'

    # 需要识别的文件
    AUDIO_FILE = 'output.wav'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
    # 文件格式
    FORMAT = AUDIO_FILE[-3:]  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式

    CUID = '123456PYTHON'
    # 采样率
    RATE = 16000  # 固定值

    # 普通版

    DEV_PID = 1537  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
    ASR_URL = 'http://vop.baidu.com/server_api'
    SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有


    class DemoError(Exception):
        pass


    """  TOKEN start """

    TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'


    def fetch_token():
        params = {'grant_type': 'client_credentials',
                  'client_id': API_KEY,
                  'client_secret': SECRET_KEY}
        post_data = urlencode(params)
        if (IS_PY3):
            post_data = post_data.encode('utf-8')
        req = Request(TOKEN_URL, post_data)
        try:
            f = urlopen(req)
            result_str = f.read()
        except URLError as err:
            # print('token http response http code : ' + str(err.code))
            result_str = err.read()
        if (IS_PY3):
            result_str = result_str.decode()

        # print(result_str)
        result = json.loads(result_str)
        # print(result)
        if ('access_token' in result.keys() and 'scope' in result.keys()):
            # print(SCOPE)
            if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
                raise DemoError('scope is not correct')
            # print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
            return result['access_token']
        else:
            raise DemoError(
                'MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


    """  TOKEN end """

    if __name__ == '__main__':
        token = fetch_token()

        speech_data = []
        with open(AUDIO_FILE, 'rb') as speech_file:
            speech_data = speech_file.read()

        length = len(speech_data)

        if length == 0:
            raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)

        speech = base64.b64encode(speech_data)
        if (IS_PY3):
            speech = str(speech, 'utf-8')
        params = {'dev_pid': DEV_PID,
                  # "lm_id" : LM_ID,    #测试自训练平台开启此项
                  'format': FORMAT,
                  'rate': RATE,
                  'token': token,
                  'cuid': CUID,
                  'channel': 1,
                  'speech': speech,
                  'len': length
                  }
        post_data = json.dumps(params, sort_keys=False)
        # print post_data
        req = Request(ASR_URL, post_data.encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        try:
            begin = timer()
            f = urlopen(req)
            result_str = f.read()
            # print("Request time cost %f" % (timer() - begin))
        except URLError as err:
            # print('asr http response http code : ' + str(err.code))
            result_str = err.read()

        if (IS_PY3):
            result_str = str(result_str, 'utf-8')

        # print(result_str)
        # print(str(json.loads(result_str)['result'])[2:-2])

        with open("result.txt", "w") as of:
            of.write(result_str)

        final = str(json.loads(result_str)['result'])[2:-2].split("。")
        final_order = "".join(final)