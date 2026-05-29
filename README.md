# PySide6 / PyQt6 现代登录系统

一个美观、稳健且高可扩展的 PySide6/PyQt6 登录系统模板。支持本地数据库、动态多媒体背景轮播，并可无缝接入你自己的应用主界面。

## ✨ 核心特性

- **🚀 开箱即用**：默认采用完全本地化运行！移除了对 MySQL 和 Redis 的强依赖，内置 SQLite (`local_data.db`) 和本地缓存 `LocalCache`，首次运行自动建表。
- **🎨 动态多媒体背景**：登录界面支持自定义图片、GIF 动图以及 MP4 视频的自动轮番展示。
- **🛡️ 稳定无闪退**：彻底修复了 Windows D3D11 媒体切换报错与 PyQt 的底层 C++ 内存泄漏问题。
- **📧 邮件验证码**：采用 Python 原生 `smtplib` 重构邮件发送内核，支持安全获取验证码与找回密码。
- **🔌 模块化接入**：支持以插件形式，极速绑定任何自定义的主界面 GUI 项目。

---

## 🛠️ 环境配置与安装

**1. 安装依赖**
```bash
pip install -r requirements.txt
```
*(注：如果您想使用自带的 `Excel_Main_GUI` 示例，还需额外安装 pandas: `pip install pandas`)*

**2. 核心配置**
请优先修改项目根目录的 `config.py` 或外部的 `config.json` 文件：
- **必填项**：发件邮箱账号、邮箱授权码（用于发送验证码）。
- **可选项**：你可以随时通过修改配置开关，无缝切换回 MySQL / Redis 生产环境模式。

---

## 🚀 启动与打包

### 运行程序
**Windows:**
```bash
python login_system.py
```

**MacOS / Linux:**
```bash
python3 login_system.py
```

### 📦 软件打包 (PyInstaller)
推荐直接使用命令行进行打包（已屏蔽各类运行报错及依赖提示）：
```bash
pyinstaller -D -w -i app/images/ico/cactus.ico login_system.py
```
> *(你也可以使用 `auto-py-to-exe` 工具进行可视化的图形打包。)*

---

## 🖼️ 界面展示

### 1. 登录界面（媒体轮播）
登录界面的背景可通过放置文件在 `app/images` 目录下，实现图片、动态图、视频的自动轮番展示。
![图片描述](app/images/logout/20240621233518.png)
![图片描述](app/images/logout/20240621233347.png)

### 2. 示例项目主界面
![图片描述](app/images/logout/20240621233235.png)

---

## 📂 项目结构

```text
PySide6_Login_System/
├── app/                  # 登录系统核心引擎
│   ├── UI_all/           # Qt Designer 导出的 .ui 源码文件
│   ├── handlers/         # 登录、注册、修改密码的逻辑控制器
│   ├── images/           # 登录界面多媒体资源库（可自定义添加素材）
│   ├── models/           # SQLAlchemy 数据模型（自动映射数据库表）
│   └── utls/             # 核心工具类（邮件验证、防爬虫抓图、密码 Hash 等）
├── config.py             # 核心全局配置文件
├── login_system.py       # 程序启动入口文件
├── setup.spec            # PyInstaller 打包配置脚本
├── Excel_Main_GUI/       # 示例应用 1：Excel/CSV 文件合并
├── Image_GUI/            # 示例应用 2：随机二次元动漫壁纸获取
└── Modern_GUI/           # 示例应用 3：PyDracula 现代扁平化主界面
```

---

## 🧩 配合自定义 GUI 使用

本项目默认内置了三个示例项目，修改 `login_system.py` 开头的导入代码（第 16~18 行左右）即可轻松切换登录成功后弹出的主窗口：

- **示例项目 1 (Modern_GUI)**: 基于开源项目的现代扁平化 UI。（[原项目地址](https://gitcode.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6/overview)）
- **示例项目 2 (Image_GUI)**: 高质量动漫图片 API 随机获取与展示。
- **示例项目 3 (Excel_Main_GUI)**: Excel 等数据文件的处理程序。

### 💡 如何接入你自己的项目？

1. 将你自己的项目文件夹拷贝到本仓库的同级目录中。
2. 在 `login_system.py` 顶部导入你自己的主窗口类。
3. **重要规范**：你的主窗口类的 `__init__` 必须接收以下两个参数：
   - `parent`: 登录界面的 GUI 实例（必传，用于触发返回登录界面）。
   - `user_info`: 当前登录成功的用户信息字典（包含账号、UID 等）。
4. **注销功能**：请务必在你的主界面中实现 `logout` 按钮功能，并在点击时调用 `self.parent.show()` 唤出原登录页面并 `close()` 自身。否则自动登录后无法注销切换其他账号。

**附：注销 (Logout) 按钮功能实现演示代码块：**
![图片描述](app/images/logout/logout.png)