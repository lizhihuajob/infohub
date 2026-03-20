#!/bin/bash
# =============================================================================
# 个人博客项目启动脚本
# 用于启动 Docker 容器进行开发
# =============================================================================

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   个人博客项目 - Docker 启动脚本      ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误：Docker 未安装${NC}"
    echo "请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误：Docker Compose 未安装${NC}"
    echo "请先安装 Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# 创建数据目录
echo -e "${YELLOW}[1/4] 创建数据目录...${NC}"
mkdir -p data/db
mkdir -p backend/data/media

# 构建并启动容器
echo -e "${YELLOW}[2/4] 构建 Docker 镜像...${NC}"
docker-compose build

# 启动服务
echo -e "${YELLOW}[3/4] 启动服务...${NC}"
docker-compose up -d

# 等待服务启动
echo -e "${YELLOW}[4/4] 等待服务启动...${NC}"
sleep 5

# 检查服务状态
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   服务状态检查                        ${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查后端服务
if curl -s http://localhost:8000/api/blog/stats/ > /dev/null; then
    echo -e "${GREEN}✓ 后端服务运行正常 (http://localhost:8000)${NC}"
else
    echo -e "${YELLOW}⚠ 后端服务可能还在启动中 (http://localhost:8000)${NC}"
fi

# 检查前端服务
if curl -s http://localhost:5173 > /dev/null; then
    echo -e "${GREEN}✓ 前端服务运行正常 (http://localhost:5173)${NC}"
else
    echo -e "${YELLOW}⚠ 前端服务可能还在启动中 (http://localhost:5173)${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   服务访问地址                        ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "  前端页面: http://localhost:5173"
echo "  后端 API: http://localhost:8000"
echo "  管理后台: http://localhost:8000/admin"
echo ""
echo -e "${GREEN}========================================${NC}"
echo ""

# 创建超级用户提示
echo -e "${YELLOW}提示：首次运行需要创建 Django 超级用户${NC}"
echo "运行以下命令创建管理员账号："
echo ""
echo "  docker-compose exec backend python manage.py createsuperuser"
echo ""

# 显示常用命令
echo -e "${GREEN}常用命令：${NC}"
echo ""
echo "  查看日志:    docker-compose logs -f"
echo "  停止服务:    docker-compose down"
echo "  重启服务:    docker-compose restart"
echo "  进入后端:    docker-compose exec backend bash"
echo "  进入前端:    docker-compose exec frontend sh"
echo ""
