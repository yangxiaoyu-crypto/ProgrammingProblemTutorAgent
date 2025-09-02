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
def generate_counter_example(problem_desc: str, student_code: str, error_analysis: dict, llm_model: str) -> str:
    """
    当 LLM 判断为概念性错误时，使用 LLM 生成一个能暴露此概念性错误的测试用例（反例）。
    返回一个包含输入和正确输出的字符串。
    """
    logging.info("🤖 LLM: 正在为概念性错误生成反例...")
    
    # 构建给 LLM 的 Prompt，强调任务和上下文
    prompt = f"""
[SYSTEM]
你是一位顶级的竞赛编程导师。学生的代码因核心逻辑存在概念性缺陷而被判错误。
你的任务是提供一个具体的输入，用以展示这个逻辑缺陷，并给出该输入的正确输出。

[问题陈述]
{problem_desc}

[学生代码]
```{SUBMISSION_LANGUAGE.lower()}
{student_code}
[LLM 对概念性错误的分析]
LLM 先前已将错误类型判断为概念性，原因为：
{error_analysis.get('reasoning', '未提供原因。')}
[任务]
基于问题陈述和已识别出的概念性错误，设计一个特定的输入测试用例。
确定该输入对应的正确输出。
清晰地呈现输入和正确输出。
[输出格式]
输入:
<你生成的输入>
正确输出:
<你生成的输入对应的正确输出>
"""
    try:
        # 调用 LLM 模型
        llm = LLM(model=llm_model)
        response = llm(prompt).result()
        content = response.get("content", "")
        
        logging.debug(f"LLM 反例生成响应:\n{content}")
        
        # 从 LLM 的响应中解析出"输入"和"正确输出"
        # 使用正则表达式匹配指定的输出格式
        input_match = re.search(r"输入:\s*\n?(.*?)正确输出:", content, re.DOTALL | re.IGNORECASE)
        output_match = re.search(r"正确输出:\s*\n?(.*)", content, re.DOTALL | re.IGNORECASE)
        
        generated_input = input_match.group(1).strip() if input_match else "无法生成输入。"
        correct_output = output_match.group(1).strip() if output_match else "无法确定正确输出。"
        
        # 如果无法生成，返回错误信息
        if generated_input == "无法生成输入。":
            return "LLM未能成功生成反例。"
        
        # 格式化反例信息并返回
        counter_example_info = f"LLM 生成的反例:\n输入:\n{generated_input}\n正确输出:\n{correct_output}\n"
        logging.info(counter_example_info)
        return counter_example_info

    except Exception as e:
        logging.error(f"❌ 使用 LLM 生成反例时出错: {e}")
        logging.error(traceback.format_exc())
        return f"LLM 在生成反例时出错: {e}"