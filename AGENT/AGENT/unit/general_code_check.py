
import re
import logging
from coper.LLM import LLM
from core.Context import Context
import traceback
# 初始化日志
log_filename = "general_code_check.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
SOURE_LANGUAGE = "C++14"
def general_code_check(student_code: str, llm_model: str) -> str:
    """
    使用 LLM 对给定的源代码进行一次通用型检查：
    1. 指出潜在的代码错误（逻辑 / 语法 / 边界 / 资源泄漏等）。
    2. 提出简洁性与可读性方面的优化建议。
    返回一段结构化文本，包含上述两部分内容。
    """
    logging.info("🤖 LLM: 正在执行通用型代码检查...")

    prompt = f"""
[SYSTEM]
你是一位资深代码审计专家。请对以下 {SOURE_LANGUAGE} 代码进行通用型检查，并按照以下要求输出报告：

### 一、审查维度（必须覆盖所有子项）
1. **语法与编译问题**：检查语法错误、未定义行为（如未初始化变量、整数溢出、越界访问）、不符合 C++ 标准的写法（如 C 风格强制转换 vs static_cast）。
2. **逻辑与正确性**：检查循环条件（如边界值是否闭合）、条件判断（如是否遗漏等价情况）、算法逻辑（如计算逻辑是否与需求一致）。
3. **性能与效率**：检查不必要的拷贝（如传值而非传 const 引用）、循环内的冗余操作（如重复计算相同表达式）、资源管理（如文件/内存未及时释放）。
4. **安全性**：检查不安全的输入处理（如未校验 cin 输入有效性）、潜在的内存泄漏（如 new 后未 delete）、危险的函数调用（如 gets()、strcpy() 等已被弃用的函数）。
5. **代码可读性与风格**：检查命名规范（变量/函数名是否符合驼峰式或下划线式）、注释质量（关键逻辑是否有注释）、代码缩进与格式（是否符合 Google C++ 风格指南）。
6. **最佳实践**：检查是否使用现代 C++ 特性（如 auto、范围 for 循环替代传统循环）、是否避免全局变量/using namespace std;、是否合理使用 const 修饰符。

### 二、输出要求
请以 **清晰的自然语言报告** 格式输出结果，要求语言通俗易懂，小白也能看明白，包含以下三部分内容：
格式要求：
1. 每个问题占一行
2. 每行格式固定为：[行号] <error/warning/info> 问题描述 => 修改建议
3. 如果代码没有问题，输出 "代码正常，未发现问题"
每一行回答的格式按照以下要求来做：
# #   1. 🔍 问题现象（如"这里存在内存泄漏"）
# #   2. ❓ 原因与风险（使用初学者易懂的比喻说明，如"这就像水池注水后不关闭水龙头"）
# #   3. ✨ 改进建议（提供具体可操作的修改方案，如"建议在对象析构时调用delete释放资源"）
### 三、输出格式
请按照以下格式输出，请你自己优化输出方式，要求你的输出看起来简洁明了：
## 代码错误检查
<列出所有错误问题，每个问题一行>

## 优化建议
<列出所有优化建议，每个建议一行>

[待检查代码]
{SOURE_LANGUAGE.lower()}

{student_code}
"""

    try:
        llm = LLM(model=llm_model)
        response = llm(prompt).result()
        content = response.get("content", "")

        logging.debug(f"LLM 通用检查结果:\n{content}")
        
        # 直接返回模型生成的报告内容
        # 添加标题前缀
        report = "【通用代码检查报告】\n\n" + content
        
        #logging.info(report)
        return report

    except Exception as e:
        logging.error(f"❌ 通用代码检查时出错: {e}")
        # 使用导入的 traceback 模块记录详细错误信息
        logging.error(traceback.format_exc())
        return f"LLM 在执行通用代码检查时发生异常: {e}"
        