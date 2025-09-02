#!/bin/bash

echo "========================================"
echo "SDU AI Code Analysis - 服务启动脚本"
echo "========================================"

# 检查Python环境
echo
echo "1. 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3未安装"
    exit 1
fi
python3 --version

# 安装Python依赖
echo
echo "2. 安装Python依赖..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: Python依赖安装失败"
    exit 1
fi

# 启动中间件服务
echo
echo "3. 启动中间件服务..."
cd middleware
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "错误: 中间件服务启动失败，请检查Docker环境"
    cd ..
    exit 1
fi
cd ..

# 等待中间件服务启动
echo
echo "4. 等待中间件服务启动..."
sleep 10

# 启动API网关
echo
echo "5. 启动API网关..."
echo "正在启动API网关服务器 (端口8080)..."
nohup python3 -m uvicorn api_gateway:app --host 0.0.0.0 --port 8080 --reload > api_gateway.log 2>&1 &
API_GATEWAY_PID=$!
echo "API网关进程ID: $API_GATEWAY_PID"

# 等待API网关启动
echo
echo "6. 等待API网关启动..."
sleep 5

# 检查Node.js环境
echo
echo "7. 检查Node.js环境..."
if ! command -v node &> /dev/null; then
    echo "错误: Node.js未安装"
    kill $API_GATEWAY_PID
    exit 1
fi
node --version

# 安装前端依赖
echo
echo "8. 安装前端依赖..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "错误: 前端依赖安装失败"
    cd ..
    kill $API_GATEWAY_PID
    exit 1
fi

# 启动前端开发服务器
echo
echo "9. 启动前端开发服务器..."
echo "正在启动前端服务器 (端口5173)..."
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端进程ID: $FRONTEND_PID"
cd ..

echo
echo "========================================"
echo "🎉 所有服务启动完成！"
echo "========================================"
echo
echo "访问地址:"
echo "- 前端界面: http://10.102.32.223:5173"
echo "- API文档: http://10.102.32.223:8080/docs"
echo
echo "进程ID:"
echo "- API网关: $API_GATEWAY_PID"
echo "- 前端: $FRONTEND_PID"
echo
echo "日志文件:"
echo "- API网关: api_gateway.log"
echo "- 前端: frontend.log"
echo
echo "停止服务:"
echo "kill $API_GATEWAY_PID $FRONTEND_PID"
echo
echo "按Ctrl+C退出..."

# 等待用户中断
trap 'echo "正在停止服务..."; kill $API_GATEWAY_PID $FRONTEND_PID; exit' INT
while true; do
    sleep 1
done
