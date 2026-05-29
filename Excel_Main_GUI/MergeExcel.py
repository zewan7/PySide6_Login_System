# -*- coding: utf-8 -*-
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
# 坚决不能在模块全局使用 os.chdir()，否则会导致打包后抛出 FileNotFoundError，并且会破坏主程序的相对路径！
sys.path.append(current_dir)
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QSize, Signal, QTimer, QDateTime
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyMergeExcel.Concat_Excel import Concat_File
from threading import Thread
from UI.背景3 import Ui_MainWindow as ui_mian
from UI.excel_ui import Ui_MainWindow as ui_excel
from UI.path_ui import Ui_MainWindow as ui_path
from UI.意见建议 import Ui_Form as ui_opinion

concat_file = Concat_File()
version_number = '1.0.1'


class EmittingStr(QtCore.QObject):
    # 定义信号
    textWritten = QtCore.Signal(str)

    def write(self, text):
        # 调用信号传入文本
        self.textWritten.emit(str(text))
        
    def flush(self):
        pass


class MyMainpage(QMainWindow):
    def __init__(self, parent=None, user_inof={}):
        super().__init__()
        self.parent = parent
        self.user_inof = user_inof
        self.name = self.user_inof.get('user_name', '游客')
        # 坚决不使用 os.chdir()，使用绝对路径拼接
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(current_dir)

        # 主界面
        self.ui_main = ui_mian()
        self.ui_main.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(current_dir, 'ico', '猫.jpg')))
        self.time_q = QTimer(self)
        self.time_q.timeout.connect(self.update_time)
        self.time_q.start(1000)
        self.label_show()
        self.run()

    def run(self):
        # 设置Button图片
        self.ui_main.pushButton_6.setIcon(QIcon(os.path.join(current_dir, 'ico', '猫咪.jpg')))
        # 设置图片大小
        self.ui_main.pushButton_6.setIconSize(QSize(350, 221))
        # 图片
        self.ui_main.pushButton_6.clicked.connect(self.bClicked)
        self.ui_main.pushButton1.clicked.connect(self.clicked_excel)
        self.ui_main.pushButton2.clicked.connect(self.clicked_button2)
        self.ui_main.pushButton3.clicked.connect(self.clicked_button3)
        self.ui_main.pushButton4.clicked.connect(self.clicked_button4)
        self.ui_main.pushButton5.clicked.connect(self.suggestion_btn)
        # 返回登陆
        self.ui_main.pushButton_re_login.clicked.connect(self.re_login)

        # 下面将输出重定向到textEdit中
        sys.stdout = EmittingStr()
        sys.stdout.textWritten.connect(self.outputWritten)

    def label_show(self):
        self.ui_main.label_2.setText("提示：输出文件均在桌面【输出文件夹】中")
        author_label = QLabel('Copyright (c) 2021 By Peter Liu')
        version_label = QLabel(f"v{version_number}")
        self.statusBar().addWidget(author_label, 1)
        # 将版本号标签添加为永久部件，以确保它始终在最右侧
        self.statusBar().addPermanentWidget(version_label)

    def update_time(self):
        now_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.ui_main.label.setText(f"欢迎：{self.name}  |  当前时间：{now_time}")

    def outputWritten(self, text):
        # 获取界面指针
        cursor = self.ui_main.textEdit.textCursor()
        # 界面指针到最后
        cursor.movePosition(QtGui.QTextCursor.End)
        # 添加文本
        cursor.insertText(text)
        # 添加到界面
        self.ui_main.textEdit.setTextCursor(cursor)
        # 显示到最后
        self.ui_main.textEdit.ensureCursorVisible()

    def re_login(self):
        self.close()
        self.parent.show()

    def bClicked(self):
        self.ui_main.textEdit.clear()
        result = concat_file.TAG()
        self.ui_main.textEdit.setText(result)

    def suggestion_btn(self):
        # 意见建议
        # 清空主显示界面
        self.ui_main.textEdit.clear()
        # 调用函数
        self.sg = Suggestion()
        self.sg.signal_email_str.connect(self.send_str)

    def send_str(self, text):
        self.ui_main.textEdit.setText(text)
        self.sg.close()

    def clicked_excel(self):
        # 清空主显示界面
        self.ui_main.textEdit.clear()
        # 调用函数
        PathExcel()

    def clicked_button2(self):
        # 合并csv
        self.ui_main.textEdit.clear()
        PathExcelCsv().clicked_button_2()

    def clicked_button3(self):
        # 合并所有excel
        self.ui_main.textEdit.clear()
        PathExcelCsv().clicked_button_3()

    def clicked_button4(self):
        # 合并所有sheet
        self.ui_main.textEdit.clear()
        PathExcelCsv().clicked_button_4()


