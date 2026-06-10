import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth')
  if (token) {
    try {
      const parsed = JSON.parse(token)
      if (parsed?.token) {
        config.headers.Authorization = `Bearer ${parsed.token}`
      }
    } catch (_error) {
      localStorage.removeItem('auth')
    }
  }
  return config
})

http.interceptors.response.use(
  (response) => {
    const payload = response.data
    if (payload.code !== 0) {
      return Promise.reject(new Error(payload.message || '请求失败'))
    }
    return payload.data
  },
  (error) => {
    const message = error.response?.data?.message || error.message || '服务请求失败'
    if (error.response?.status === 401) {
      localStorage.removeItem('auth')
    }
    return Promise.reject(new Error(message))
  },
)

export default http
