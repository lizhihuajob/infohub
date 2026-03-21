# 使用Python 3.12作为基础镜像
FROM python:3.12-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 使用清华源安装Python依赖
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 复制项目文件
COPY . /app/

# 创建必要的目录
RUN mkdir -p /app/data /app/staticfiles /app/media && \
    chmod +x /app/init.sh

# 初始化数据库（在构建时创建，避免挂载卷的锁问题）
RUN python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    mkdir -p /app/data_initial && \
    cp /app/data/db.sqlite3 /app/data_initial/

# 暴露端口
EXPOSE 8000

# 启动命令（通过docker-compose command覆盖）
CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0:8000", "myblog.wsgi:application"]