class PathExcel(QMainWindow):
    # 执行1模块
    # excel文件路劲含Sheet
    def __init__(self):
        super().__init__()
        self.ui = ui_excel()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(current_dir, 'ico', '猫.jpg')))
        path = "格式如：C:\\Users\\ee\\Desktop\\文件夹\\excel演示文件夹"
        # 设置lable标签文字演示字段
        self.ui.label_1.setText(path)
        self.clicked_button_1()
        # 下面将输出重定向到textEdit中
        sys.stdout = EmittingStr()
        sys.stdout.textWritten.connect(self.outputWritten)

    def outputWritten(self, text):
        # 获取界面指针
        cursor = self.ui.textEdit.textCursor()
        # 界面指针到最后
        cursor.movePosition(QtGui.QTextCursor.End)
        # 添加文本
        cursor.insertText(text)
        # 添加到界面
        self.ui.textEdit.setTextCursor(cursor)
        # 显示到最后
        self.ui.textEdit.ensureCursorVisible()

    def clicked_button_1(self):
        def clicked_button1():
            def start_excel():
                # 获取地址输入
                path1 = self.ui.lineEdit.text()
                # 获取sheet输入
                sheet_name = self.ui.lineEdit_2.text()
                if not sheet_name:
                    sheet_name = 0
                # 调用函数执行excel合并
                concat_file.merge_excel(path=path1, sheet_name=sheet_name)

            # 创建一个线程
            thread = Thread(target=start_excel)
            thread.start()

        # 点击按钮开始执行
        self.ui.pushButton.clicked.connect(clicked_button1)
        # 显示窗口
        self.show()


class PathExcelCsv(QMainWindow):
    # 执行2/3/4模块
    def __init__(self):
        super().__init__()
        self.ui = ui_path()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(current_dir, 'ico', '猫.jpg')))
        # 下面将输出重定向到textEdit中
        sys.stdout = EmittingStr()
        sys.stdout.textWritten.connect(self.outputWritten)

    def outputWritten(self, text):
        # 获取界面指针
        cursor = self.ui.textEdit.textCursor()
        # 界面指针到最后
        cursor.movePosition(QtGui.QTextCursor.End)
        # 添加文本
        cursor.insertText(text)
        # 添加到界面
        self.ui.textEdit.setTextCursor(cursor)
        # 显示到最后
        self.ui.textEdit.ensureCursorVisible()

    def clicked_button_2(self):
        def clicked_button():
            def csv():
                text = self.ui.lineEdit_1.text()
                concat_file.merge_csv(path=text)

            thread = Thread(target=csv)
            thread.start()

        path = "格式如：C:\\Users\\ee\\Desktop\\文件夹\\csv演示文件夹"
        # 设置lable标签文字演示字段
        self.ui.lable_1.setText(path)
        self.ui.pushButton.clicked.connect(clicked_button)
        # 显示窗口
        self.show()

    def clicked_button_3(self):
        def clicked_button():
            def all_excel():
                text = self.ui.lineEdit_1.text()
                concat_file.merge_all_excel(path=text)

            thread = Thread(target=all_excel)
            thread.start()

        path = "格式如：C:\\Users\\ee\\Desktop\\文件夹 (多文件夹批量处理)"
        # 设置lable标签文字演示字段
        self.ui.lable_1.setText(path)
        self.ui.pushButton.clicked.connect(clicked_button)
        # 显示窗口
        self.show()

    def clicked_button_4(self):
        def clicked_button():
            def excel_sheet():
                text = self.ui.lineEdit_1.text()
                concat_file.merge_sheet(path=text)

            thread = Thread(target=excel_sheet)
            thread.start()

        path = "格式如：C:\\Users\\ee\\Desktop\\文件夹\\演示文件excel含多个Sheet文件.xlsx"
        # 设置lable标签文字演示字段
        self.ui.lable_1.setText(path)
        self.ui.pushButton.clicked.connect(clicked_button)
        # 显示窗口
        self.show()


class Suggestion(QMainWindow):
    signal_email_str = Signal(str)

    # 意见建议
    def __init__(self):
        super().__init__()
        # concat_file = Concat_File()
        self.ui = ui_opinion()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.join(current_dir, 'ico', '猫.jpg')))
        self.clicked_button_5()

    def clicked_button_5(self):
        def pushButton_stop():
            # 取消按钮，关闭窗口
            self.close()

        def pushButton_2_strat():
            # 确定按钮，多线程执行
            def suggestion_thread():
                text1 = self.ui.textEdit.toPlainText()
                # 调用模块执行
                res = concat_file.email_text(text=text1)
                self.signal_email_str.emit(res)

            thread = Thread(target=suggestion_thread)
            thread.start()

        # 点击确定按钮
        self.ui.pushButton_2.clicked.connect(pushButton_2_strat)
        self.ui.pushButton.clicked.connect(pushButton_stop)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyMainpage()
    win.show()
    sys.exit(app.exec())
