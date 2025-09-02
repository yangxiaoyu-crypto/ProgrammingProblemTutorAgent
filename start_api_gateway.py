#!/usr/bin/env python3
"""
启动API网关服务器的脚本
"""

import os
import sys
import subprocess
import signal
import time

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI 和 Uvicorn 已安装")
    except ImportError:
        print("❌ 缺少依赖，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"], check=True)
        print("✅ 依赖安装完成")

def check_env_files():
    """检查环境变量文件"""
    env_file = ".env"
    middleware_env = "middleware/.env"
    
    if not os.path.exists(env_file):
        print(f"❌ 缺少环境变量文件: {env_file}")
        return False
    
    if not os.path.exists(middleware_env):
        print(f"❌ 缺少环境变量文件: {middleware_env}")
        return False
    
    print("✅ 环境变量文件检查通过")
    return True

def start_middleware():
    """启动中间件服务"""
    print("🚀 启动中间件服务...")
    try:
        os.chdir("middleware")
        result = subprocess.run(["docker-compose", "up", "-d"], 
                              capture_output=True, text=True, check=True)
        print("✅ 中间件服务启动成功")
        os.chdir("..")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 中间件服务启动失败: {e}")
        print(f"错误输出: {e.stderr}")
        os.chdir("..")
        return False

def start_api_gateway():
    """启动API网关"""
    print("🚀 启动API网关服务器...")
    try:
        # 使用uvicorn启动API网关
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api_gateway:app",
            "--host", "0.0.0.0",
            "--port", "8080",
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 API网关服务器已停止")
    except Exception as e:
        print(f"❌ API网关启动失败: {e}")

def main():
    print("🎯 SDU AI Code Analysis - API网关启动脚本")
    print("=" * 50)
    
    # 检查依赖
    check_dependencies()
    
    # 检查环境变量文件
    if not check_env_files():
        print("请确保环境变量文件存在并配置正确")
        return
    
    # 启动中间件服务
    if not start_middleware():
        print("中间件服务启动失败，请检查Docker环境")
        return
    
    # 等待中间件服务启动
    print("⏳ 等待中间件服务启动...")
    time.sleep(10)
    
    # 启动API网关
    start_api_gateway()

if __name__ == "__main__":
    main()
