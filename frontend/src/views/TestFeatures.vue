<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">功能测试页面</h1>
    
    <!-- SVG头像测试 -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">SVG头像测试</h2>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div v-for="userId in [1, 2, 3, 4, 5]" :key="userId" class="text-center">
          <img 
            :src="`http://localhost:8000/users/${userId}/avatar.svg`"
            :alt="`用户${userId}头像`"
            class="w-16 h-16 rounded-full mx-auto mb-2"
          />
          <p class="text-sm text-gray-600">用户 {{ userId }}</p>
        </div>
      </div>
      
      <div class="mt-6">
        <h3 class="text-lg font-medium mb-3">几何图案头像</h3>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div v-for="userId in [1, 2, 3, 4, 5]" :key="`geo-${userId}`" class="text-center">
            <img 
              :src="`http://localhost:8000/users/${userId}/avatar.svg?style=geometric`"
              :alt="`用户${userId}几何头像`"
              class="w-16 h-16 rounded-full mx-auto mb-2"
            />
            <p class="text-sm text-gray-600">几何 {{ userId }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 关注功能测试 -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">关注功能测试</h2>
      <div class="space-y-4">
        <div v-for="user in testUsers" :key="user.id" class="flex items-center justify-between p-4 border rounded-lg">
          <div class="flex items-center space-x-3">
            <img
              :src="getAvatarUrl(user)"
              :alt="user.username"
              class="w-10 h-10 rounded-full"
            />
            <div>
              <p class="font-medium">{{ user.username }}</p>
              <p class="text-sm text-gray-500">{{ user.bio }}</p>
            </div>
          </div>
          <FollowButton :userId="user.id" />
        </div>
      </div>
    </div>
    
    <!-- 通知测试 -->
    <div class="bg-white rounded-lg shadow p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">通知功能测试</h2>
      <div class="space-y-4">
        <div v-if="notifications.length === 0" class="text-gray-500 text-center py-4">
          暂无通知
        </div>
        <div v-else>
          <div 
            v-for="notification in notifications" 
            :key="notification.id"
            class="p-4 border rounded-lg"
            :class="notification.isRead ? 'bg-gray-50' : 'bg-blue-50'"
          >
            <div class="flex items-start justify-between">
              <div>
                <p class="font-medium">{{ notification.title }}</p>
                <p class="text-sm text-gray-600 mt-1">{{ notification.content }}</p>
                <p class="text-xs text-gray-400 mt-2">{{ formatDate(notification.created_at) }}</p>
              </div>
              <span v-if="!notification.isRead" class="w-2 h-2 bg-blue-500 rounded-full"></span>
            </div>
          </div>
        </div>
        <button 
          @click="loadNotifications"
          class="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          刷新通知
        </button>
      </div>
    </div>
    
    <!-- 管理后台测试 -->
    <div v-if="authStore.isAdmin" class="bg-white rounded-lg shadow p-6">
      <h2 class="text-xl font-semibold mb-4">管理后台功能测试</h2>
      <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
        <div v-for="(value, key) in adminStats" :key="key" class="text-center p-4 bg-gray-50 rounded">
          <p class="text-2xl font-bold text-blue-600">{{ value }}</p>
          <p class="text-sm text-gray-600">{{ getStatLabel(key) }}</p>
        </div>
      </div>
      <div class="flex space-x-4">
        <button 
          @click="loadAdminStats"
          class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          刷新统计
        </button>
        <router-link 
          to="/admin"
          class="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
        >
          进入管理后台
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { notificationsAPI } from '../api/notifications'
import { adminAPI } from '../api/admin'
import FollowButton from '../components/user/FollowButton.vue'
import { getAvatarUrl } from '../utils/avatar'

const authStore = useAuthStore()

const testUsers = ref([
  { id: 1, username: '管理员', bio: '博客系统管理员' },
  { id: 3, username: '前端开发者', bio: '专注于前端技术' },
  { id: 4, username: '后端工程师', bio: '后端技术爱好者' },
  { id: 5, username: 'UI设计师', bio: 'UI/UX设计师' }
])

const notifications = ref([])
const adminStats = ref({})

const loadNotifications = async () => {
  if (!authStore.isAuthenticated) return
  
  try {
    const response = await notificationsAPI.getNotifications({ limit: 5 })
    notifications.value = response.data.items
  } catch (error) {
    console.error('加载通知失败:', error)
  }
}

const loadAdminStats = async () => {
  if (!authStore.isAdmin) return
  
  try {
    const response = await adminAPI.getStats()
    adminStats.value = response.data
  } catch (error) {
    console.error('加载管理统计失败:', error)
  }
}

const getStatLabel = (key) => {
  const labels = {
    users_count: '用户数',
    posts_count: '文章数',
    comments_count: '评论数',
    tags_count: '标签数',
    follows_count: '关注数',
    notifications_count: '通知数'
  }
  return labels[key] || key
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadNotifications()
  if (authStore.isAdmin) {
    loadAdminStats()
  }
})
</script>
