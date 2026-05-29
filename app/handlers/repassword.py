from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QThread, Signal
from ..UI_all.Ui_rePwd import Ui_Form as ui_rePwd
from ..models.create_tables import Session, UserTable
from ..utls.send_email import send_email_captcha
from ..utls.get_captcha import get_captcha
from ..utls.api_hash import PasswordHasher
from ..utls.check_password import validate_password
from datetime import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import redis_conn

hash_pwd = PasswordHasher()


class RePasswordHander(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.repwd_ui = ui_rePwd()
        self.repwd_ui.setupUi(self)
        self.repwd_func()
        self.parent.setWindowTitle("修改密码")

    # 忘记密码页面
    def repwd_func(self):
        # 返回到登陆
        self.repwd_ui.pushButton_reReturn.clicked.connect(self.re_return_login)
        # 获取验证码
        self.repwd_ui.pushButton_reGetNum.clicked.connect(self.re_get_num)
        # 确定
        self.repwd_ui.pushButton_reOk.clicked.connect(self.re_ok)

    def re_return_login(self):
        # 清空输入
        self.clear_repwd_lineEdit()
        self.parent.setWindowTitle("登陆")
        # 跳转到登陆
        self.parent.stacked_layout.setCurrentIndex(0)

    def clear_repwd_lineEdit(self):
        self.repwd_ui.lineEdit_reEmailPath.clear()
        self.repwd_ui.lineEdit_reVcode.clear()
        self.repwd_ui.lineEdit_reNewPwd.clear()
        self.repwd_ui.label_reLed.clear()
        self.repwd_ui.pushButton_reGetNum.setEnabled(True)
        self.repwd_ui.pushButton_reGetNum.setText("获取验证码")

    def re_get_num(self):
        # 修改密码 邮箱验证和发送eamil
        email_text = self.repwd_ui.lineEdit_reEmailPath.text()
        self.checke_mail_thread = CheckEmailExistsThread(email=email_text)
        self.checke_mail_thread.send_sig.connect(self.on_captcha_sent)
        self.checke_mail_thread.start()
        self.update_button_timer = QTimer(self)
        self.update_button_timer.timeout.connect(self.update_button_text)

    def update_button_text(self):
        # 更新按钮文本，直到倒计时结束  
        text = self.repwd_ui.pushButton_reGetNum.text()
        if text == "0":
            self.repwd_ui.pushButton_reGetNum.setEnabled(True)
            self.repwd_ui.pushButton_reGetNum.setText("获取验证码")
            self.update_button_timer.stop()
        elif text == "获取验证码":
            self.update_button_timer.stop()
        else:
            num = int(text) - 1
            self.repwd_ui.pushButton_reGetNum.setText(str(num))

    def on_captcha_sent(self, success, text):
        # 后台线程发送完验证码后调用  
        if success:
            # 启动倒计时  
            self.repwd_ui.pushButton_reGetNum.setEnabled(False)
            self.repwd_ui.pushButton_reGetNum.setText(str(59))
            self.update_button_timer.start(1000)
            self.repwd_ui.label_reLed.setText(text)
        else:
            self.repwd_ui.label_reLed.setText(text)

    def re_ok(self):
        # 修改密码确定按钮
        email_text = self.repwd_ui.lineEdit_reEmailPath.text()
        re_captcha = self.repwd_ui.lineEdit_reVcode.text()
        re_redis_captcha = redis_conn.get(email_text)
        re_password = self.repwd_ui.lineEdit_reNewPwd.text()

        if not email_text:
            self.repwd_ui.label_reLed.setText("请输入邮箱")
            return
        res, msg = validate_password(re_password)
        if not res:
            self.repwd_ui.label_reLed.setText(msg)
            return
        if re_captcha == re_redis_captcha:
            session = Session()
            try:
                re_user = session.query(UserTable).filter_by(email=email_text).first()
                if re_user:
                    hash_password = hash_pwd.hash_password(re_password)
                    re_user.password = hash_password
                    re_user.update_time = datetime.now()
                    session.commit()
                    print("密码修改成功")
                    # 清空输入
                    self.clear_repwd_lineEdit()
                    self.parent.setWindowTitle("登陆")
                    # 跳转到登陆
                    self.parent.stacked_layout.setCurrentIndex(0)
                else:
                    self.repwd_ui.label_reLed.setText("查不到此邮箱")
            finally:
                session.close()
        else:
            self.repwd_ui.label_reLed.setText("验证码不正确")


class CheckEmailExistsThread(QThread):
    send_sig = Signal(bool, str)

    def __init__(self, email):
        super().__init__()
        self.email = email

    def run(self):
        session = Session()
        try:
            re_user = session.query(UserTable).filter_by(email=self.email).first()
        finally:
            session.close()
            
        if not re_user:
            self.send_sig.emit(False, "输入的邮箱不存在")
            return
        captcha = get_captcha()
        redis_conn.set(self.email, captcha, ex=300)
        send_email_captcha(email=self.email, captcha=captcha)
        self.send_sig.emit(True, "验证码发送成功")
