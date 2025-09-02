import { useState } from 'react'
import { appConfig } from '../config'
import { ApiKeyInput } from '../components/ApiKeyInput'

export function EmbeddingPage() {
	const [text, setText] = useState('你好，世界')
	const [vector, setVector] = useState<number[] | null>(null)
	const [loading, setLoading] = useState(false)
	const [apiKey, setApiKey] = useState('')

	async function runEmbedding() {
		if (!text.trim()) return
		setLoading(true)
		setVector(null)
		try {
			const headers: Record<string, string> = { 'Content-Type': 'application/json' }
			if (apiKey) headers['Authorization'] = `Bearer ${apiKey}`
			const res = await fetch(appConfig.embeddingBaseUrl, {
				method: 'POST',
				headers,
				body: JSON.stringify({
					model: 'embeddings',
					input: text,
				}),
			})
			const json = await res.json()
			const vec = json.data?.[0]?.embedding as number[] | undefined
			if (vec) setVector(vec)
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="page embed-page">
			<div className="toolbar" style={{ display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
				<ApiKeyInput onChange={setApiKey} />
			</div>
			<div className="toolbar">
				<textarea value={text} onChange={(e) => setText(e.target.value)} rows={4} />
				<button onClick={runEmbedding} disabled={loading}>生成向量</button>
			</div>
			{vector && (
				<div className="result">
					<p>维度：{vector.length}</p>
					<p>前 8 项：{vector.slice(0, 8).map((v) => v.toFixed(4)).join(', ')}</p>
				</div>
			)}
		</div>
	)
} 