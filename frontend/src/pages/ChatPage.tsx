import { useEffect, useRef, useState } from 'react'
import { appConfig } from '../config'
import { ApiKeyInput } from '../components/ApiKeyInput'

type ChatMessage = {
	role: 'user' | 'assistant'
	content: string
}

export function ChatPage() {
	const [provider, setProvider] = useState<'sdu' | 'vllm'>(appConfig.defaultModelProvider)
	const [model, setModel] = useState<string>(appConfig.defaultModelProvider === 'vllm' ? 'qwen2.5-7b-instruct' : 'gpt-3.5-turbo')
	const [stream, setStream] = useState<boolean>(true)
	const [input, setInput] = useState('')
	const [messages, setMessages] = useState<ChatMessage[]>([])
	const [loading, setLoading] = useState(false)
	const [apiKey, setApiKey] = useState<string>('')
	const controllerRef = useRef<AbortController | null>(null)

	const baseUrl = provider === 'sdu' ? appConfig.sduBaseUrl : appConfig.vllmBaseUrl

	async function sendMessage() {
		if (!input.trim() || loading) return
		const userMsg: ChatMessage = { role: 'user', content: input }
		setMessages((m) => [...m, userMsg, { role: 'assistant', content: '' }])
		setInput('')
		setLoading(true)

		const controller = new AbortController()
		controllerRef.current = controller

		try {
			const headers: Record<string, string> = { 'Content-Type': 'application/json' }
			if (apiKey) headers['Authorization'] = `Bearer ${apiKey}`

			// 过滤掉占位的空 assistant 消息
			const history = messages
				.concat(userMsg)
				.filter((m) => !(m.role === 'assistant' && m.content.trim() === ''))
				.map((m) => ({ role: m.role, content: m.content }))

			const body = JSON.stringify({ model, stream, messages: history })

			const res = await fetch(`${baseUrl}/chat/completions`, {
				method: 'POST',
				headers,
				body,
				signal: controller.signal,
			})
			if (!res.ok) throw new Error(`网络错误: ${res.status}`)

			if (!stream) {
				const json = await res.json()
				const content = json.choices?.[0]?.message?.content ?? JSON.stringify(json)
				setMessages((prev) => {
					const copy = [...prev]
					copy[copy.length - 1] = { role: 'assistant', content }
					return copy
				})
				return
			}

			if (!res.body) throw new Error('无响应体')
			const reader = res.body.getReader()
			const decoder = new TextDecoder('utf-8')
			let assistantText = ''
			while (true) {
				const { value, done } = await reader.read()
				if (done) break
				const chunk = decoder.decode(value, { stream: true })
				for (const line of chunk.split('\n')) {
					const data = line.replace(/^data: /, '').trim()
					if (!data) continue
					if (data === '[DONE]') break
					try {
						const json = JSON.parse(data)
						const delta = json.choices?.[0]?.delta?.content ?? ''
						if (delta) {
							assistantText += delta
							setMessages((prev) => {
								const copy = [...prev]
								copy[copy.length - 1] = { role: 'assistant', content: assistantText }
								return copy
							})
						}
					} catch {}
				}
			}
		} catch (e) {
			console.error(e)
		} finally {
			setLoading(false)
			controllerRef.current = null
		}
	}

	useEffect(() => () => controllerRef.current?.abort(), [])

	return (
		<div className="page chat-page">
			<div className="toolbar" style={{ display: 'flex', gap: 16, alignItems: 'center', flexWrap: 'wrap' }}>
				<label>
					模型源：
					<select value={provider} onChange={(e) => setProvider(e.target.value as 'sdu' | 'vllm')}>
						<option value="vllm">VLLM</option>
						<option value="sdu">SDU</option>
					</select>
				</label>
				<label>
					模型名：
					<input value={model} onChange={(e) => setModel(e.target.value)} style={{ width: 220 }} />
				</label>
				<label>
					流式：
					<input type="checkbox" checked={stream} onChange={(e) => setStream(e.target.checked)} />
				</label>
				<ApiKeyInput onChange={setApiKey} />
			</div>
			<div className="messages">
				{messages.map((m, i) => (
					<div key={i} className={`msg ${m.role}`}>
						{m.content}
					</div>
				))}
			</div>
			<div className="composer">
				<input value={input} onChange={(e) => setInput(e.target.value)} placeholder="输入你的问题..." />
				<button onClick={sendMessage} disabled={loading || !input.trim()}>
					发送
				</button>
			</div>
		</div>
	)
} 