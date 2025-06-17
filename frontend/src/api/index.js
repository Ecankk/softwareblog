import axios from "axios"
import { useAuthStore } from "../stores/auth"
import { useToastStore } from "../stores/toast"

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
})

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

    if (error.response?.status === 401) {
      authStore.logout()
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
