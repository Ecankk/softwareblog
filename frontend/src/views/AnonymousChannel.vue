<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 页面头部 -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-4xl mx-auto px-4 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">匿名频道</h1>
            <p class="text-gray-600 mt-1">在这里自由表达你的想法，完全匿名</p>
          </div>
          <div class="flex items-center space-x-2 text-sm text-gray-500">
            <MessageCircle class="w-4 h-4" />
            <span>{{ totalMessages }} 条消息</span>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 py-6">
      
      <!-- 发送消息区域 -->
      <div class="bg-white rounded-lg shadow-sm border p-6 mb-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">发送匿名消息</h2>
        <form @submit.prevent="sendMessage" class="space-y-4">
          <div>
            <textarea
              v-model="newMessage"
              placeholder="在这里输入你的想法...（最多500字符）"
              rows="4"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              :disabled="sending"
            ></textarea>
            <div class="flex justify-between items-center mt-2">
              <span class="text-sm text-gray-500">
                {{ newMessage.length }}/500 字符
              </span>
              <button
                type="submit"
                :disabled="!newMessage.trim() || newMessage.length > 500 || sending"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                <span v-if="sending">发送中...</span>
                <span v-else>发送消息</span>
              </button>
            </div>
          </div>
        </form>
      </div>
      
      <!-- 消息列表 -->
      <div class="space-y-4">
        <div
          v-for="message in messages"
          :key="message.id"
          class="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow"
        >
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <p class="text-gray-900 whitespace-pre-wrap">{{ message.content }}</p>
              <div class="flex items-center space-x-4 mt-3 text-sm text-gray-500">
                <span class="flex items-center">
                  <Clock class="w-4 h-4 mr-1" />
                  {{ formatDate(message.created_at) }}
                </span>
                <span class="flex items-center">
                  <User class="w-4 h-4 mr-1" />
                  匿名用户
                </span>
              </div>
            </div>
            <!-- 管理员删除按钮 -->
            <button
              v-if="authStore.user?.role === 'admin'"
              @click="deleteMessage(message.id)"
              class="ml-4 p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              title="删除消息"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- 加载更多 -->
        <div v-if="hasMore" class="text-center py-4">
          <button
            @click="loadMore"
            :disabled="loading"
            class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 disabled:opacity-50 transition-colors"
          >
            <span v-if="loading">加载中...</span>
            <span v-else>加载更多</span>
          </button>
        </div>

        <!-- 没有更多消息 -->
        <div v-else-if="messages.length > 0" class="text-center py-4 text-gray-500">
          没有更多消息了
        </div>

        <!-- 空状态 -->
        <div v-if="messages.length === 0 && !loading" class="text-center py-12">
          <MessageCircle class="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">还没有消息</h3>
          <p class="text-gray-500">成为第一个发送匿名消息的人吧！</p>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading && messages.length === 0" class="text-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p class="text-gray-500 mt-2">加载中...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { MessageCircle, Clock, User, Trash2 } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useToastStore } from '../stores/toast'
import { anonymousAPI } from '../api/anonymous'
import { formatDate } from '../utils/date'

const authStore = useAuthStore()
const toastStore = useToastStore()

// 响应式数据
const messages = ref([])
const newMessage = ref('')
const loading = ref(false)
const sending = ref(false)
const hasMore = ref(true)
const currentPage = ref(1)
const totalMessages = ref(0)

// 加载消息列表
const loadMessages = async (reset = false) => {
  if (loading.value) return

  loading.value = true
  try {
    const page = reset ? 1 : currentPage.value
    const response = await anonymousAPI.getMessages({
      page,
      limit: 20
    })

    const data = response.data

    if (reset) {
      messages.value = data.items
      currentPage.value = 1
    } else {
      messages.value.push(...data.items)
    }

    hasMore.value = data.has_more
    totalMessages.value = data.total
    currentPage.value++
  } catch (error) {
    console.error('加载消息失败:', error)
    toastStore.error('加载消息失败')
  } finally {
    loading.value = false
  }
}

// 加载更多
const loadMore = () => {
  if (hasMore.value && !loading.value) {
    loadMessages()
  }
}

// 发送消息
const sendMessage = async () => {
  if (!newMessage.value.trim() || sending.value) return

  sending.value = true
  try {
    await anonymousAPI.sendMessage(newMessage.value.trim())
    newMessage.value = ''
    toastStore.success('消息发送成功')

    // 重新加载消息列表
    await loadMessages(true)
  } catch (error) {
    console.error('发送消息失败:', error)
    const errorMsg = error.response?.data?.detail || '发送失败'
    toastStore.error(errorMsg)
  } finally {
    sending.value = false
  }
}

// 删除消息（管理员）
const deleteMessage = async (messageId) => {
  if (!confirm('确定要删除这条消息吗？')) return

  try {
    await anonymousAPI.deleteMessage(messageId)
    toastStore.success('消息已删除')

    // 从列表中移除
    messages.value = messages.value.filter(msg => msg.id !== messageId)
    totalMessages.value--
  } catch (error) {
    console.error('删除消息失败:', error)
    const errorMsg = error.response?.data?.detail || '删除失败'
    toastStore.error(errorMsg)
  }
}

// 页面加载时获取消息
onMounted(() => {
  loadMessages(true)
})
</script>
