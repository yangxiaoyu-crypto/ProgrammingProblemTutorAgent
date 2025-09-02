#!/bin/bash

echo "========================================"
echo "SDU AI Code Analysis - 停止服务脚本"
echo "========================================"

# 停止API网关
echo "停止API网关服务..."
pkill -f "uvicorn api_gateway:app"

# 停止前端开发服务器
echo "停止前端开发服务器..."
pkill -f "npm run dev"

# 停止中间件服务
echo "停止中间件服务..."
cd middleware
docker-compose down
cd ..

echo "✅ 所有服务已停止"
