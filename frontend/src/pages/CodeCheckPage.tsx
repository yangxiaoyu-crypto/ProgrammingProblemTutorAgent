import { useState } from 'react'
import { appConfig } from '../config'

type CodeCheckResult = {
	status: string
	result: string
	message?: string
}

export function CodeCheckPage() {
	const [code, setCode] = useState(`#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}`)
	const [language, setLanguage] = useState('C++14')
	const [model, setModel] = useState('deepseek/deepseek-chat')
	const [result, setResult] = useState<CodeCheckResult | null>(null)
	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)

	async function checkCode() {
		if (!code.trim()) return
		
		setLoading(true)
		setError(null)
		setResult(null)

		try {
			const apiUrl = appConfig.enableDevProxy ? '/api/code-check' : `${appConfig.apiGatewayUrl}/api/code-check`
			const response = await fetch(apiUrl, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					code: code,
					language: language,
					model: model
				}),
			})

			if (!response.ok) {
				throw new Error(`HTTP ${response.status}: ${response.statusText}`)
			}

			const data: CodeCheckResult = await response.json()
			setResult(data)
		} catch (err) {
			const errorMessage = err instanceof Error ? err.message : '未知错误'
			setError(`代码检查失败: ${errorMessage}`)
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="page code-check-page">
			<div className="header">
				<h1>🔍 通用代码检查</h1>
				<p>检查代码中的潜在错误和优化建议</p>
			</div>

			<div className="toolbar" style={{ display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap', marginBottom: 16 }}>
				<label>
					编程语言：
					<select value={language} onChange={(e) => setLanguage(e.target.value)}>
						<option value="C++14">C++14</option>
						<option value="C++17">C++17</option>
						<option value="C++20">C++20</option>
						<option value="Python3.11">Python3.11</option>
						<option value="Java17">Java17</option>
					</select>
				</label>
				<label>
					分析模型：
					<select value={model} onChange={(e) => setModel(e.target.value)}>
						<option value="deepseek/deepseek-chat">DeepSeek Chat</option>
						<option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
						<option value="gpt-4">GPT-4</option>
					</select>
				</label>
			</div>

			<div className="input-section" style={{ marginBottom: 20 }}>
				<label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>
					请输入要检查的代码：
				</label>
				<textarea
					value={code}
					onChange={(e) => setCode(e.target.value)}
					placeholder="请输入您的代码..."
					style={{
						width: '100%',
						height: '300px',
						fontFamily: 'Monaco, Consolas, "Courier New", monospace',
						fontSize: '14px',
						padding: '12px',
						border: '1px solid #ddd',
						borderRadius: '4px',
						resize: 'vertical'
					}}
				/>
			</div>

			<div className="actions" style={{ marginBottom: 20 }}>
				<button 
					onClick={checkCode} 
					disabled={loading || !code.trim()}
					style={{
						padding: '12px 24px',
						fontSize: '16px',
						backgroundColor: loading ? '#ccc' : '#007bff',
						color: 'white',
						border: 'none',
						borderRadius: '4px',
						cursor: loading ? 'not-allowed' : 'pointer'
					}}
				>
					{loading ? '检查中...' : '开始检查'}
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
					<h2>📋 检查结果</h2>
					<div className="result-content" style={{
						backgroundColor: '#f8f9fa',
						border: '1px solid #dee2e6',
						borderRadius: '4px',
						padding: '16px',
						whiteSpace: 'pre-wrap',
						fontFamily: 'Monaco, Consolas, "Courier New", monospace',
						fontSize: '14px',
						lineHeight: '1.5'
					}}>
						{result.result}
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
