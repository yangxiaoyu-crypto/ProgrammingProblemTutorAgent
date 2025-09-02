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
def judge_error_type(problem_desc: str, student_code: str,  llm_model: str) -> dict:
    """
    使用 LLM 判断学生的错误是概念性错误还是实现性错误。
    返回格式: {"error_type": "conceptual" 或 "implementation" 或 "unknown", "reasoning": "LLM 的分析", "raw_feedback": "原始评测信息"}
    """
    logging.info("🤖 LLM: 正在分析错误类型（概念性 vs 实现性）...")

    
    # 构建给 LLM 的 Prompt
    prompt = f"""
[SYSTEM]
你是一位顶级的竞赛编程导师。你将分析一个学生提交的、因逻辑错误而判为不正确的代码。
你的任务是根据问题陈述、学生代码和评测反馈，判断错误是源于核心算法/逻辑的缺陷（概念性错误），还是编码实现细节的失误（实现性错误）。

[问题陈述]
{problem_desc}

[学生代码]
```{SUBMISSION_LANGUAGE.lower()}
{student_code}
[任务]
分析学生代码和评测反馈。
判断主要问题是出现在基本方法（例如，选择了错误的算法、逻辑不正确）还是代码的实现方式（例如，越界错误、变量使用不当、导致运行时错误的语法问题，但逻辑本身是健全的）。
提供清晰的分类解释。
[输出格式]
错误类型: <conceptual 或 implementation>
原因分析: <你的详细解释>
"""
    try:
        llm = LLM(model=llm_model)
        response = llm(prompt).result()
        content = response.get("content", "")
        
        logging.debug(f"LLM 错误类型分析响应:\n{content}")
        
        # 提取错误类型和原因
        error_type_match = re.search(r"错误类型:\s*(\w+)", content, re.IGNORECASE)
        reasoning_match = re.search(r"原因分析:\s*(.*)", content, re.DOTALL | re.IGNORECASE)
        
        error_type = "unknown"
        if error_type_match:
            type_str = error_type_match.group(1).lower()
            if type_str == "conceptual":
                error_type = "conceptual"
            elif type_str == "implementation":
                error_type = "implementation"
        
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "LLM 未提供具体原因分析。"
        
        logging.info(f"LLM 错误类型分类: {error_type.upper()}，原因: {reasoning[:100]}...")
        return {
            "error_type": error_type, 
            "reasoning": reasoning
        }
    
    except Exception as e:
        logging.error(f"❌ 使用 LLM 分析错误类型时出错: {e}")
        logging.error(traceback.format_exc())
        return {
            "error_type": "unknown", 
            "reasoning": f"LLM 分析失败: {e}", 
            "raw_feedback": judge_info
        }
