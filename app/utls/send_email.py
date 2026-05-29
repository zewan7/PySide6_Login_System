import smtplib
from email.mime.text import MIMEText
from email.header import Header
from config import config

def send_email_captcha(email, captcha):
    """
    发送验证码到邮箱
    """
    try:
        subject = '您的验证码'
        contents = f'您好，您的验证码是：{captcha}。有效时间5分钟。'
        
        # 构造邮件
        msg = MIMEText(contents, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = config['email']['user']
        msg['To'] = email

        # 发送
        host = config['email'].get('host', 'smtp.qq.com')
        port = config['email'].get('port', 465)
        
        server = smtplib.SMTP_SSL(host, port)
        server.login(config['email']['user'], config['email']['password'])
        server.sendmail(config['email']['user'], [email], msg.as_string())
        server.quit()
        
        return True
    except Exception as e:
        print(f"验证码发送error:{e}")
        return False
