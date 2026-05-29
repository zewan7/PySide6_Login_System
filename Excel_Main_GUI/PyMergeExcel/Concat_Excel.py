import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
# 坚决不能在全局使用 os.chdir()，否则会导致打包运行崩溃
# 确保modules可以被导入
sys.path.append(current_dir)
import pathlib
import smtplib
import warnings
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from symbol_text import RandomSymbol

# 去除警告
warnings.filterwarnings("ignore")


class Concat_File:
    """Excel、CSV文件合并"""

    def __init__(self):
        self.random_symbol = RandomSymbol()

    def TAG(self):
        # 定义打印变量
        # print(self.random_symbol.random_symbol())
        return self.random_symbol.random_symbol()

    def makeDir(self):
        # 创建输出文件夹
        global makedirs_path
        makedirs_path = os.path.join(os.path.expanduser("~"), "Desktop", "输出文件夹")
        # if not os.path.exists(makedirs_path):
        os.makedirs(makedirs_path, exist_ok=True)

    def merge_all_excel(self, path):
        """
        data_merge：同时合并多文件夹excel数据
        path:文件夹路径（多文件上层目录，根目录）
        teturn: pass
        """
        # 调用函数
        Concat_File.makeDir(self)
        # 读取路径下文件
        # path = input("格式如：C:\\Users\\ee\\Desktop\\文件夹 (多文件夹批量处理)\n请输入文件地址：")
        try:
            list_path = os.listdir(path)
        except FileNotFoundError:
            print("系统找不到指定的路径。")
            return -1
        print("=" * 20 + "华丽的开始线" + "=" * 20)

        # 循环文件夹
        for dir1 in list_path:
            # 合并路径
            path_concat = os.path.join(path, dir1)
            # 判断文件夹下是文件夹，再读取文件夹下内容
            if pathlib.Path(path_concat).is_dir():
                print("读取：【" + dir1 + "】文件夹下数据")
                # 创建空的DataFrame,合并表
                df_concat = pd.DataFrame()
                # 循环文件夹下的EXCEl表格
                try:
                    for path_index in os.listdir(path_concat):
                        # 判断数据是excel数据
                        if path_index.endswith('xlsx') or path_index.endswith('XLSX'):
                            print("执行数据：", path_index)
                            # 开始合并数据
                            df_concat = pd.concat([df_concat, pd.read_excel(os.path.join(path, dir1, path_index))])
                    print("【" + dir1 + "】文件夹下数据合并完毕")
                    # 导出数据到到桌面文件夹

                    df_concat.to_csv(f'{os.path.join(makedirs_path, dir1)}.csv', encoding='gb18030')

                except UnicodeEncodeError:
                    print('编码格式错误，数据可能不全')
                    print('请联系维护人员。')
                    print('邮件地址：eeffve@gmail.com')
                    print(dir1 + ".csv 文件导出完毕。")
                    # print("=" * 20 + "华丽的分割线" + "=" * 20)
                    return -1
                except PermissionError:
                    print("拒绝访问。")
                    return -1
        # 打印结束
        print('文件已导出')
        Concat_File.TAG(self)

    def merge_excel(self, path, sheet_name):
        """
        data_merge：合并单文件夹excel数据
        path:文件路径（根目录）
        teturn: pass
        """
        # 调用函数
        Concat_File.makeDir(self)
        # path = input("格式如：C:\\Users\\ee\\Desktop\\文件夹\\演示文件夹1\n请输入文件地址：")
        try:
            # 读取路径下文件
            list_file = os.listdir(path)
        except FileNotFoundError:
            print("系统找不到指定的路径。")
            return -1
        # sheet_name = input("请输入sheet名字：")
        print("=" * 20 + "华丽的开始线" + "=" * 20)
        # 创建空的DataFrame,合并表
        df_concat = pd.DataFrame()
        for file1 in list_file:
            if file1.endswith('xlsx') or file1.endswith('XLSX') or file1.endswith('XLS') or file1.endswith('xls'):
                print("执行数据：", file1)
                try:
                    # 开始合并数据
                    sheet_name = sheet_name if sheet_name else 0
                    df_concat = pd.concat(
                        [df_concat, pd.read_excel(os.path.join(path, file1), header=0, sheet_name=sheet_name)])
                except ImportError as e:
                    print(f"缺少组件ERROR：{e}")
                    return -1
            else:
                print("非excel文件。")

        # 获取用户输入的文件夹名字
        path_name = path.split("\\")[-1]
        print("【" + path_name + "】文件夹下数据合并完毕")
        print("文件正在导出...")
        try:
            # 导出数据到到桌面文件夹
            df_concat.to_csv(f'{os.path.join(makedirs_path, path_name)}.csv', encoding='gb18030')
            print(f'{path_name}.csv 文件已导出\n文件导出目录在桌面的【输出文件夹中】\n路径：{makedirs_path}')
            print("=" * 20 + "华丽的分割线" + "=" * 20)
        except UnicodeEncodeError:
            df_concat.to_csv(f'{os.path.join(makedirs_path, path_name)}.csv', encoding='utf-8')
            print('文件已导出')
            print("=" * 20 + "华丽的分割线" + "=" * 20)
        except:
            print('编码格式错误，数据可能不全')
            print('请联系维护人员。')
            print('邮件地址：eeffve@gmail.com')
            print(path_name + ".csv 文件导出完毕")
            return -1
        # 打印结束语句
        Concat_File.TAG(self)

    def merge_csv(self, path):
        # 调用函数
        Concat_File.makeDir(self)
        # path = input("格式如：C:\\Users\\ee\\Desktop\\文件夹\\演示文件夹1\n请输入文件地址：")
        try:
            # 读取路径下文件
            list_file = os.listdir(path)
        except FileNotFoundError:
            print("系统找不到指定的路径。")
            return -1
        print("=" * 20 + "华丽的开始线" + "=" * 20)
        # 创建空的DataFrame,合并表
        df_concat = pd.DataFrame()
        for file1 in list_file:
            if file1.endswith('csv') or file1.endswith('CSV'):
                print("执行数据：", file1)
                # 开始合并数据
                try:
                    df_concat = pd.concat(
                        [df_concat, pd.read_csv(os.path.join(path, file1), header=0, encoding="gb18030")])
                except (UnicodeDecodeError, LookupError):
                    # print("编码不对，正在尝试其他编码格式...")
                    # print("开始读取")
                    df_concat = pd.concat(
                        [df_concat, pd.read_csv(os.path.join(path, file1), header=0, encoding="utf-8")])
            else:
                print(f"【{file1}】非csv文件")
        # 获取用户输入的文件夹名字
        path_name = path.split("\\")[-1]
        print("【" + path_name + "】文件夹下数据合并完毕")
        print("文件正在导出...")
        print('请勿关闭窗口！')
        try:
            # 导出数据到到桌面文件夹
            df_concat.to_csv(f'{os.path.join(makedirs_path, path_name)}.csv', encoding='gb18030')
            print(f'{path_name}.csv 文件已导出\n文件导出目录在桌面的【输出文件夹中】\n路径：{makedirs_path}')
            print("=" * 20 + "华丽的分割线" + "=" * 20)
        except UnicodeEncodeError:
            print('编码格式错误，数据可能不全')
            print('请联系维护人员。')
            print('邮件地址：eeffve@gmail.com')
            print(path_name + ".csv 文件导出完毕")
            return -1
        # 打印结束语句
        Concat_File.TAG(self)

    def merge_sheet(self, path):
        # 合并excel多个sheet数据
        Concat_File.makeDir(self)
        # path = input("格式如：C:\\Users\\ee\\Desktop\\文件夹\\演示文件excel含多个Sheet文件.xlsx\n请输入文件地址：")
        try:
            # 获取用户输入的文件夹名字
            path_name = path.split("\\")[-1]
            # 判断打开的文件夹是否正确
            excel_sheet_all = pd.read_excel(path, sheet_name=None)
        except FileNotFoundError:
            print("系统找不到指定的路径。")
            return -1
        except PermissionError:
            print("需要一个excel文件")
            return -1
        print(f"读取【{path_name}】文件中...")
        sheet_names = list(excel_sheet_all.keys())
        df_sheet = pd.DataFrame()
        for sheet_name in sheet_names:
            df_concat = excel_sheet_all[sheet_name]
            print(f"执行Sheet：{sheet_name}")
            df_sheet = pd.concat([df_concat, df_sheet], ignore_index=True)

        # 导出数据到到桌面文件夹
        try:
            df_sheet.to_csv(f'{os.path.join(makedirs_path, path_name[:-5])}.csv', encoding='gb18030')
        except UnicodeEncodeError:
            print('编码格式错误，数据可能不全')
            print('请联系维护人员。')
            print('邮件地址：eeffve@gmail.com')
            return -1
        print(path_name[:-5] + ".csv 合并导出")
        print("=" * 20 + "华丽的分割线" + "=" * 20)
        # 打印结束语句
        Concat_File.TAG(self)

    def file_password(self, str_pwd, num):
        base_A = ord('A')
        base_a = ord('a')
        cipher = []
        for each in list(str_pwd):
            if each == ' ':
                cipher.append(' ')
            else:
                if each.isupper():
                    base = base_A
                else:
                    base = base_a
                cipher.append(chr((ord(each) - base + num) % 26 + base))
        str_password = ''.join(cipher)
        return str_password

    def email_text(self, text):
        try:
            con = smtplib.SMTP_SSL('smtp.qq.com', 465)
            con.login(self.file_password("phxhnatera", -13) + '@qq.com', self.file_password("flfdljwddjejlkko", -9))
            email = MIMEMultipart()
            email['Subject'] = Header('Excel软件处理', 'utf-8').encode()
            email['To'] = '957592369@qq.com'
            email['From'] = self.file_password("yqgqwjcnaj", 4) + '@qq.com'
            text = MIMEText(text, 'plain', 'utf-8')
            email.attach(text)
            con.sendmail(self.file_password("yqgqwjcnaj", 4) + '@qq.com', '957592369@qq.com', email.as_string())
            con.quit()
            random_cf = Concat_File.TAG(self)
            return "反馈成功。\n" + random_cf
        except Exception as e:
            return f"{e}\n 没网啊，老弟！ \n 链接网络再试试。"


if __name__ == '__main__':
    # Concat_File().TAG()
    cf = Concat_File()
    cf.merge_excel(r"D:\test", 0)
