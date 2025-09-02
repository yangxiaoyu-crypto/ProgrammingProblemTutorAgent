"""
HTTP API网关服务器
提供三大功能的HTTP接口：
1. 通用代码检查
2. 题目深度分析  
3. 代码深度分析
"""

import sys
import os
import uuid
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# 添加项目路径
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('./AGENT'))

from core.Context import Context
from AGENT.unit.general_code_check import general_code_check
from AGENT.system.FUNCTION3 import process_student_solution
from AGENT.unit.generate_problem_simplified import generate_problem_simplified
from AGENT.unit.generate_edge_cases import generate_edge_cases
from AGENT.unit.generate_possible_errors import generate_possible_errors
import traceback

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SDU AI Code Analysis API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求模型定义
class CodeCheckRequest(BaseModel):
    code: str
    language: str = "C++14"
    model: str = "deepseek/deepseek-chat"

class ProblemAnalysisRequest(BaseModel):
    problem_code: str
    problem_description: str

class StudentCodeAnalysisRequest(BaseModel):
    problem_id: str
    student_code: str
    problem_description: str
    submission_history: list = []

# 响应模型定义
class CodeCheckResponse(BaseModel):
    status: str
    result: str
    message: Optional[str] = None

class ProblemAnalysisResponse(BaseModel):
    status: str
    result: Dict[str, Any]
    message: Optional[str] = None

class StudentCodeAnalysisResponse(BaseModel):
    status: str
    result: Dict[str, Any]
    message: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "SDU AI Code Analysis API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/code-check", response_model=CodeCheckResponse)
async def code_check(request: CodeCheckRequest):
    """
    通用代码检查接口
    """
    try:
        logger.info(f"收到代码检查请求，代码长度: {len(request.code)}")
        
        with Context(task_id=str(uuid.uuid4().hex)):
            result = general_code_check(request.code, request.model)
            
        return CodeCheckResponse(
            status="success",
            result=result,
            message="代码检查完成"
        )
    except Exception as e:
        logger.error(f"代码检查失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"代码检查失败: {str(e)}")

@app.post("/api/problem-analysis", response_model=ProblemAnalysisResponse)
async def problem_analysis(request: ProblemAnalysisRequest):
    """
    题目深度分析接口
    """
    try:
        logger.info(f"收到题目分析请求，题目代码: {request.problem_code}")

        with Context(task_id=str(uuid.uuid4().hex)):
            # 1. 生成简化的数学形式题目描述
            simplified_desc = generate_problem_simplified(
                request.problem_description,
                "deepseek/deepseek-chat"
            )

            # 2. 生成边缘测试用例
            edge_cases = generate_edge_cases(
                simplified_desc,
                "deepseek/deepseek-chat"
            )

            # 3. 生成可能的错误类型
            possible_errors = generate_possible_errors(
                simplified_desc,
                "deepseek/deepseek-chat"
            )

            result = {
                "problem_code": request.problem_code,
                "simplified_description": simplified_desc,
                "edge_cases": edge_cases,
                "possible_errors": possible_errors,
                "solutions": [],  # 解法生成功能待实现
                "std_code": None  # 标准代码生成功能待实现
            }

        return ProblemAnalysisResponse(
            status="success",
            result=result,
            message="题目分析完成"
        )
    except Exception as e:
        logger.error(f"题目分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"题目分析失败: {str(e)}")

@app.post("/api/student-code-analysis", response_model=StudentCodeAnalysisResponse)
async def student_code_analysis(request: StudentCodeAnalysisRequest):
    """
    学生代码深度分析接口
    """
    try:
        logger.info(f"收到学生代码分析请求，题目ID: {request.problem_id}")
        
        with Context(task_id=str(uuid.uuid4().hex)):
            # 注意：这里需要session参数，但原函数需要requests.Session
            import requests
            session = requests.Session()

            result = process_student_solution(
                problem_id=request.problem_id,
                student_code=request.student_code,
                problem_desc=request.problem_description,
                session=session,
                submission_history=request.submission_history
            )
            
        return StudentCodeAnalysisResponse(
            status="success",
            result=result,
            message="学生代码分析完成"
        )
    except Exception as e:
        logger.error(f"学生代码分析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"学生代码分析失败: {str(e)}")

if __name__ == "__main__":
    # 启动API服务器
    uvicorn.run(
        "api_gateway:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
