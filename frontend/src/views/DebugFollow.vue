<template>
  <div class="max-w-4xl mx-auto py-8 px-4">
    <h1 class="text-3xl font-bold mb-8">关注功能调试</h1>
    
    <!-- 当前用户信息 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">当前用户信息</h2>
      <div v-if="authStore.isAuthenticated">
        <p><strong>用户ID:</strong> {{ authStore.user?.id }}</p>
        <p><strong>用户名:</strong> {{ authStore.user?.username || authStore.user?.email }}</p>
        <p><strong>邮箱:</strong> {{ authStore.user?.email }}</p>
        <p><strong>角色:</strong> {{ authStore.user?.role || 'user' }}</p>
        <p><strong>Token:</strong> {{ authStore.token ? '已设置' : '未设置' }}</p>
      </div>
      <div v-else>
        <p class="text-red-600">未登录</p>
      </div>
    </div>

    <!-- API测试 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">API测试</h2>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-2">测试用户ID:</label>
          <input 
            v-model="testUserId" 
            type="number" 
            class="border border-gray-300 rounded px-3 py-2 w-32"
            placeholder="输入用户ID"
          />
          <button 
            @click="testFollowStatus"
            class="ml-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            检查关注状态
          </button>
        </div>
        
        <div v-if="apiResult" class="mt-4 p-4 bg-gray-100 rounded">
          <h3 class="font-medium mb-2">API结果:</h3>
          <pre class="text-sm">{{ JSON.stringify(apiResult, null, 2) }}</pre>
        </div>
      </div>
    </div>

    <!-- 数据库关注记录 -->
    <div class="bg-white rounded-lg shadow p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">数据库关注记录</h2>
      <button 
        @click="loadFollowRecords"
        class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 mb-4"
      >
        加载关注记录
      </button>
      
      <div v-if="followRecords.length > 0" class="overflow-x-auto">
        <table class="min-w-full border border-gray-300">
          <thead class="bg-gray-50">
            <tr>
              <th class="border border-gray-300 px-4 py-2">ID</th>
              <th class="border border-gray-300 px-4 py-2">关注者ID</th>
              <th class="border border-gray-300 px-4 py-2">被关注者ID</th>
              <th class="border border-gray-300 px-4 py-2">创建时间</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in followRecords" :key="record.id">
              <td class="border border-gray-300 px-4 py-2">{{ record.id }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ record.followerId }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ record.followingId }}</td>
              <td class="border border-gray-300 px-4 py-2">{{ record.created_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 实际测试 -->
    <div class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">实际关注测试</h2>
      <div class="space-y-4">
        <div v-for="user in testUsers" :key="user.id" class="flex items-center justify-between p-4 border rounded">
          <div>
            <p class="font-medium">{{ user.name }}</p>
            <p class="text-sm text-gray-500">用户ID: {{ user.id }}</p>
          </div>
          <div class="flex items-center space-x-3">
            <button 
              @click="checkUserFollowStatus(user.id)"
              class="px-3 py-1 bg-gray-600 text-white rounded text-sm"
            >
              检查状态
            </button>
            <span :class="[
              'px-2 py-1 rounded text-sm',
              userStatuses[user.id] === true ? 'bg-green-100 text-green-800' :
              userStatuses[user.id] === false ? 'bg-red-100 text-red-800' :
              'bg-gray-100 text-gray-800'
            ]">
              {{ 
                userStatuses[user.id] === true ? '已关注' :
                userStatuses[user.id] === false ? '未关注' :
                '未检查'
              }}
            </span>
            <FollowButton 
              v-if="authStore.isAuthenticated"
              :userId="user.id"
              :initialFollowStatus="userStatuses[user.id]"
              @follow-changed="onFollowChanged"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { followsAPI } from '../api/follows'
import FollowButton from '../components/user/FollowButton.vue'

const authStore = useAuthStore()

const testUserId = ref(1)
const apiResult = ref(null)
const followRecords = ref([])
const userStatuses = ref({})

const testUsers = [
  { id: 1, name: '用户1' },
  { id: 2, name: '用户2' },
  { id: 3, name: '用户3' },
  { id: 4, name: '用户4' }
]

// 测试关注状态API
const testFollowStatus = async () => {
  if (!authStore.isAuthenticated) {
    apiResult.value = { error: '未登录' }
    return
  }

  try {
    console.log('测试关注状态API, 用户ID:', testUserId.value)
    const response = await followsAPI.checkFollowStatus(testUserId.value)
    console.log('API响应:', response)
    apiResult.value = {
      success: true,
      data: response.data,
      url: `/users/${testUserId.value}/follow/status`,
      currentUser: authStore.user?.id,
      targetUser: testUserId.value
    }
  } catch (error) {
    console.error('API错误:', error)
    apiResult.value = {
      success: false,
      error: error.response?.data || error.message,
      status: error.response?.status
    }
  }
}

// 加载关注记录（模拟）
const loadFollowRecords = () => {
  // 这里模拟一些关注记录，实际应该从API获取
  followRecords.value = [
    { id: 13, followerId: 2, followingId: 1, created_at: '2025-06-18T18:58:36.820064Z' },
    { id: 12, followerId: 1, followingId: 4, created_at: '2025-06-14T09:15:00.000000Z' },
    { id: 11, followerId: 7, followingId: 5, created_at: '2025-06-18T19:56:00.000000Z' }
  ]
}

// 检查特定用户的关注状态
const checkUserFollowStatus = async (userId) => {
  if (!authStore.isAuthenticated) {
    console.log('未登录，无法检查关注状态')
    return
  }

  try {
    console.log('检查用户', userId, '的关注状态')
    const response = await followsAPI.checkFollowStatus(userId)
    console.log('关注状态响应:', response)
    userStatuses.value[userId] = response.data.isFollowing
  } catch (error) {
    console.error('检查关注状态失败:', error)
    userStatuses.value[userId] = false
  }
}

// 关注状态变化回调
const onFollowChanged = (data) => {
  console.log('关注状态变化:', data)
  userStatuses.value[data.userId] = data.isFollowing
}
</script>
