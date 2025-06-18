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

        <!-- 匿名消息管理 -->
        <div v-else-if="activeTab === 'anonymous'">
          <div class="mb-4 flex justify-between items-center">
            <h2 class="text-lg font-semibold text-gray-900">匿名消息管理</h2>
            <button
              @click="loadAnonymousMessages"
              :disabled="loadingMessages"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {{ loadingMessages ? '刷新中...' : '刷新' }}
            </button>
          </div>

          <!-- 匿名消息列表 -->
          <div class="space-y-4">
            <div
              v-for="message in anonymousMessages"
              :key="message.id"
              class="bg-gray-50 rounded-lg p-4 border"
              :class="{ 'opacity-50': message.is_deleted }"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <p class="text-gray-900 mb-2">{{ message.content }}</p>
                  <div class="flex items-center space-x-4 text-sm text-gray-500">
                    <span>{{ formatDate(message.created_at) }}</span>
                    <span v-if="message.ip_hash">IP: {{ message.ip_hash }}</span>
                    <span v-if="message.is_deleted" class="text-red-600">已删除</span>
                  </div>
                </div>
                <button
                  v-if="!message.is_deleted"
                  @click="deleteAnonymousMessage(message.id)"
                  class="ml-4 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
                >
                  删除
                </button>
              </div>
            </div>

            <!-- 加载更多 -->
            <div v-if="hasMoreMessages" class="text-center py-4">
              <button
                @click="loadMoreMessages"
                :disabled="loadingMessages"
                class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50"
              >
                {{ loadingMessages ? '加载中...' : '加载更多' }}
              </button>
            </div>

            <!-- 空状态 -->
            <div v-if="anonymousMessages.length === 0 && !loadingMessages" class="text-center py-12 text-gray-500">
              暂无匿名消息
            </div>
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
import { anonymousAPI } from '../../api/anonymous'
import { formatDate } from '../../utils/date'

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

// 匿名消息管理
const anonymousMessages = ref([])
const loadingMessages = ref(false)
const hasMoreMessages = ref(true)
const currentMessagePage = ref(1)

// 检查管理员权限
if (!authStore.isAuthenticated || authStore.user?.role !== 'admin') {
  toastStore.error('需要管理员权限')
}

const adminTabs = [
  { key: 'posts', label: '文章管理' },
  { key: 'users', label: '用户管理' },
  { key: 'comments', label: '评论审核' },
  { key: 'anonymous', label: '匿名消息' },
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

// 加载匿名消息
const loadAnonymousMessages = async (reset = false) => {
  if (loadingMessages.value) return

  loadingMessages.value = true
  try {
    const page = reset ? 1 : currentMessagePage.value
    const response = await anonymousAPI.getAllMessages({
      page,
      limit: 20
    })

    const data = response.data

    if (reset) {
      anonymousMessages.value = data.items
      currentMessagePage.value = 1
    } else {
      anonymousMessages.value.push(...data.items)
    }

    hasMoreMessages.value = data.has_more
    currentMessagePage.value++
  } catch (error) {
    console.error('加载匿名消息失败:', error)
    toastStore.error('加载匿名消息失败')
  } finally {
    loadingMessages.value = false
  }
}

// 加载更多消息
const loadMoreMessages = () => {
  if (hasMoreMessages.value && !loadingMessages.value) {
    loadAnonymousMessages()
  }
}

// 删除匿名消息
const deleteAnonymousMessage = async (messageId) => {
  if (!confirm('确定要删除这条匿名消息吗？')) return

  try {
    await anonymousAPI.deleteMessage(messageId)
    toastStore.success('消息已删除')

    // 更新列表中的消息状态
    const message = anonymousMessages.value.find(msg => msg.id === messageId)
    if (message) {
      message.is_deleted = true
    }
  } catch (error) {
    console.error('删除消息失败:', error)
    const errorMsg = error.response?.data?.detail || '删除失败'
    toastStore.error(errorMsg)
  }
}

onMounted(() => {
  loadStats()
  // 如果默认显示匿名消息标签页，则加载消息
  if (activeTab.value === 'anonymous') {
    loadAnonymousMessages(true)
  }
})
</script>
