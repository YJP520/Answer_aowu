"""
@Project : Answer_aowu
@Time : 2022/11/30
@Author : YU.J.P
@Version: 1.0
@CopyRight: 2022(Yu.J.P)
"""

import os
import sys
# CORE
from Core.aowu_graph import Aowu
# Colors
from Plug_in.Colors import Color
# UI
from aowu_ui_1 import Ui_MainWindow
# PYQT5
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon


########################################################################################################################

# 子窗口继承类
class Main_UI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 监听事件
        self.controller()
        # 按钮事件
        self.buttonInit()
        # 嗷呜精灵
        self.aowu = Aowu()

    # 监听事件都放在这里面
    def controller(self):
        # 设置监听
        self.actionSetting.triggered.connect(self.setting)
        # 退出监听
        self.actionExit.triggered.connect(self.exit)
        # 查找监听
        self.actionFind.triggered.connect(self.find)
        # 提示监听
        self.actionTips.triggered.connect(self.tips)

    # 设置动作按钮点击事件
    def setting(self):
        QMessageBox.about(self, 'Setting', '点击了设置动作')

    # 查询动作按钮点击事件
    def find(self):
        QMessageBox.about(self, 'find', '点击了查找动作')

    # 退出动作按钮店址事件
    def exit(self):
        QMessageBox.about(self, 'Exit', '确定退出程序？')
        # 退出程序
        self.actionExit()

    # 提示动作按钮店址事件
    def tips(self):
        QMessageBox.about(self, 'Tips', '点击了提示动作')

    # 按钮事件都放在这里面
    def buttonInit(self):
        self.pushButton.clicked.connect(self.button_ask)
        self.pushButton_2.clicked.connect(self.button_voice)
        self.pushButton_3.clicked.connect(self.button_talk)
        self.pushButton_4.clicked.connect(self.button_update)
        self.pushButton_5.clicked.connect(self.button_clear)
        # 加入一句话
        self.textBrowser.setTextColor(Qt.darkGreen)
        self.textBrowser.insertPlainText('AOWU：很高兴为您服务！')

    # BF按钮 动作按钮店址事件
    def button_ask(self):
        # QMessageBox.about(self, 'BF', '点击了提示动作')
        self.textBrowser.clear()

        question = self.lineEdit.text()
        # print(Color.red, question)
        if question != '':
            answer = self.aowu.answer(question)

            self.textBrowser.setTextColor(Qt.black)
            self.textBrowser.insertPlainText('AOWU:' + answer)
            # self.aowu.engine.say("。" + answer[0: 100])
            # self.aowu.engine.runAndWait()
        else:
            QMessageBox.about(self, 'ask', '请输入提问信息！！')

    # KMP按钮 动作按钮店址事件
    def button_voice(self):
        QMessageBox.about(self, 'voice', '点击了提示动作')
        # self.textBrowser.clear()

    # BM按钮 动作按钮店址事件
    def button_talk(self):
        self.textBrowser.clear()

        question = self.lineEdit.text()
        # print(Color.red, question)
        if question != '':
            answer = self.aowu.answer(question)

            self.textBrowser.setTextColor(Qt.black)
            self.textBrowser.insertPlainText('AOWU:' + answer)
            self.aowu.engine.say("。" + answer[0: 100])
            self.aowu.engine.runAndWait()
        else:
            QMessageBox.about(self, 'talk', '请输入提问信息！！')

    # Update按钮 动作按钮店址事件
    def button_update(self):
        QMessageBox.about(self, 'Update', '点击了提示动作')
        # self.textBrowser.clear()

    # Clear按钮 动作按钮店址事件
    def button_clear(self):
        # QMessageBox.about(self, 'Clear', '点击了按钮点动作')
        self.textBrowser.clear()


########################################################################################################################


# MAIN
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 应用图标
    app.setWindowIcon(QIcon('icon/icon.jpg'))
    app.setApplicationDisplayName('Aowu - 语音精灵')
    app_ui = Main_UI()
    app_ui.show()
    # 循环不退出
    sys.exit(app.exec_())
