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
def generate_problem_simplified(problem_content: str, model_identifier: str) -> str:
    """
    生成简化的数学形式题目描述 (problem_s.md)
    """
    logging.info("📝 开始生成简化数学形式的题目描述...")
    
    # 构建提示词
    prompt = f"""
【角色】
你是一名“极简题面生成器”，只输出数学形式，不讲故事。

【输入】
{problem_content}

【任务】
生成一份“纯技术规格”文档，要求：
1. 删除所有背景、故事、情境、示例解释、提示。
2. 用符号表达：输入集合、输出集合、约束条件、数学关系。
3. 必须包含：
   - 变量名及类型
   - 变量上下界
   - 运算/逻辑关系式
4. 禁止出现：
   - 任何自然语言描述
   - 样例输入/输出
   - 解释性文字

【输出模板】（严格按 Markdown 层级）
```markdown
## 问题定义

### 输入
- 变量：`a`, `b`
- 类型：整数
- 范围：`1 ≤ a, b ≤ 10^9`

### 输出
- 变量：`s`
- 类型：整数

### 关系
- `s = a + b`
请仅填充模板，不要添加额外文字。
"""

    try:
        # 调用大模型生成简化题面
        llm = LLM(model="deepseek-chat",
        custom_provider="DEEPSEEK"
        )
        response = llm(prompt=prompt).result()
        content = response.get("content", "")
        
        # 提取简化题面内容
        simplified_content = content.strip()
        
        # 确保以Markdown格式返回
        if not simplified_content.startswith("#"):
            simplified_content = f"# 题目简化数学形式\n\n{simplified_content}"
        
        logging.info("✅ 简化题面生成成功！")
        return simplified_content
    
    except Exception as e:
        logging.error(f"❌ 生成简化题面失败: {e}")
        logging.error(traceback.format_exc())
        return problem_content  # 失败时返回原始题面