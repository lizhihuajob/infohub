# Django 后端 Dockerfile
# 基于 Python 3.11 官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
# PYTHONDONTWRITEBYTECODE: 防止 Python 生成 .pyc 文件
# PYTHONUNBUFFERED: 确保 Python 输出直接显示，不缓冲
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 使用国内清华 apt 源，加快系统依赖安装速度
RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list

# 安装系统依赖
# gcc: 编译某些 Python 包所需
# libpq-dev: PostgreSQL 开发库（预留）
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 使用国内清华 pip 源，加快 Python 包安装速度
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制依赖文件并安装 Python 包
# 先复制 requirements.txt 可以利用 Docker 缓存层
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码（开发环境下会被 volume 覆盖）
COPY . .

# 暴露 Django 开发服务器端口
EXPOSE 8000

# 默认启动命令（可在 docker-compose.yml 中覆盖）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
