import { useState } from 'react'
import { appConfig } from '../config'

type StudentCodeAnalysisResult = {
	status: string
	result: {
		status: string
		message: string
		analysis?: any
		counter_example?: any
		error_id?: string
		implementation_analysis?: string
		fix_suggestions?: string
	}
	message?: string
}

export function StudentCodeAnalysisPage() {
	const [problemId, setProblemId] = useState('SDUOJ-1001')
	const [problemDescription, setProblemDescription] = useState(`# A+B Problem

## 题目描述
给定两个整数A和B，计算A+B的值。

## 输入格式
一行包含两个整数A和B，用空格分隔。

## 输出格式
输出一个整数，即A+B的值。

## 数据范围
- -10^9 ≤ A, B ≤ 10^9`)
	const [studentCode, setStudentCode] = useState(`#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << a * b << endl;  // 错误：应该是加法而不是乘法
    return 0;
}`)
	const [result, setResult] = useState<StudentCodeAnalysisResult | null>(null)
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)

	async function analyzeStudentCode() {
		if (!studentCode.trim() || !problemDescription.trim()) return
		
		setLoading(true)
		setError(null)
		setResult(null)

		try {
			const apiUrl = appConfig.enableDevProxy ? '/api/student-code-analysis' : `${appConfig.apiGatewayUrl}/api/student-code-analysis`
			const response = await fetch(apiUrl, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					problem_id: problemId,
					student_code: studentCode,
					problem_description: problemDescription,
					submission_history: []
				}),
			})

			if (!response.ok) {
				throw new Error(`HTTP ${response.status}: ${response.statusText}`)
			}

			const data: StudentCodeAnalysisResult = await response.json()
			setResult(data)
		} catch (err) {
			const errorMessage = err instanceof Error ? err.message : '未知错误'
			setError(`代码分析失败: ${errorMessage}`)
		} finally {
			setLoading(false)
		}
	}

	const renderAnalysisResult = () => {
		if (!result) return null

		const analysisResult = result.result

		return (
			<div className="analysis-result">
				<div className="status-badge" style={{
					display: 'inline-block',
					padding: '4px 12px',
					borderRadius: '12px',
					fontSize: '12px',
					fontWeight: 'bold',
					marginBottom: 16,
					backgroundColor: analysisResult.status === 'conceptual_error' ? '#dc3545' : 
									analysisResult.status === 'implementation' ? '#ffc107' : '#28a745',
					color: 'white'
				}}>
					{analysisResult.status === 'conceptual_error' ? '概念性错误' :
					 analysisResult.status === 'implementation' ? '实现性错误' :
					 analysisResult.status === 'exists_in_kb' ? '已知错误' : '其他'}
				</div>

				<div className="message" style={{ marginBottom: 16 }}>
					<strong>分析结果：</strong> {analysisResult.message}
				</div>

				{analysisResult.status === 'conceptual_error' && analysisResult.counter_example && (
					<div className="counter-example" style={{
						backgroundColor: '#f8d7da',
						border: '1px solid #f5c6cb',
						borderRadius: '4px',
						padding: '16px',
						marginBottom: 16
					}}>
						<h3>🔍 反例测试用例</h3>
						<pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'Monaco, Consolas, monospace' }}>
							{JSON.stringify(analysisResult.counter_example, null, 2)}
						</pre>
					</div>
				)}

				{analysisResult.implementation_analysis && (
					<div className="implementation-analysis" style={{
						backgroundColor: '#fff3cd',
						border: '1px solid #ffeaa7',
						borderRadius: '4px',
						padding: '16px',
						marginBottom: 16
					}}>
						<h3>🔧 实现错误分析</h3>
						<div style={{ whiteSpace: 'pre-wrap' }}>
							{analysisResult.implementation_analysis}
						</div>
					</div>
				)}

				{analysisResult.fix_suggestions && (
					<div className="fix-suggestions" style={{
						backgroundColor: '#d1ecf1',
						border: '1px solid #bee5eb',
						borderRadius: '4px',
						padding: '16px',
						marginBottom: 16
					}}>
						<h3>💡 修复建议</h3>
						<div style={{ whiteSpace: 'pre-wrap' }}>
							{analysisResult.fix_suggestions}
						</div>
					</div>
				)}

				{analysisResult.error_id && (
					<div className="error-reference" style={{
						backgroundColor: '#e2e3e5',
						border: '1px solid #d6d8db',
						borderRadius: '4px',
						padding: '16px'
					}}>
						<h3>📚 错误参考</h3>
						<p>错误ID: {analysisResult.error_id}</p>
						<p>该错误已存在于知识库中，可参考相似案例。</p>
					</div>
				)}
			</div>
		)
	}

	return (
		<div className="page student-analysis-page">
			<div className="header">
				<h1>🎯 代码深度分析</h1>
				<p>分析学生代码的错误类型，提供针对性的修复建议</p>
			</div>

			<div className="input-section" style={{ marginBottom: 20 }}>
				<div style={{ marginBottom: 16 }}>
					<label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>
						题目ID：
					</label>
					<input
						type="text"
						value={problemId}
						onChange={(e) => setProblemId(e.target.value)}
						placeholder="例如: SDUOJ-1001"
						style={{
							width: '300px',
							padding: '8px',
							border: '1px solid #ddd',
							borderRadius: '4px'
						}}
					/>
				</div>

				<div style={{ marginBottom: 16 }}>
					<label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>
						题目描述：
					</label>
					<textarea
						value={problemDescription}
						onChange={(e) => setProblemDescription(e.target.value)}
						placeholder="请输入题目描述..."
						style={{
							width: '100%',
							height: '150px',
							fontFamily: 'Monaco, Consolas, "Courier New", monospace',
							fontSize: '14px',
							padding: '12px',
							border: '1px solid #ddd',
							borderRadius: '4px',
							resize: 'vertical'
						}}
					/>
				</div>

				<div style={{ marginBottom: 16 }}>
					<label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>
						学生代码：
					</label>
					<textarea
						value={studentCode}
						onChange={(e) => setStudentCode(e.target.value)}
						placeholder="请输入学生提交的代码..."
						style={{
							width: '100%',
							height: '200px',
							fontFamily: 'Monaco, Consolas, "Courier New", monospace',
							fontSize: '14px',
							padding: '12px',
							border: '1px solid #ddd',
							borderRadius: '4px',
							resize: 'vertical'
						}}
					/>
				</div>
			</div>

			<div className="actions" style={{ marginBottom: 20 }}>
				<button 
					onClick={analyzeStudentCode} 
					disabled={loading || !studentCode.trim() || !problemDescription.trim()}
					style={{
						padding: '12px 24px',
						fontSize: '16px',
						backgroundColor: loading ? '#ccc' : '#dc3545',
						color: 'white',
						border: 'none',
						borderRadius: '4px',
						cursor: loading ? 'not-allowed' : 'pointer'
					}}
				>
					{loading ? '分析中...' : '分析代码'}
				</button>
			</div>

			{error && (
				<div className="error" style={{
					padding: '12px',
					backgroundColor: '#f8d7da',
					color: '#721c24',
					border: '1px solid #f5c6cb',
					borderRadius: '4px',
					marginBottom: 20
				}}>
					❌ {error}
				</div>
			)}

			{result && (
				<div className="result-section">
					<h2>📋 分析结果</h2>
					{renderAnalysisResult()}
					{result.message && (
						<p style={{ marginTop: 12, color: '#28a745', fontWeight: 'bold' }}>
							✅ {result.message}
						</p>
					)}
				</div>
			)}
		</div>
	)
}
