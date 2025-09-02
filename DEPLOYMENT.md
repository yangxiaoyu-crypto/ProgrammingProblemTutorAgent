# SDU AI Code Analysis 部署指南

## 项目概述

这是一个基于AI的代码分析系统，提供三大核心功能：
1. **通用代码检查** - 检查代码错误和优化建议
2. **题目深度分析** - 分析题目并生成测试用例
3. **代码深度分析** - 分析学生代码的错误类型

## 系统架构

- **后端**: 基于RabbitMQ消息队列的微服务架构
- **API网关**: FastAPI提供HTTP接口
- **前端**: React + TypeScript + Vite
- **基础设施**: Docker (MySQL, Redis, RabbitMQ, Minio, Milvus)

## 服务器信息

- **服务器IP**: 10.102.32.223
- **用户名**: yxy
- **密码**: Lib[61-MKNGdimRy

## 部署步骤

### 1. 连接服务器并准备环境

```bash
# 连接服务器
ssh yxy@10.102.32.223

# 进入项目目录
cd /path/to/PROJECT  # 请替换为实际项目路径

# 确保Python环境
python3 --version
pip3 --version
```

### 2. 配置环境变量

确保以下环境变量文件存在并配置正确：

**根目录 `.env` 文件：**
```env
ANTHROPIC_API_KEY="fd065221-62ce-44cc-a0df-e20f6571bc55"
SDU_API_KEY="sk-cPbl4W5omBMZM0wADfFdEeCd5a7c4fD492D88dDb21Ac8e9e"
SDU_BASE_URL="http://10.2.8.77:3000/v1"
VLLM_API_KEY="empty"
VLLM_BASE_URL="http://10.102.32.223:8000/v1/"
EMBEDDING_URL="http://10.2.8.77:3000/v1/embeddings"
EMBEDDING_API_KEY="sk-cPbl4W5omBMZM0wADfFdEeCd5a7c4fD492D88dDb21Ac8e9e"
EMBEDDING_MODEL="embeddings"
MINIMAX_GROUP_ID="1941056464013500830"
MINIMAX_API_KEY="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiLlrZnnv4rovakiLCJVc2VyTmFtZSI6IuWtmee_iui9qSIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxOTQxMDU2NDY0MDIxODg5NDM4IiwiUGhvbmUiOiIxNTY4NDM3NTM5MCIsIkdyb3VwSUQiOiIxOTQxMDU2NDY0MDEzNTAwODMwIiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjUtMDctMDUgMjE6NTQ6MTciLCJUb2tlblR5cGUiOjEsImlzcyI6Im1pbmltYXgifQ.IqQ0rlIk33AceAjY1W7tOtgbZ9dDlEYq1Z3FQWGtFvcF86tX7tOpFG6JGWr0TGRoNuy1CLQqdZV3QcZ5BYLbp-igK4wRSWJRF-wY6ruRmHIWq79WMpb2NVNL6JI6BOnfSpIYAmlUgMflqIuK1VWKrT2A4srj27wIya5X8xfkWiWTQHg_oA6Zi99pvCFnZK9rOYMxe6yQ-JUbYccGx2xacWkrYvhHz4a1Lo0bTBXm_Jbuc1IKxDRFKvqVngV-qRDTAdvXvM38729Zb5bTBRGp4vJqCy1Q8x7zx7BBwR2fZxKdCyKcCPk_7FHexW5U_Etx0QP8I85bVuIma_VuNlZV6g"
VOLCENGINE_API_KEY="fd065221-62ce-44cc-a0df-e20f6571bc55"
```

**middleware/.env 文件：**
```env
HEADER_ADDRESS="10.102.34.150"
MYSQL_PORT="13306"
MYSQL_ROOT_PASSWORD="a1gen3t_M30ysql_p6assword"
REDIS_PORT="16379"
REDIS_PASSWORD="7dDNyObd0TVEbCqz8XTdGOhYJlB3RvdpHw7P2z9eOA"
RABBITMQ_PORT="15672"
RABBITMQ_WEB_PORT="25672"
RABBITMQ_USER="user"
RABBITMQ_PASSWORD="IAAKPTum9LueHQ9OBNr4JaFPptL7YIaitvkx35LeMw"
MINIO_API_PORT="19000"
MINIO_CONSOLE_PORT="19001"
MINIO_ROOT_USER="minio"
MINIO_ROOT_PASSWORD="nQuvqL4lWopVBDo5Slr57J0aWsOVV2omPgY8Ob+Ickk"
MILVUS_PORT="19530"
MILVUS_MONITORING_PORT="19091"
```

### 3. 安装依赖

```bash
# 安装Python依赖
pip3 install -r requirements.txt

# 安装Node.js (如果未安装)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装前端依赖
cd frontend
npm install
cd ..
```

### 4. 启动服务

#### 方法1: 使用启动脚本（推荐）

```bash
# 启动API网关和中间件
python3 start_api_gateway.py

# 在另一个终端启动前端
python3 start_frontend.py
```

#### 方法2: 手动启动

```bash
# 1. 启动中间件服务
cd middleware
docker-compose up -d
cd ..

# 2. 启动API网关
python3 -m uvicorn api_gateway:app --host 0.0.0.0 --port 8080 --reload

# 3. 在另一个终端启动前端
cd frontend
npm run dev
```

### 5. 访问应用

- **前端界面**: http://10.102.32.223:5173
- **API网关**: http://10.102.32.223:8080
- **API文档**: http://10.102.32.223:8080/docs

## 功能说明

### 1. 通用代码检查
- 输入代码，选择编程语言和分析模型
- 系统会检查代码中的潜在错误和优化建议

### 2. 题目深度分析
- 输入题目描述
- 系统会生成简化的数学形式描述
- 生成边缘测试用例
- 分析可能的错误类型

### 3. 代码深度分析
- 输入学生代码和题目描述
- 分析代码的错误类型（概念性错误/实现性错误）
- 提供反例和修复建议

## 故障排除

### 常见问题

1. **API网关启动失败**
   - 检查端口8080是否被占用: `netstat -tlnp | grep 8080`
   - 检查Python依赖是否安装完整

2. **前端无法连接后端**
   - 检查API网关是否正常运行
   - 检查防火墙设置
   - 确认前端配置中的API地址正确

3. **中间件服务启动失败**
   - 检查Docker是否正常运行: `docker --version`
   - 检查端口是否冲突
   - 查看Docker日志: `docker-compose logs`

### 日志查看

```bash
# 查看API网关日志
tail -f api_gateway.log

# 查看中间件日志
cd middleware
docker-compose logs -f

# 查看前端开发服务器日志
cd frontend
npm run dev
```

## 开发说明

### 添加新功能

1. 在后端添加新的处理函数
2. 在`api_gateway.py`中添加对应的HTTP接口
3. 在前端创建新的页面组件
4. 更新路由配置

### 修改样式

前端样式文件位于 `frontend/src/App.css`，可以根据需要调整界面样式。

## 注意事项

1. 确保所有环境变量文件配置正确
2. 中间件服务需要先启动，再启动API网关
3. 生产环境部署时，建议使用nginx作为反向代理
4. 定期备份数据库和配置文件
