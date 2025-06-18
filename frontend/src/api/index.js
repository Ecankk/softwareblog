import axios from "axios"
import { useAuthStore } from "../stores/auth"
import { useToastStore } from "../stores/toast"
import { API_BASE_URL, log } from "../config"

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
})

// 记录API配置
log.info('API配置初始化:', { baseURL: API_BASE_URL })

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    const toastStore = useToastStore()
    const authStore = useAuthStore()

    // 只有在非登录请求的401错误时才自动登出
    if (error.response?.status === 401 && !error.config?.url?.includes('/auth/login')) {
      authStore.logout(false) // 不显示"已退出登录"消息
      toastStore.error("登录已过期，请重新登录")
    } else if (error.response?.status === 403) {
      toastStore.error("权限不足")
    } else if (error.response?.status >= 500) {
      toastStore.error("服务器错误，请稍后重试")
    }

    return Promise.reject(error)
  },
)

export default api
