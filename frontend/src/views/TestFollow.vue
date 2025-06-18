<template>
  <div class="max-w-4xl mx-auto py-8 px-4">
    <h1 class="text-3xl font-bold mb-8">关注功能测试</h1>
    
    <!-- 登录状态 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">当前登录状态</h2>
      <div v-if="authStore.isAuthenticated" class="text-green-600">
        <p>✅ 已登录: {{ authStore.user?.username || authStore.user?.email }}</p>
        <p>用户ID: {{ authStore.user?.id }}</p>
        <p>角色: {{ authStore.user?.role || 'user' }}</p>
        <p>是否管理员: {{ authStore.isAdmin ? '是' : '否' }}</p>
      </div>
      <div v-else class="text-red-600">
        <p>❌ 未登录</p>
        <router-link to="/login" class="text-blue-600 hover:underline">点击登录</router-link>
      </div>
    </div>

    <!-- 关注按钮测试 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">关注按钮测试</h2>
      <div class="space-y-4">
        <!-- 测试用户1 -->
        <div class="flex items-center justify-between p-4 border rounded-lg">
          <div class="flex items-center space-x-3">
            <img 
              src="https://api.dicebear.com/7.x/avataaars/svg?seed=user1" 
              alt="测试用户1"
              class="w-10 h-10 rounded-full"
            />
            <div>
              <p class="font-medium">测试用户1</p>
              <p class="text-sm text-gray-500">user1@example.com</p>
            </div>
          </div>
          <FollowButton :userId="1" @follow-changed="onFollowChanged" />
        </div>

        <!-- 测试用户2 -->
        <div class="flex items-center justify-between p-4 border rounded-lg">
          <div class="flex items-center space-x-3">
            <img 
              src="https://api.dicebear.com/7.x/avataaars/svg?seed=user2" 
              alt="测试用户2"
              class="w-10 h-10 rounded-full"
            />
            <div>
              <p class="font-medium">测试用户2</p>
              <p class="text-sm text-gray-500">user2@example.com</p>
            </div>
          </div>
          <FollowButton :userId="2" @follow-changed="onFollowChanged" />
        </div>

        <!-- 当前用户（应该显示"这是你"） -->
        <div v-if="authStore.user" class="flex items-center justify-between p-4 border rounded-lg bg-gray-50">
          <div class="flex items-center space-x-3">
            <img 
              :src="getAvatarUrl(authStore.user)" 
              :alt="authStore.user.username"
              class="w-10 h-10 rounded-full"
            />
            <div>
              <p class="font-medium">{{ authStore.user.username || '当前用户' }}</p>
              <p class="text-sm text-gray-500">{{ authStore.user.email }}</p>
            </div>
          </div>
          <FollowButton :userId="authStore.user.id" @follow-changed="onFollowChanged" />
        </div>
      </div>
    </div>

    <!-- 管理员功能测试 -->
    <div v-if="authStore.isAdmin" class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">管理员功能</h2>
      <div class="space-y-4">
        <router-link 
          to="/admin"
          class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          进入管理后台
        </router-link>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <button 
            @click="testAdminAPI('stats')"
            class="p-4 border rounded-lg hover:bg-gray-50"
          >
            <h3 class="font-medium">测试统计API</h3>
            <p class="text-sm text-gray-500">获取系统统计信息</p>
          </button>
          
          <button 
            @click="testAdminAPI('users')"
            class="p-4 border rounded-lg hover:bg-gray-50"
          >
            <h3 class="font-medium">测试用户API</h3>
            <p class="text-sm text-gray-500">获取用户列表</p>
          </button>
          
          <button 
            @click="testAdminAPI('posts')"
            class="p-4 border rounded-lg hover:bg-gray-50"
          >
            <h3 class="font-medium">测试文章API</h3>
            <p class="text-sm text-gray-500">获取文章列表</p>
          </button>
        </div>
      </div>
    </div>

    <!-- API测试结果 -->
    <div v-if="apiResult" class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">API测试结果</h2>
      <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto">{{ JSON.stringify(apiResult, null, 2) }}</pre>
    </div>

    <!-- 关注状态变化日志 -->
    <div v-if="followLogs.length > 0" class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">关注操作日志</h2>
      <div class="space-y-2">
        <div 
          v-for="(log, index) in followLogs" 
          :key="index"
          class="p-3 bg-gray-50 rounded text-sm"
        >
          <span class="text-gray-500">{{ log.time }}</span> - 
          <span :class="log.isFollowing ? 'text-green-600' : 'text-red-600'">
            {{ log.isFollowing ? '关注了' : '取消关注了' }}
          </span>
          用户ID: {{ log.userId }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useToastStore } from '../stores/toast'
import { adminAPI } from '../api/admin'
import { getAvatarUrl } from '../utils/avatar'
import FollowButton from '../components/user/FollowButton.vue'

const authStore = useAuthStore()
const toastStore = useToastStore()

const apiResult = ref(null)
const followLogs = ref([])

// 关注状态变化回调
const onFollowChanged = (data) => {
  followLogs.value.unshift({
    ...data,
    time: new Date().toLocaleTimeString()
  })
  
  // 只保留最近10条记录
  if (followLogs.value.length > 10) {
    followLogs.value = followLogs.value.slice(0, 10)
  }
}

// 测试管理员API
const testAdminAPI = async (type) => {
  try {
    let result
    switch (type) {
      case 'stats':
        result = await adminAPI.getStats()
        break
      case 'users':
        result = await adminAPI.getAllUsers({ page: 1, limit: 5 })
        break
      case 'posts':
        result = await adminAPI.getAllPosts({ page: 1, limit: 5 })
        break
      default:
        throw new Error('未知的API类型')
    }
    
    apiResult.value = {
      type,
      success: true,
      data: result.data || result,
      timestamp: new Date().toISOString()
    }
    
    toastStore.showToast(`${type} API测试成功`, 'success')
  } catch (error) {
    console.error(`${type} API测试失败:`, error)
    
    apiResult.value = {
      type,
      success: false,
      error: error.response?.data || error.message,
      timestamp: new Date().toISOString()
    }
    
    toastStore.showToast(`${type} API测试失败`, 'error')
  }
}
</script>
