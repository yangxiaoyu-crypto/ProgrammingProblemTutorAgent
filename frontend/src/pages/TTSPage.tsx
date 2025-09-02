import { useRef, useState } from 'react'
import { appConfig } from '../config'

export function TTSPage() {
	const [text, setText] = useState('欢迎使用 TTS 测试页')
	const [loading, setLoading] = useState(false)
	const audioRef = useRef<HTMLAudioElement | null>(null)

	async function runTTS() {
		if (!text.trim()) return
		setLoading(true)
		try {
			const res = await fetch(`${appConfig.enableDevProxy ? '/tts' : appConfig.vllmBaseUrl.replace(/\/v1\/?$/, '') + '/tts'}`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ text }),
			})
			const blob = await res.blob()
			const url = URL.createObjectURL(blob)
			if (audioRef.current) {
				audioRef.current.src = url
				audioRef.current.play()
			}
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="page tts-page">
			<textarea value={text} onChange={(e) => setText(e.target.value)} rows={3} />
			<div>
				<button onClick={runTTS} disabled={loading}>合成并播放</button>
			</div>
			<audio ref={audioRef} controls />
		</div>
	)
} 