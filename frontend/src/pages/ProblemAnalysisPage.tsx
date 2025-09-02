import { useState } from 'react'
import { appConfig } from '../config'

type ProblemAnalysisResult = {
	status: string
	result: {
		problem_code: string
		simplified_description: string
		edge_cases: string
		possible_errors: string
		solutions: any[]
		std_code: string | null
	}
	message?: string
}

export function ProblemAnalysisPage() {
	const [problemCode, setProblemCode] = useState('SDUOJ-1001')
	const [problemDescription, setProblemDescription] = useState(`# A+B Problem

## 题目描述
给定两个整数A和B，计算A+B的值。

## 输入格式
一行包含两个整数A和B，用空格分隔。

## 输出格式
输出一个整数，即A+B的值。

## 数据范围
- -10^9 ≤ A, B ≤ 10^9

## 样例输入
1 2

## 样例输出
3`)
	const [result, setResult] = useState<ProblemAnalysisResult | null>(null)
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)
	const [activeTab, setActiveTab] = useState<'simplified' | 'edge_cases' | 'errors'>('simplified')

	async function analyzeProblem() {
		if (!problemDescription.trim()) return
		
		setLoading(true)
		setError(null)
		setResult(null)

		try {
			const apiUrl = appConfig.enableDevProxy ? '/api/problem-analysis' : `${appConfig.apiGatewayUrl}/api/problem-analysis`
			const response = await fetch(apiUrl, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					problem_code: problemCode,
					problem_description: problemDescription
				}),
			})

			if (!response.ok) {
				throw new Error(`HTTP ${response.status}: ${response.statusText}`)
			}

			const data: ProblemAnalysisResult = await response.json()
			setResult(data)
		} catch (err) {
			const errorMessage = err instanceof Error ? err.message : '未知错误'
			setError(`题目分析失败: ${errorMessage}`)
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="page problem-analysis-page">
			<div className="header">
				<h1>📊 题目深度分析</h1>
				<p>对题目进行深度分析，生成简化描述、边缘用例和错误分析</p>
			</div>

			<div className="input-section" style={{ marginBottom: 20 }}>
				<div style={{ marginBottom: 16 }}>
					<label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>
						题目代码：
					</label>
					<input
						type="text"
						value={problemCode}
						onChange={(e) => setProblemCode(e.target.value)}
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
						placeholder="请输入完整的题目描述..."
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
					onClick={analyzeProblem} 
					disabled={loading || !problemDescription.trim()}
					style={{
						padding: '12px 24px',
						fontSize: '16px',
						backgroundColor: loading ? '#ccc' : '#28a745',
						color: 'white',
						border: 'none',
						borderRadius: '4px',
						cursor: loading ? 'not-allowed' : 'pointer'
					}}
				>
					{loading ? '分析中...' : '开始分析'}
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
					
					<div className="tabs" style={{ marginBottom: 16 }}>
						<button 
							onClick={() => setActiveTab('simplified')}
							style={{
								padding: '8px 16px',
								marginRight: '8px',
								backgroundColor: activeTab === 'simplified' ? '#007bff' : '#f8f9fa',
								color: activeTab === 'simplified' ? 'white' : '#333',
								border: '1px solid #dee2e6',
								borderRadius: '4px',
								cursor: 'pointer'
							}}
						>
							简化描述
						</button>
						<button 
							onClick={() => setActiveTab('edge_cases')}
							style={{
								padding: '8px 16px',
								marginRight: '8px',
								backgroundColor: activeTab === 'edge_cases' ? '#007bff' : '#f8f9fa',
								color: activeTab === 'edge_cases' ? 'white' : '#333',
								border: '1px solid #dee2e6',
								borderRadius: '4px',
								cursor: 'pointer'
							}}
						>
							边缘用例
						</button>
						<button 
							onClick={() => setActiveTab('errors')}
							style={{
								padding: '8px 16px',
								backgroundColor: activeTab === 'errors' ? '#007bff' : '#f8f9fa',
								color: activeTab === 'errors' ? 'white' : '#333',
								border: '1px solid #dee2e6',
								borderRadius: '4px',
								cursor: 'pointer'
							}}
						>
							可能错误
						</button>
					</div>

					<div className="tab-content" style={{
						backgroundColor: '#f8f9fa',
						border: '1px solid #dee2e6',
						borderRadius: '4px',
						padding: '16px',
						whiteSpace: 'pre-wrap',
						fontFamily: 'Monaco, Consolas, "Courier New", monospace',
						fontSize: '14px',
						lineHeight: '1.5',
						maxHeight: '500px',
						overflowY: 'auto'
					}}>
						{activeTab === 'simplified' && result.result.simplified_description}
						{activeTab === 'edge_cases' && result.result.edge_cases}
						{activeTab === 'errors' && result.result.possible_errors}
					</div>

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
