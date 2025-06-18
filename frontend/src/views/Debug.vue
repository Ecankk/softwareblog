<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">🔍 系统诊断页面</h1>
    
    <!-- 基础信息 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">📊 基础信息</h2>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <p><strong>Vue版本:</strong> {{ vueVersion }}</p>
          <p><strong>当前时间:</strong> {{ currentTime }}</p>
          <p><strong>当前路由:</strong> {{ $route.path }}</p>
          <p><strong>浏览器:</strong> {{ userAgent }}</p>
        </div>
        <div>
          <p><strong>API地址:</strong> {{ API_BASE_URL }}</p>
          <p><strong>环境模式:</strong> {{ mode }}</p>
          <p><strong>调试模式:</strong> {{ DEBUG }}</p>
          <p><strong>日志级别:</strong> {{ LOG_LEVEL }}</p>
        </div>
      </div>
    </div>

    <!-- 配置检查 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">⚙️ 配置检查</h2>
      <div class="space-y-2">
        <div class="flex items-center">
          <span :class="API_BASE_URL ? 'text-green-600' : 'text-red-600'">
            {{ API_BASE_URL ? '✅' : '❌' }}
          </span>
          <span class="ml-2">API_BASE_URL: {{ API_BASE_URL || '未配置' }}</span>
        </div>
        <div class="flex items-center">
          <span :class="APP_NAME ? 'text-green-600' : 'text-red-600'">
            {{ APP_NAME ? '✅' : '❌' }}
          </span>
          <span class="ml-2">APP_NAME: {{ APP_NAME || '未配置' }}</span>
        </div>
        <div class="flex items-center">
          <span :class="globalStore ? 'text-green-600' : 'text-red-600'">
            {{ globalStore ? '✅' : '❌' }}
          </span>
          <span class="ml-2">Global Store: {{ globalStore ? '已加载' : '未加载' }}</span>
        </div>
        <div class="flex items-center">
          <span :class="authStore ? 'text-green-600' : 'text-red-600'">
            {{ authStore ? '✅' : '❌' }}
          </span>
          <span class="ml-2">Auth Store: {{ authStore ? '已加载' : '未加载' }}</span>
        </div>
      </div>
    </div>

    <!-- API测试 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">🌐 API连接测试</h2>
      <div class="space-y-4">
        <button 
          @click="testHealthCheck"
          :disabled="testing"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {{ testing ? '测试中...' : '测试健康检查' }}
        </button>
        
        <div v-if="healthResult" class="p-4 rounded" :class="healthResult.success ? 'bg-green-100' : 'bg-red-100'">
          <p class="font-semibold">{{ healthResult.success ? '✅ 连接成功' : '❌ 连接失败' }}</p>
          <pre class="mt-2 text-sm">{{ JSON.stringify(healthResult.data, null, 2) }}</pre>
        </div>
      </div>
    </div>

    <!-- 环境变量 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">🔧 环境变量</h2>
      <div class="bg-gray-100 p-4 rounded">
        <pre class="text-sm">{{ JSON.stringify(envVars, null, 2) }}</pre>
      </div>
    </div>

    <!-- 错误日志 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">📝 错误日志</h2>
      <div v-if="errors.length === 0" class="text-green-600">
        ✅ 暂无错误
      </div>
      <div v-else class="space-y-2">
        <div v-for="(error, index) in errors" :key="index" class="bg-red-100 p-3 rounded">
          <p class="font-semibold text-red-800">{{ error.message }}</p>
          <p class="text-sm text-red-600">{{ error.time }}</p>
          <pre v-if="error.stack" class="text-xs text-red-500 mt-2">{{ error.stack }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onErrorCaptured } from 'vue'
import { useGlobalStore } from '../stores/global'
import { useAuthStore } from '../stores/auth'
import { API_BASE_URL, APP_NAME, DEBUG, LOG_LEVEL } from '../config'

const vueVersion = ref('3.x')
const currentTime = ref('')
const userAgent = ref('')
const mode = ref('')
const testing = ref(false)
const healthResult = ref(null)
const errors = ref([])
const envVars = ref({})

const globalStore = useGlobalStore()
const authStore = useAuthStore()

// 测试健康检查
const testHealthCheck = async () => {
  testing.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/health`)
    const data = await response.json()
    healthResult.value = {
      success: true,
      data: data
    }
  } catch (error) {
    healthResult.value = {
      success: false,
      data: {
        error: error.message,
        stack: error.stack
      }
    }
  } finally {
    testing.value = false
  }
}

// 捕获错误
onErrorCaptured((error, instance, info) => {
  errors.value.push({
    message: error.message,
    stack: error.stack,
    info: info,
    time: new Date().toLocaleString()
  })
  return false
})

// 全局错误处理
window.addEventListener('error', (event) => {
  errors.value.push({
    message: event.message,
    stack: event.error?.stack,
    time: new Date().toLocaleString()
  })
})

window.addEventListener('unhandledrejection', (event) => {
  errors.value.push({
    message: `Promise rejection: ${event.reason}`,
    time: new Date().toLocaleString()
  })
})

onMounted(() => {
  currentTime.value = new Date().toLocaleString()
  userAgent.value = navigator.userAgent
  mode.value = import.meta.env.MODE
  
  // 收集环境变量
  envVars.value = {
    MODE: import.meta.env.MODE,
    DEV: import.meta.env.DEV,
    PROD: import.meta.env.PROD,
    VITE_API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
    VITE_APP_TITLE: import.meta.env.VITE_APP_TITLE,
    VITE_APP_VERSION: import.meta.env.VITE_APP_VERSION
  }
  
  // 自动测试API
  testHealthCheck()
})
</script>
