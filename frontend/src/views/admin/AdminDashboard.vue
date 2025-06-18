<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="bg-white rounded-lg shadow-sm p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">管理后台</h1>
      
      <!-- 统计卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-blue-50 rounded-lg p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                <span class="text-white text-sm font-bold">文</span>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-blue-600">总文章数</p>
              <p class="text-2xl font-bold text-blue-900">{{ stats.posts_count }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-green-50 rounded-lg p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                <span class="text-white text-sm font-bold">用</span>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-green-600">总用户数</p>
              <p class="text-2xl font-bold text-green-900">{{ stats.users_count }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-yellow-50 rounded-lg p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-500 rounded-lg flex items-center justify-center">
                <span class="text-white text-sm font-bold">评</span>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-yellow-600">总评论数</p>
              <p class="text-2xl font-bold text-yellow-900">{{ stats.comments_count }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-red-50 rounded-lg p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-500 rounded-lg flex items-center justify-center">
                <span class="text-white text-sm font-bold">举</span>
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-red-600">标签数量</p>
              <p class="text-2xl font-bold text-red-900">{{ stats.tags_count }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 管理标签页 -->
      <div class="border-b border-gray-200 mb-6">
        <nav class="-mb-px flex space-x-8">
          <button
            v-for="tab in adminTabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm',
              activeTab === tab.key
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>
      
      <!-- 标签页内容 -->
      <div class="min-h-96">
        <!-- 文章管理 -->
        <div v-if="activeTab === 'posts'">
          <div class="text-center py-12 text-gray-500">
            文章管理功能开发中...
          </div>
        </div>
        
        <!-- 用户管理 -->
        <div v-else-if="activeTab === 'users'">
          <div class="text-center py-12 text-gray-500">
            用户管理功能开发中...
          </div>
        </div>
        
        <!-- 评论审核 -->
        <div v-else-if="activeTab === 'comments'">
          <div class="text-center py-12 text-gray-500">
            评论审核功能开发中...
          </div>
        </div>
        
        <!-- 举报处理 -->
        <div v-else-if="activeTab === 'reports'">
          <div class="text-center py-12 text-gray-500">
            举报处理功能开发中...
          </div>
        </div>
        
        <!-- 系统设置 -->
        <div v-else-if="activeTab === 'settings'">
          <div class="text-center py-12 text-gray-500">
            系统设置功能开发中...
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { adminAPI } from '../../api/admin'

const authStore = useAuthStore()
const toastStore = useToastStore()

const activeTab = ref('posts')
const stats = ref({
  users_count: 0,
  posts_count: 0,
  comments_count: 0,
  tags_count: 0,
  follows_count: 0,
  notifications_count: 0
})

// 检查管理员权限
if (!authStore.isAuthenticated || authStore.user?.role !== 'admin') {
  toastStore.error('需要管理员权限')
}

const adminTabs = [
  { key: 'posts', label: '文章管理' },
  { key: 'users', label: '用户管理' },
  { key: 'comments', label: '评论审核' },
  { key: 'reports', label: '举报处理' },
  { key: 'settings', label: '系统设置' }
]

const loadStats = async () => {
  try {
    const response = await adminAPI.getStats()
    stats.value = response.data
  } catch (error) {
    console.error('加载统计信息失败:', error)
    toastStore.error('加载统计信息失败')
  }
}

onMounted(() => {
  loadStats()
})
</script>
