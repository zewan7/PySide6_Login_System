from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QThread, Signal
from ..UI_all.Ui_register import Ui_Form as ui_register
from ..models.create_tables import Session, UserTable
from ..utls.email_verification import validate_email_with_lib
from ..utls.send_email import send_email_captcha
from ..utls.get_captcha import get_captcha
from ..utls.api_hash import PasswordHasher
from datetime import datetime
from ..utls.check_password import validate_password
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import redis_conn

hash_pwd = PasswordHasher()


class RegisterHander(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.register_ui = ui_register()
        self.register_ui.setupUi(self)
        self.register_func()

    # 注册界面按钮
    def register_func(self):
        # 已有账号切换到登陆页面
        self.register_ui.pushButton_okAccount.clicked.connect(self.existing_account)
        # 获取验证码
        self.register_ui.pushButton_get_vCode.clicked.connect(self.get_captcha_and_to_email)
        # 注册确定
        self.register_ui.pushButton_register.clicked.connect(self.add_register)

    def existing_account(self):
        # 清空输入
        self.clear_register_lineEdit()
        self.parent.setWindowTitle("登陆")
        # 跳转到登陆
        self.parent.stacked_layout.setCurrentIndex(0)

    def clear_register_lineEdit(self):
        self.register_ui.lineEdit_name.clear()
        self.register_ui.lineEdit_email.clear()
        self.register_ui.lineEdit_pwd.clear()
        self.register_ui.lineEdit_pwd_ok.clear()
        self.register_ui.lineEdit_Vcode.clear()
        self.register_ui.label_led.clear()
        self.register_ui.pushButton_get_vCode.setEnabled(True)
        self.register_ui.pushButton_get_vCode.setText("获取验证码")

    # 注册获取验证码并发送到邮箱和redis
    def get_captcha_and_to_email(self):
        email = self.register_ui.lineEdit_email.text()
        # 使用信号触发后台线程  
        self.worker_thread = SendEmailWorkerThread(email)
        self.worker_thread.captcha_sent.connect(self.on_captcha_sent)
        self.worker_thread.start()
        # 初始化定时器用于倒计时  
        self.update_button_timer = QTimer(self)
        self.update_button_timer.timeout.connect(self.update_button_text)

    def update_button_text(self):
        # 更新按钮文本，直到倒计时结束  
        text = self.register_ui.pushButton_get_vCode.text()
        if text == "0":
            self.register_ui.pushButton_get_vCode.setEnabled(True)
            self.register_ui.pushButton_get_vCode.setText("获取验证码")
            self.update_button_timer.stop()
        elif text == "获取验证码":
            self.update_button_timer.stop()
        else:
            num = int(text) - 1
            self.register_ui.pushButton_get_vCode.setText(str(num))

    def on_captcha_sent(self, success, text):
        # 后台线程发送完验证码后调用  
        if success:
            # 启动倒计时  
            self.register_ui.pushButton_get_vCode.setEnabled(False)
            self.register_ui.pushButton_get_vCode.setText(str(59))
            self.update_button_timer.start(1000)
            self.register_ui.label_led.setText(text)
        else:
            self.register_ui.label_led.setText(text)

    # 用户注册确定
    def add_register(self):
        name = self.register_ui.lineEdit_name.text()
        email = self.register_ui.lineEdit_email.text()
        password = self.register_ui.lineEdit_pwd.text()
        password_ok = self.register_ui.lineEdit_pwd_ok.text()
        vcode = self.register_ui.lineEdit_Vcode.text()
        res, msg = validate_password(password)
        if not res:
            self.register_ui.label_led.setText(msg)
            return
        redis_captcha = redis_conn.get(email)
        print("redis_captcha:", redis_captcha)
        if vcode != redis_captcha:
            self.register_ui.label_led.setText("验证码不正确")
            return
        if password != password_ok:
            self.register_ui.label_led.setText("两次密码不一致")
            return
        if not name:
            self.register_ui.label_led.setText("未输入用户名")
            return

        now_time = datetime.now()
        hash_password = hash_pwd.hash_password(password)
        new_user = UserTable(email=email, name=name, password=hash_password, create_time=now_time, update_time=now_time)
        
        session = Session()
        try:
            session.add(new_user)
            session.commit()
        finally:
            session.close()
            
        print(f"{email} 用户注册成功")
        # 清空输入
        self.clear_register_lineEdit()
        self.parent.setWindowTitle("登陆")
        # 跳转到登陆
        self.parent.stacked_layout.setCurrentIndex(0)


# 发送email工作线程类  
class SendEmailWorkerThread(QThread):
    captcha_sent = Signal(bool, str)

    def __init__(self, email):
        super().__init__()
        self.email = email

    def run(self):
        session = Session()
        try:
            email_exist = session.query(UserTable).filter_by(email=self.email).first()
        finally:
            session.close()
            
        if email_exist:
            self.captcha_sent.emit(False, "Email已注册")
            return

        # 验证邮箱是否有效
        email_validate = validate_email_with_lib(self.email)
        if not email_validate:
            self.captcha_sent.emit(False, "请输入有效的邮箱地址")
            return

        captcha = get_captcha()
        # 发送邮件
        res = send_email_captcha(email=self.email, captcha=captcha)
        if not res:
            self.captcha_sent.emit(False, "发送失败，请输入正确的邮箱地址")
            return

        # 添加到redis
        redis_conn.set(self.email, captcha, ex=300)
        self.captcha_sent.emit(True, "验证码发送成功")
