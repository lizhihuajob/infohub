# Vue 前端 Dockerfile
# 基于 Node.js 18 LTS 官方镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 安装系统依赖（git 用于某些 npm 包）
RUN apk add --no-cache git

# 使用国内 npm 镜像源，加快依赖安装速度
RUN npm config set registry https://registry.npmmirror.com

# 复制 package.json 和 package-lock.json（如果存在）
# 先复制这些文件可以利用 Docker 缓存层，避免每次代码变更都重新安装依赖
COPY package*.json ./

# 安装项目依赖
RUN npm install

# 复制项目代码（开发环境下会被 volume 覆盖）
COPY . .

# 暴露 Vite 开发服务器端口
EXPOSE 5173

# 默认启动命令（可在 docker-compose.yml 中覆盖）
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
