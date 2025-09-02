# SDU AI Code Analysis System

基于AI的智能代码分析系统，提供代码检查、题目分析和学生代码诊断功能。

## 🚀 快速启动

### 服务器部署 (10.102.32.223)

```bash
# 1. 连接服务器
ssh yxy@10.102.32.223

# 2. 启动后端API网关
python3 start_api_gateway.py

# 3. 启动前端（新终端）
python3 start_frontend.py
```

### 访问地址
- **前端界面**: http://10.102.32.223:5173
- **API文档**: http://10.102.32.223:8080/docs

## 🎯 核心功能

### 1. 通用代码检查
- 检查代码中的潜在错误
- 提供代码优化建议
- 支持多种编程语言

### 2. 题目深度分析
- 生成简化的数学形式题目描述
- 自动生成边缘测试用例
- 分析可能的错误类型

### 3. 代码深度分析
- 判断学生代码的错误类型（概念性/实现性）
- 生成反例测试用例
- 提供针对性的修复建议

详细使用说明请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)

## Configuration

### Environment Files Setup

There are two types of environment configuration files:

1. **Middleware Environment** (`middleware/.env`): Docker deployment configuration for infrastructure services
2. **Runtime Environment** (`.env`): Agent runtime configuration including API keys and service endpoints

#### Setup Steps:

```bash
# Copy environment templates
cp .env.example .env
cp middleware/.env.example middleware/.env
```

Fill in your own parameters in the copied files according to your deployment needs.

### Middleware Configuration (Docker Services)

Configure infrastructure services in `middleware/.env`:

```
# Database and Cache
MYSQL_PORT=13306
MYSQL_ROOT_PASSWORD=<your-mysql-password>
REDIS_PORT=16379
REDIS_PASSWORD=<your-redis-password>

# Message Queue
RABBITMQ_PORT=15672
RABBITMQ_WEB_PORT=25672
RABBITMQ_USER=<your-rabbitmq-user>
RABBITMQ_PASSWORD=<your-rabbitmq-password>

# Object Storage
MINIO_API_PORT=19000
MINIO_CONSOLE_PORT=19001
MINIO_ROOT_USER=<your-minio-user>
MINIO_ROOT_PASSWORD=<your-minio-password>

# Vector Database
MILVUS_PORT=19530
MILVUS_MONITORING_PORT=19091
```

### Runtime Configuration (Agent Services)

Configure agent runtime parameters in `.env`:

```
# LLM API Keys
OPENAI_API_KEY=<your-openai-key>
ANTHROPIC_API_KEY=<your-anthropic-key>
AZURE_OPENAI_API_KEY=<your-azure-key>

# Custom LLM Service
SDU_API_KEY=<your-custom-llm-key>
SDU_BASE_URL=<your-custom-llm-endpoint>

# Embedding Service
EMBEDDING_URL=<your-embedding-endpoint>
EMBEDDING_API_KEY=<your-embedding-key>
EMBEDDING_MODEL=<your-embedding-model>
```

Minio operators are available for writing, reading and deleting objects.