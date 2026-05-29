from PySide6.QtWidgets import QWidget
from Image_GUI.UI.Ui_mainwindow import Ui_Form as ui_mainwindow
from PySide6.QtCore import QSize, QThread, Signal
from PySide6.QtGui import QPixmap, QImage
import requests
# 换成高质量二次元图片 API（直接返回图片链接，不拦截 Python）
image_url = "https://t.alcy.cc/pc/"

class MyMainpage(QWidget):

    def __init__(self, parent=None, user_inof=dict):
        super().__init__()
        self.parent = parent
        self.user_inof = user_inof
        self.mainwindow = ui_mainwindow()
        self.mainwindow.setupUi(self)
        self.setMinimumSize(QSize(560, 490))
        self.setMaximumSize(QSize(560, 490))

        # 返回登陆
        self.mainwindow.pushButton_re_login.clicked.connect(self.re_login)

        self.mainwindow.pushButton_random.clicked.connect(self.random_image)
        self.random_image()

    def random_image(self):
        self.getimage = GetImage()
        self.getimage.signal_image.connect(self.on_image_ready)
        self.getimage.start()

    def on_image_ready(self, bytes_data):
        self.show()
        if not bytes_data:
            return
            
        # 图片请求完成后，将图片二进制数据转换为QImage
        image = QImage.fromData(bytes_data)
        
        # 必须判断图片是否损坏或为空，否则 PySide6 解析空图片会导致底层 C++ 闪退
        if not image.isNull():
            pixmap = QPixmap.fromImage(image)
            self.mainwindow.label.setPixmap(pixmap)
            self.mainwindow.label.setScaledContents(True)
        else:
            print("下载的数据无法被解析为图片（可能是格式不支持或网络返回错误）")

    def re_login(self):
        self.close()
        self.parent.show()


class GetImage(QThread):
    # 信号传递图片的二进制字节流
    signal_image = Signal(bytes)
    
    session = requests.Session()
    # 终极浏览器特征伪装：添加目前最新的 Chrome 124 的所有特征头
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://img.8845.top/',
        'Origin': 'https://img.8845.top',
        'Connection': 'keep-alive',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    })

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            # 1. 尝试获取图片的下载链接 (alcy.cc 会返回 302 跳转)
            res = self.session.get(image_url, allow_redirects=False, timeout=5)
            img_link = res.headers.get("Location")
            
            if img_link:
                print(f'URL获取成功, url:{img_link}')
                
                # 2. 直接使用 requests 下载图片文件本身
                img_res = self.session.get(img_link, timeout=10)
                if img_res.status_code == 200:
                    self.signal_image.emit(img_res.content)
                else:
                    print(f"下载图片失败，状态码: {img_res.status_code}")
                    self.signal_image.emit(b"")
            else:
                print(f"获取链接失败，未找到 Location 重定向: {res.status_code}")
                self.signal_image.emit(b"")
        except Exception as e:
            print(f"网络请求报错: {e}")
            self.signal_image.emit(b"")

