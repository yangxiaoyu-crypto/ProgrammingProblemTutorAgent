#!/usr/bin/env python3
"""
启动前端开发服务器的脚本
"""

import os
import sys
import subprocess
import json

def check_node():
    """检查Node.js是否安装"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js 版本: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js 未安装，请先安装 Node.js")
    return False

def check_npm():
    """检查npm是否安装"""
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm 版本: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ npm 未安装")
    return False

def install_dependencies():
    """安装前端依赖"""
    print("📦 安装前端依赖...")
    try:
        os.chdir("frontend")
        subprocess.run(["npm", "install"], check=True)
        print("✅ 前端依赖安装完成")
        os.chdir("..")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        os.chdir("..")
        return False

def create_env_file():
    """创建前端环境变量文件"""
    env_content = """# 前端环境变量配置
VITE_APP_NAME=SDU AI Code Analysis
VITE_DEFAULT_MODEL_PROVIDER=vllm
VITE_SDU_BASE_URL=http://10.2.8.77:3000/v1
VITE_VLLM_BASE_URL=http://10.102.32.223:8000/v1
VITE_EMBEDDING_BASE_URL=http://10.2.8.77:3000/v1/embeddings
VITE_API_GATEWAY_URL=http://10.102.32.223:8080
VITE_ENABLE_DEV_PROXY=true
"""
    
    frontend_env_path = "frontend/.env"
    if not os.path.exists(frontend_env_path):
        with open(frontend_env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print(f"✅ 创建前端环境变量文件: {frontend_env_path}")
    else:
        print(f"✅ 前端环境变量文件已存在: {frontend_env_path}")

def start_frontend():
    """启动前端开发服务器"""
    print("🚀 启动前端开发服务器...")
    try:
        os.chdir("frontend")
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 前端开发服务器已停止")
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")
    finally:
        os.chdir("..")

def main():
    print("🎯 SDU AI Code Analysis - 前端启动脚本")
    print("=" * 50)
    
    # 检查Node.js和npm
    if not check_node() or not check_npm():
        return
    
    # 创建环境变量文件
    create_env_file()
    
    # 安装依赖
    if not install_dependencies():
        return
    
    # 启动前端
    start_frontend()

if __name__ == "__main__":
    main()
