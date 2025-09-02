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
def extract_solution_from_code(code: str, problem_desc: str) -> dict:
    """
    从学生代码中提取解法描述
    返回格式: {"description": "解法描述", "code": "代码"}
    """
    prompt = f"""
[任务]
你是一个解法提取器，请从学生代码中提取解法描述。

[输入]
1. 问题描述:
{problem_desc}

2. 学生代码:
```{SUBMISSION_LANGUAGE.lower()}
{code}
[要求]

提取解法的核心思路，包括使用的算法、数据结构、优化技巧等
描述时间复杂度和空间复杂度
语言简洁，不超过200字
不要包含代码本身
[输出格式]
解法描述: <描述文本>
"""
    try:  
        llm = LLM(model="deepseek-chat",
        custom_provider="DEEPSEEK"
        )
        response = llm(prompt=prompt).result()
        content = response.get("content", "")
    
    # 提取解法描述
        description = re.search(r'解法描述:\s*(.*)', content, re.DOTALL)
        if description:
            return {
            "description": description.group(1).strip(),
            "code": code
        }
        return {"description": "未提取到解法描述", "code": code}
    except Exception as e:
        logging.error(f"❌ 提取解法失败: {e}")
        return {"description": "解法提取失败", "code": code}  # 确保返回字典
