import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
	const env = loadEnv(mode, process.cwd(), '')
	const enableProxy = env.VITE_ENABLE_DEV_PROXY === 'true'
	return {
		plugins: [react()],
		server: enableProxy
			? {
				proxy: {
					'/api': {
						target: env.VITE_API_GATEWAY_URL || 'http://10.102.32.223:8080',
						changeOrigin: true,
						rewrite: (path) => path.replace(/^\/api/, '/api'),
					},
					'/v1': {
						target: env.VITE_DEFAULT_MODEL_PROVIDER === 'sdu' ? env.VITE_SDU_BASE_URL : env.VITE_VLLM_BASE_URL,
						changeOrigin: true,
						rewrite: (path) => path.replace(/^\/v1/, '/v1'),
					},
					'/embeddings': {
						target: env.VITE_EMBEDDING_BASE_URL,
						changeOrigin: true,
						rewrite: (path) => path.replace(/^\/embeddings/, ''),
					},
					'/tts': {
						target: env.VITE_TTS_MINIMAX_BASE_URL,
						changeOrigin: true,
					},
				}
			}
			: undefined,
	}
})
