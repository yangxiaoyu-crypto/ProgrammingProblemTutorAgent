export const appConfig = {
	appName: import.meta.env.VITE_APP_NAME ?? 'SDU AI Code Analysis',
	defaultModelProvider: (import.meta.env.VITE_DEFAULT_MODEL_PROVIDER as 'sdu' | 'vllm') ?? 'vllm',
	sduBaseUrl: import.meta.env.VITE_SDU_BASE_URL ?? 'http://10.2.8.77:3000/v1',
	vllmBaseUrl: import.meta.env.VITE_VLLM_BASE_URL ?? 'http://10.102.32.223:8000/v1',
	embeddingBaseUrl: import.meta.env.VITE_EMBEDDING_BASE_URL ?? 'http://10.2.8.77:3000/v1/embeddings',
	apiGatewayUrl: import.meta.env.VITE_ENABLE_DEV_PROXY === 'true' ? '' : (import.meta.env.VITE_API_GATEWAY_URL ?? 'http://10.102.32.223:8080'),
	enableDevProxy: import.meta.env.VITE_ENABLE_DEV_PROXY === 'true',
}