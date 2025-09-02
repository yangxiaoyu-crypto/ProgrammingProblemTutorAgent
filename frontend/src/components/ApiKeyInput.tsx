import { useEffect, useMemo, useState } from 'react'

function sanitize(raw: string) {
	let s = (raw || '').trim()
	// 去掉首尾成对引号
	if ((s.startsWith('"') && s.endsWith('"')) || (s.startsWith("'") && s.endsWith("'"))) {
		s = s.slice(1, -1)
	}
	// 移除不可见字符与非 ASCII 字符（只保留 0x20-0x7E）
	s = Array.from(s)
		.filter((ch) => ch.charCodeAt(0) >= 32 && ch.charCodeAt(0) <= 126)
		.join('')
	return s
}

export function ApiKeyInput(props: { onChange?: (key: string) => void }) {
	const [key, setKey] = useState<string>('')

	useEffect(() => {
		const saved = localStorage.getItem('apiKey') || ''
		setKey(saved)
		props.onChange?.(sanitize(saved))
	}, [])

	const display = useMemo(() => key, [key])
	const invalid = useMemo(() => key !== sanitize(key), [key])

	function handleSave(nextRaw: string) {
		setKey(nextRaw)
		const next = sanitize(nextRaw)
		if (next) localStorage.setItem('apiKey', next)
		else localStorage.removeItem('apiKey')
		props.onChange?.(next)
	}

	return (
		<div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
			<label>API Key：</label>
			<input
				type="password"
				value={display}
				onChange={(e) => handleSave(e.target.value)}
				placeholder="可选，输入后将附带 Authorization 头"
				style={{ width: 320 }}
			/>
			{invalid && <span style={{ color: 'orange' }}>已自动清洗非法字符</span>}
		</div>
	)
} 