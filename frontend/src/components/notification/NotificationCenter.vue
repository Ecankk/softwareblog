<template>
  <div class="relative">
    <!-- 通知铃铛按钮 -->
    <button
      @click="toggleNotifications"
      class="relative p-2 text-gray-600 hover:text-gray-900 transition-colors"
    >
      <Bell class="w-6 h-6" />
      <!-- 未读通知徽章 -->
      <span
        v-if="unreadCount > 0"
        class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
      >
        {{ unreadCount > 99 ? '99+' : unreadCount }}
      </span>
    </button>

    <!-- 通知下拉面板 -->
    <div
      v-if="showNotifications"
      class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
    >
      <!-- 头部 -->
      <div class="flex items-center justify-between p-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">通知</h3>
        <div class="flex items-center space-x-2">
          <button
            v-if="unreadCount > 0"
            @click="markAllAsRead"
            class="text-sm text-blue-600 hover:text-blue-800"
          >
            全部已读
          </button>
          <button
            @click="showNotifications = false"
            class="text-gray-400 hover:text-gray-600"
          >
            <X class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- 通知列表 -->
      <div class="max-h-96 overflow-y-auto">
        <div v-if="loading" class="p-4 text-center text-gray-500">
          加载中...
        </div>
        
        <div v-else-if="notifications.length === 0" class="p-8 text-center text-gray-500">
          <Bell class="w-12 h-12 mx-auto mb-4 text-gray-300" />
          <p>暂无通知</p>
        </div>
        
        <div v-else class="divide-y divide-gray-100">
          <div
            v-for="notification in notifications"
            :key="notification.id"
            @click="handleNotificationClick(notification)"
            :class="[
              'p-4 hover:bg-gray-50 cursor-pointer transition-colors',
              !notification.isRead && 'bg-blue-50'
            ]"
          >
            <div class="flex items-start space-x-3">
              <!-- 通知图标 -->
              <div
                :class="[
                  'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
                  getNotificationIconClass(notification.type)
                ]"
              >
                <component :is="getNotificationIcon(notification.type)" class="w-4 h-4" />
              </div>
              
              <!-- 通知内容 -->
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900">
                  {{ notification.title }}
                </p>
                <p class="text-sm text-gray-600 mt-1">
                  {{ notification.content }}
                </p>
                <p class="text-xs text-gray-400 mt-2">
                  {{ formatDate(notification.created_at) }}
                </p>
              </div>
              
              <!-- 未读标识 -->
              <div v-if="!notification.isRead" class="flex-shrink-0">
                <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 查看全部 -->
      <div class="p-4 border-t border-gray-200">
        <router-link
          to="/notifications"
          @click="showNotifications = false"
          class="block text-center text-sm text-blue-600 hover:text-blue-800"
        >
          查看全部通知
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Bell, X, Heart, MessageCircle, UserPlus } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { notificationsAPI } from '../../api/notifications'

const authStore = useAuthStore()
const toastStore = useToastStore()

const showNotifications = ref(false)
const notifications = ref([])
const loading = ref(false)
const unreadCount = ref(0)

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) {
    loadNotifications()
  }
}

const loadNotifications = async () => {
  if (!authStore.isAuthenticated) return

  loading.value = true
  try {
    const response = await notificationsAPI.getNotifications({ limit: 10 })
    notifications.value = response.data.items
    unreadCount.value = response.data.unread_count
  } catch (error) {
    console.error('加载通知失败:', error)
  } finally {
    loading.value = false
  }
}

const loadUnreadCount = async () => {
  if (!authStore.isAuthenticated) return

  try {
    const response = await notificationsAPI.getUnreadCount()
    unreadCount.value = response.data.count
  } catch (error) {
    console.error('加载未读通知数量失败:', error)
  }
}

const markAllAsRead = async () => {
  try {
    await notificationsAPI.markAllAsRead()
    notifications.value.forEach(n => n.isRead = true)
    unreadCount.value = 0
    toastStore.success('已标记所有通知为已读')
  } catch (error) {
    console.error('标记已读失败:', error)
    toastStore.error('操作失败')
  }
}

const handleNotificationClick = async (notification) => {
  // 标记为已读
  if (!notification.isRead) {
    try {
      await notificationsAPI.markAsRead(notification.id)
      notification.isRead = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    } catch (error) {
      console.error('标记已读失败:', error)
    }
  }

  // 根据通知类型跳转
  showNotifications.value = false
  // 这里可以添加跳转逻辑
}

const getNotificationIcon = (type) => {
  switch (type) {
    case 'follow':
      return UserPlus
    case 'like':
      return Heart
    case 'comment':
      return MessageCircle
    default:
      return Bell
  }
}

const getNotificationIconClass = (type) => {
  switch (type) {
    case 'follow':
      return 'bg-blue-100 text-blue-600'
    case 'like':
      return 'bg-red-100 text-red-600'
    case 'comment':
      return 'bg-green-100 text-green-600'
    default:
      return 'bg-gray-100 text-gray-600'
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN')
}

// 定期检查未读通知数量
onMounted(() => {
  loadUnreadCount()
  
  // 每30秒检查一次未读通知
  setInterval(() => {
    if (authStore.isAuthenticated) {
      loadUnreadCount()
    }
  }, 30000)
})

// 点击外部关闭通知面板
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showNotifications.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
