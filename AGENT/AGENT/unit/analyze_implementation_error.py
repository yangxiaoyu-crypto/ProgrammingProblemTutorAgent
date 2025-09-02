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
def analyze_implementation_error(problem_desc: str, student_code: str, error_analysis: dict,llm_model: str) -> str:
    """
    当 LLM 判断为实现性错误时，使用 LLM 分析具体的实现问题并提供修复建议。
    返回一个包含分析和建议的字符串。
    """
    logging.info("🤖 LLM: 正在分析实现性错误并提供修复建议...")
    prompt_parts = [
        "[SYSTEM]",
        "你是一位顶级的竞赛编程导师。学生的代码因实现性错误而被判错误，但其核心逻辑是健全的。",
        "你的任务是精确地指出代码中存在错误的具体实现细节，并提供清晰、可操作的修复建议。",
        "",
        "[问题陈述]",
        problem_desc,
        "",
        "[学生代码]",
        f"```{SUBMISSION_LANGUAGE.lower()}\n{student_code}\n```",
        "",
        "[LLM 对实现性错误的分析]",
        f"LLM 先前已将错误类型判断为实现性，原因为：{error_analysis.get('reasoning', '未提供原因。')}",
        "",
        "[任务]",
        "1. 结合问题陈述和已识别的实现性错误，仔细检查学生代码。",
        "2. 找出包含 Bug 的确切代码行或代码段。",
        "3. 解释为什么它错了。",
        "4. 提供修正后的代码片段或清晰的修复说明。",
        "5. 如果存在多个问题或细微之处，请一并说明。",
        "",
        "[输出格式]",
        "实现错误分析:",
        "<对错误的详细分析>",
        "",
        "建议修复:",
        "<修正后的代码片段或具体说明>"
    ]

    prompt = "\n".join(prompt_parts)

    try:
        llm = LLM(model=llm_model)
        response = llm(prompt).result()
        content = response.get("content", "")
        
        logging.debug(f"LLM 实现错误分析响应:\n{content}")
        
        # 提取分析和修复建议
        analysis_match = re.search(r"实现错误分析:\s*\n?(.*?)建议修复:", content, re.DOTALL | re.IGNORECASE)
        fix_match = re.search(r"建议修复:\s*\n?(.*)", content, re.DOTALL | re.IGNORECASE)
        
        analysis = analysis_match.group(1).strip() if analysis_match else "LLM 未提供具体分析。"
        fix = fix_match.group(1).strip() if fix_match else "LLM 未提供具体修复建议。"
        
        result_text = f"实现错误分析:\n{analysis}\n\n建议修复:\n{fix}"
        logging.info(result_text)
        return {
            "error_type": "implementation",
            "reasoning": error_analysis.get('reasoning', '未提供原因。'),  # 保留原始错误判断的原因
            "implementation_analysis": analysis,
            "fix_suggestions": fix
        }

    except Exception as e:
        logging.error(f"❌ 使用 LLM 分析实现错误时出错: {e}")
        logging.error(traceback.format_exc())
        return f"LLM 在分析实现错误时出错: {e}"