# -*- coding: utf-8 -*-
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
sys.path.append(current_dir)
from PySide6.QtCore import QSize, QtMsgType, qInstallMessageHandler
from PySide6.QtWidgets import QApplication, QStackedLayout, QWidget, QVBoxLayout
from PySide6.QtGui import QIcon
from app.utls.api_hash import PasswordHasher
from app.handlers.login import LoginHander
from app.handlers.register import RegisterHander
from app.handlers.repassword import RePasswordHander
# ==================GUI导入=============================
# from Image_GUI.main_page import MyMainpage
from Excel_Main_GUI.MergeExcel import MyMainpage
# from Modern_GUI.main import MainWindow as MyMainpage


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.hash_password = PasswordHasher()
        self.login = LoginHander(self)
        self.register = RegisterHander(self)
        self.repwd = RePasswordHander(self)
        self.add_stacked_layout()
        self.setWindowTitle("登陆")
        # icon = QIcon(QIcon.fromTheme(u"emblem-shared"))
        # self.setWindowIcon(icon)
        icon_path = os.path.join(current_dir, 'app', 'images', 'ico', 'cactus.ico')
        self.setWindowIcon(QIcon(icon_path))

        # 登陆成功后发出的信号
        self.login.longin_ok.connect(self.show_main_window)

    # 堆叠登录、注册、忘记密码到一个模块显示
    def add_stacked_layout(self):
        self.setMinimumSize(QSize(326, 290))
        self.setMaximumSize(QSize(326, 290))
        # 创建一个容器 QWidget 来容纳 QStackedLayout  
        self.container = QWidget()
        self.stacked_layout = QStackedLayout(self.container)

        # 将页面 QWidget 添加到 stacked layout  
        self.stacked_layout.addWidget(self.login)
        self.stacked_layout.addWidget(self.register)
        self.stacked_layout.addWidget(self.repwd)

        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)
        self.layout().addWidget(self.container)

    # 登陆成功后显示主窗口
    def show_main_window(self, is_ok, user_info):
        if is_ok:
            self.close()
            self.main_window = MyMainpage(self, user_info)
            self.main_window.show()


def custom_qt_message_handler(mode, context, message):
    # 如果是这个特定的 D3D11 报错，直接忽略，不打印到控制台
    if "Failed to resize D3D11 swapchain" in message:
        return
    # 其他的按照原样可以不拦截，如果不想打印任何Qt内部警告，可以把下面这行注释掉
    # print(message)

def main():
    app = QApplication(sys.argv)
    # 安装自定义的消息拦截器
    qInstallMessageHandler(custom_qt_message_handler)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
