# TestData-Tool-Web
This tool could excute renaming to both the folder and files, and replace any values in test data files.
mywebapp/
├── app.py              # Flask 主程序
├── templates/
│   └── index.html      # 网页界面
└── static/
    └── style.css       # 样式表

    5. 运行与部署
本地运行：​

bash
pip install flask python-dotenv
export FLASK_APP=app.py
flask run
生产环境部署：​

​使用 Gunicorn：​
bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
​Docker 部署：​
dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]


my-webapp/          ← 项目根目录
├── app.py           # 主程序文件
├── requirements.txt # Python依赖列表
├── Dockerfile       ← 在这里创建（重点）
├── templates/       # 网页模板
│   └── index.html
└── static/
    └── style.css

    创建方法
方式一：通过 VS Code

在 VS Code 中打开项目文件夹
右键点击项目根目录空白处
选择 "New File"
输入文件名 Dockerfile（注意大小写敏感）
输入以下内容：
dockerfile
# 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制全部项目文件
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]


方法二：使用 WSL（推荐）​
安装 WSL
在 WSL 终端中执行：
bash
cd /mnt/c/Users/lijun/OneDrive/Documents/GitHub/TestData-Tool-Web
docker run --rm -i hadolint/hadolint < Dockerfile

