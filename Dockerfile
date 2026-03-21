# 使用Python 3.12作为基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖（包括curl用于健康检查）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    psmisc \
    && rm -rf /var/lib/apt/lists/*

# 使用清华源安装Python依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制项目文件
COPY . /app/

# 暴露端口
EXPOSE 8000

# 默认启动命令（会被docker-compose覆盖）
CMD ["sh", "-c", "chmod +x /app/init.sh && /app/init.sh"]
