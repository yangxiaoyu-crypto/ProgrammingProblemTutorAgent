import { BrowserRouter, Link, Route, Routes, Navigate } from 'react-router-dom'
import { ChatPage } from './pages/ChatPage'
import { EmbeddingPage } from './pages/EmbeddingPage'
import { TTSPage } from './pages/TTSPage'
import { CodeCheckPage } from './pages/CodeCheckPage'
import { ProblemAnalysisPage } from './pages/ProblemAnalysisPage'
import { StudentCodeAnalysisPage } from './pages/StudentCodeAnalysisPage'
import './App.css'

export default function App() {
	return (
		<BrowserRouter>
			<div className="app">
				<nav className="nav">
					<Link to="/code-check">代码检查</Link>
					<Link to="/problem-analysis">题目分析</Link>
					<Link to="/student-analysis">代码分析</Link>
					<Link to="/chat">聊天</Link>
					<Link to="/embedding">Embedding</Link>
					<Link to="/tts">TTS</Link>
				</nav>
				<main className="main">
					<Routes>
						<Route path="/" element={<Navigate to="/code-check" replace />} />
						<Route path="/code-check" element={<CodeCheckPage />} />
						<Route path="/problem-analysis" element={<ProblemAnalysisPage />} />
						<Route path="/student-analysis" element={<StudentCodeAnalysisPage />} />
						<Route path="/chat" element={<ChatPage />} />
						<Route path="/embedding" element={<EmbeddingPage />} />
						<Route path="/tts" element={<TTSPage />} />
					</Routes>
				</main>
			</div>
		</BrowserRouter>
	)
}
