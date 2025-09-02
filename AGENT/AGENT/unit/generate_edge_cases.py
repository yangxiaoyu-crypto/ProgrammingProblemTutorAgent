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
def generate_edge_cases(problem_desc, model_identifier: str) -> str:
    """
    使用 LLM 根据题目描述生成潜在的边缘测试用例。
    返回格式化的边缘测试用例字符串。
    """
    # import traceback  # 添加必要的导入
    # import logging
    
    logging.info("🧪 LLM: 正在生成边缘测试用例...")

    prompt = f"""
[SYSTEM]
你是一位经验丰富的竞赛编程出题人和测试员。请根据给定的编程问题，生成一组全面的、可能暴露程序潜在缺陷的**边缘测试用例**。

[问题描述]
{problem_desc}

[任务]
1.  仔细分析问题描述中的每一个约束条件（如变量范围、数据类型、特殊关系）。
2.  构思能够触及这些边界或极端情况的输入数据。
3.  对于每个测试用例，提供：
    a.  **输入描述**：具体的输入数据。
    b.  **预期输出**：该输入对应的正确输出。
    c.  **设计理由**：简要说明这个用例测试了什么边界条件或特殊情况。

[输出格式]
请以 Markdown 格式清晰地列出这些边缘用例。
例如：

markdown
边缘测试用例

用例 1: 最小值边界

• 输入:

[具体输入数据]
• 预期输出:

[具体预期输出]
• 设计理由: 测试当变量 X 取其最小允许值 Y 时的情况。

用例 2: 最大值边界

...v   
"""
    try:
        llm = LLM(model_identifier)
        response = llm(prompt).result()
        content = response.get("content", "")
        logging.debug(f"LLM 边缘测试用例生成响应:\n{content}")

        # 简单提取，假设 LLM 直接返回 Markdown
        edge_cases_content = content.strip()
        if not edge_cases_content.startswith("#"):
            edge_cases_content = f"# 边缘测试用例\n\n{edge_cases_content}"

        logging.info("✅ 边缘测试用例生成成功！")
        return edge_cases_content

    except Exception as e:
        logging.error(f"❌ 生成边缘测试用例失败: {e}")
        logging.error(traceback.format_exc())
        return "# 边缘测试用例\n\n生成失败，请手动检查。"
