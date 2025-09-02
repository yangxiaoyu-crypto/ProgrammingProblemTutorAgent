import uuid
import re
from coper.LLM import LLM
from coper.basic_ops import Mul
from core.Context import Context
from coper.Service import Service
import logging
log_filename = f"judge_error_type.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)
SUBMISSION_LANGUAGE = "C++14"
def generate_possible_errors(problem_desc, model_name: str) -> str:
    """
    生成针对特定题目可能出现的错误类型和具体描述。
    
    :param problem_description: 题目描述（简化或完整描述）
    :param model_name: 使用的LLM模型名称
    :return: 错误描述的Markdown文本
    """
    logging.info("🔍 LLM: 正在生成潜在错误分析...")
    
    # 构建提示词
    prompt = f"""
[SYSTEM]
你是一位经验丰富的竞赛编程教练，请分析给定编程问题，指出解题者可能犯的常见错误类型及具体原因。

[问题描述]
{problem_desc}

[任务]
1. 分析题目中的难点和陷阱
2. 分类列出可能的错误类型（概念性错误/实现性错误）
3. 为每种错误类型提供：
   a) 错误代码片段示例（伪代码或语言无关）
   b) 错误原因解释
   c) 避免该错误的建议

[输出格式]
请以Markdown格式组织内容，包含以下部分：
1. **主要难点与陷阱**
2. **实现性错误**
   - 错误1描述
     - 示例代码
     - 原因分析
     - 避免建议
"""

    try:
        llm = LLM(model_name)
        response = llm(prompt).result()
        content = response.get("content", "")
        logging.debug(f"LLM 潜在错误分析响应:\n{content}")

        # 格式化输出结果
        errors_content = content.strip()
        if not errors_content.startswith("#"):
            errors_content = f"# 潜在错误分析\n\n{errors_content}"

        logging.info("✅ 潜在错误分析生成成功！")
        return errors_content

    except Exception as e:
        logging.error(f"❌ 生成潜在错误分析失败: {e}")
        logging.error(traceback.format_exc())
        return "# 潜在错误分析\n\n生成失败，请手动分析题目难点和常见错误。"