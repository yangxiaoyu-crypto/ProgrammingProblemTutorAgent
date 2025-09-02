# pydantic_models.py

from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TestCase(BaseModel):
    """测试用例数据结构"""
    input_data: str = Field(..., description="测试用例的输入数据。")
    expected_output: str = Field(..., description="对应输入的预期正确输出。")
    description: str = Field(..., description="简要说明该测试用例旨在检查的边界或特定情况。")
    case_type: str = Field(..., description="用例类型，必须是 'basic', 'boundary', 或 'edge' 之一。")

class TestCaseList(BaseModel):
    """A list of test cases."""
    test_cases: List[TestCase] = Field(..., description="包含多个测试用例的列表。")

class SolutionOutput(BaseModel):
    thought: str = Field(..., description="一步步解释代码背后逻辑的思考过程。")
    code: str = Field(..., description="用于解决问题的完整、可运行的源代码。")

class ErrorTypeAnalysisOutput(BaseModel):
    """用于错误类型分析的 Pydantic 模型"""
    error_type: str = Field(..., description="Must be 'conceptual', 'implementation', or 'unknown'.")
    reasoning: str = Field(..., description="A detailed explanation for the classification.")

class CounterExampleOutput(BaseModel):
    """用于生成反例的 Pydantic 模型"""
    input_data: str = Field(..., description="A specific input that demonstrates the conceptual error.")
    expected_output: str = Field(..., description="The correct output for the generated input.")

class ImplementationAnalysisOutput(BaseModel):
    """用于实现性错误分析的 Pydantic 模型"""
    analysis: str = Field(..., description="A detailed analysis of the implementation error.")
    suggestion: str = Field(..., description="A concrete suggestion for fixing the code.")

class SimplifiedProblemOutput(BaseModel):
    """用于简化题面的 Pydantic 模型"""
    simplified_description: str = Field(..., description="The simplified problem description in markdown format.")

class PossibleErrorsOutput(BaseModel):
    """用于预测可能错误的 Pydantic 模型"""
    markdown_content: str = Field(..., description="A markdown text listing potential errors.")

class SolutionDescriptionOutput(BaseModel):
    """用于从代码中提取解法描述的 Pydantic 模型"""
    description: str = Field(..., description="A concise description of the solution's logic and complexity.")