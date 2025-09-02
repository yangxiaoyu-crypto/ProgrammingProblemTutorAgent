@echo off
echo ========================================
echo SDU AI Code Analysis - 服务启动脚本
echo ========================================

echo.
echo 1. 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: Python未安装或未添加到PATH
    pause
    exit /b 1
)

echo.
echo 2. 安装Python依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 错误: Python依赖安装失败
    pause
    exit /b 1
)

echo.
echo 3. 启动中间件服务...
cd middleware
docker-compose up -d
if %errorlevel% neq 0 (
    echo 错误: 中间件服务启动失败，请检查Docker环境
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo 4. 等待中间件服务启动...
timeout /t 10 /nobreak

echo.
echo 5. 启动API网关...
echo 正在启动API网关服务器 (端口8080)...
start "API Gateway" python -m uvicorn api_gateway:app --host 0.0.0.0 --port 8080 --reload

echo.
echo 6. 等待API网关启动...
timeout /t 5 /nobreak

echo.
echo 7. 检查Node.js环境...
node --version
if %errorlevel% neq 0 (
    echo 错误: Node.js未安装
    pause
    exit /b 1
)

echo.
echo 8. 安装前端依赖...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo 错误: 前端依赖安装失败
    cd ..
    pause
    exit /b 1
)

echo.
echo 9. 启动前端开发服务器...
echo 正在启动前端服务器 (端口5173)...
start "Frontend Dev Server" npm run dev
cd ..

echo.
echo ========================================
echo 🎉 所有服务启动完成！
echo ========================================
echo.
echo 访问地址:
echo - 前端界面: http://localhost:5173
echo - API文档: http://localhost:8080/docs
echo.
echo 按任意键退出...
pause
