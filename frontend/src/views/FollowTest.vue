<template>
  <div class="max-w-4xl mx-auto py-8 px-4">
    <h1 class="text-3xl font-bold mb-8">关注功能测试</h1>
    
    <!-- 登录状态 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">当前登录状态</h2>
      <div v-if="authStore.isAuthenticated" class="text-green-600">
        <p>✅ 已登录: {{ authStore.user?.username || authStore.user?.email }}</p>
        <p>用户ID: {{ authStore.user?.id }}</p>
      </div>
      <div v-else class="text-red-600">
        <p>❌ 未登录</p>
        <router-link to="/login" class="text-blue-600 hover:underline">点击登录</router-link>
      </div>
    </div>

    <!-- 测试用户列表 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">测试用户</h2>
      <div class="space-y-4">
        <div v-for="testUser in testUsers" :key="testUser.id" class="flex items-center justify-between p-4 border rounded-lg">
          <div class="flex items-center space-x-3">
            <img 
              :src="testUser.avatar" 
              :alt="testUser.username"
              class="w-12 h-12 rounded-full"
            />
            <div>
              <p class="font-medium">{{ testUser.username }}</p>
              <p class="text-sm text-gray-500">{{ testUser.email }}</p>
              <p class="text-sm text-gray-500">用户ID: {{ testUser.id }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <router-link 
              :to="`/user/${testUser.id}`"
              class="px-3 py-1 border border-gray-300 rounded text-sm hover:bg-gray-50"
            >
              查看资料
            </router-link>
            <FollowButton
              v-if="authStore.isAuthenticated"
              :userId="testUser.id"
              @follow-changed="onFollowChanged"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 关注状态测试 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">关注状态测试</h2>
      <div class="space-y-4">
        <div v-for="testUser in testUsers" :key="`status-${testUser.id}`" class="flex items-center justify-between p-3 bg-gray-50 rounded">
          <span>用户 {{ testUser.username }} (ID: {{ testUser.id }})</span>
          <div class="flex items-center space-x-2">
            <button 
              @click="checkFollowStatus(testUser.id)"
              class="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700"
            >
              检查状态
            </button>
            <span :class="[
              'px-2 py-1 rounded text-sm',
              followStatuses[testUser.id] === true ? 'bg-green-100 text-green-800' :
              followStatuses[testUser.id] === false ? 'bg-red-100 text-red-800' :
              'bg-gray-100 text-gray-800'
            ]">
              {{ 
                followStatuses[testUser.id] === true ? '已关注' :
                followStatuses[testUser.id] === false ? '未关注' :
                '未检查'
              }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作日志 -->
    <div v-if="operationLogs.length > 0" class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">操作日志</h2>
      <div class="space-y-2 max-h-64 overflow-y-auto">
        <div 
          v-for="(log, index) in operationLogs" 
          :key="index"
          class="p-3 bg-gray-50 rounded text-sm"
        >
          <span class="text-gray-500">{{ log.time }}</span> - 
          <span :class="log.type === 'success' ? 'text-green-600' : log.type === 'error' ? 'text-red-600' : 'text-blue-600'">
            {{ log.message }}
          </span>
        </div>
      </div>
      <button 
        @click="operationLogs = []"
        class="mt-4 px-3 py-1 bg-gray-600 text-white rounded text-sm hover:bg-gray-700"
      >
        清空日志
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { followsAPI } from '../api/follows'
import FollowButton from '../components/user/FollowButton.vue'

const authStore = useAuthStore()

const testUsers = ref([
  {
    id: 1,
    username: '测试用户1',
    email: 'user1@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=user1'
  },
  {
    id: 2,
    username: '测试用户2',
    email: 'user2@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=user2'
  },
  {
    id: 3,
    username: '测试用户3',
    email: 'user3@example.com',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=user3'
  }
])

const followStatuses = ref({})
const operationLogs = ref([])

// 添加日志
const addLog = (message, type = 'info') => {
  operationLogs.value.unshift({
    time: new Date().toLocaleTimeString(),
    message,
    type
  })
  
  // 只保留最近20条记录
  if (operationLogs.value.length > 20) {
    operationLogs.value = operationLogs.value.slice(0, 20)
  }
}

// 检查关注状态
const checkFollowStatus = async (userId) => {
  if (!authStore.isAuthenticated) {
    addLog('请先登录', 'error')
    return
  }

  if (authStore.user?.id === userId) {
    addLog(`用户${userId}: 不能关注自己`, 'info')
    followStatuses.value[userId] = null
    return
  }

  try {
    addLog(`正在检查用户${userId}的关注状态...`, 'info')
    const response = await followsAPI.checkFollowStatus(userId)
    followStatuses.value[userId] = response.data.isFollowing
    addLog(`用户${userId}: ${response.data.isFollowing ? '已关注' : '未关注'}`, 'success')
  } catch (error) {
    console.error('检查关注状态失败:', error)
    addLog(`检查用户${userId}关注状态失败: ${error.response?.data?.detail || error.message}`, 'error')
  }
}

// 关注状态变化回调
const onFollowChanged = (data) => {
  addLog(`用户${data.userId}: ${data.isFollowing ? '关注成功' : '取消关注成功'}`, 'success')
  followStatuses.value[data.userId] = data.isFollowing
}

// 检查所有用户的关注状态
const checkAllFollowStatuses = async () => {
  if (!authStore.isAuthenticated) {
    addLog('请先登录后再检查关注状态', 'error')
    return
  }

  for (const user of testUsers.value) {
    if (user.id !== authStore.user?.id) {
      await checkFollowStatus(user.id)
      // 添加小延迟避免请求过快
      await new Promise(resolve => setTimeout(resolve, 100))
    }
  }
}

onMounted(() => {
  addLog('关注功能测试页面已加载', 'info')
  
  // 如果已登录，自动检查所有关注状态
  if (authStore.isAuthenticated) {
    setTimeout(() => {
      checkAllFollowStatuses()
    }, 1000)
  }
})
</script>
