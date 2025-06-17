import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { authAPI } from "../api/auth"
import { useToastStore } from "./toast"

export const useAuthStore = defineStore(
  "auth",
  () => {
    const user = ref(null)
    const token = ref(null)
    const isLoading = ref(false)

    const toastStore = useToastStore()

    // 计算属性
    const isAuthenticated = computed(() => !!token.value)
    const isAdmin = computed(() => user.value?.role === "admin")
    const isMember = computed(() => user.value?.is_member || false)

    // 初始化认证状态
    const initAuth = async () => {
      const savedToken = localStorage.getItem("token")
      if (savedToken) {
        token.value = savedToken
        try {
          await fetchUser()
        } catch (error) {
          logout()
        }
      }
    }

    // 登录
    const login = async (credentials) => {
      isLoading.value = true
      try {
        const response = await authAPI.login(credentials)
        token.value = response.data.access_token
        user.value = response.data.user
        localStorage.setItem("token", token.value)
        toastStore.success("登录成功")
        return true
      } catch (error) {
        toastStore.error(error.response?.data?.detail || "登录失败")
        return false
      } finally {
        isLoading.value = false
      }
    }

    // 注册
    const register = async (userData) => {
      isLoading.value = true
      try {
        const response = await authAPI.register(userData)
        toastStore.success("注册成功，请登录")
        return true
      } catch (error) {
        toastStore.error(error.response?.data?.detail || "注册失败")
        return false
      } finally {
        isLoading.value = false
      }
    }

    // 登出
    const logout = () => {
      user.value = null
      token.value = null
      localStorage.removeItem("token")
      toastStore.success("已退出登录")
    }

    // 获取用户信息
    const fetchUser = async () => {
      try {
        const response = await authAPI.getProfile()
        user.value = response.data
      } catch (error) {
        throw error
      }
    }

    // 更新用户信息
    const updateProfile = async (profileData) => {
      isLoading.value = true
      try {
        const response = await authAPI.updateProfile(profileData)
        user.value = response.data
        toastStore.success("个人信息更新成功")
        return true
      } catch (error) {
        toastStore.error(error.response?.data?.detail || "更新失败")
        return false
      } finally {
        isLoading.value = false
      }
    }

    return {
      user,
      token,
      isLoading,
      isAuthenticated,
      isAdmin,
      isMember,
      initAuth,
      login,
      register,
      logout,
      fetchUser,
      updateProfile,
    }
  },
  {
    persist: {
      paths: ["token", "user"],
    },
  },
)
