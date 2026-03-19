#!/bin/bash
# 启动开发环境脚本

echo "======================================"
echo "  启动博客项目开发环境"
echo "======================================"

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker未运行，请先启动Docker"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: docker-compose未安装"
    exit 1
fi

echo "正在构建并启动服务..."
docker-compose up --build -d

echo ""
echo "======================================"
echo "  服务启动成功！"
echo "======================================"
echo ""
echo "访问地址:"
echo "  前端页面: http://localhost:3000"
echo "  后端API:  http://localhost:8000/api/"
echo "  管理后台: http://localhost:8000/admin/"
echo ""
echo "常用命令:"
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo ""
