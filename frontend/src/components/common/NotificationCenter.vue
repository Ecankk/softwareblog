<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-hidden">
    <div class="absolute inset-0 bg-black bg-opacity-50" @click="close"></div>
    <div class="absolute right-0 top-0 h-full w-96 bg-white shadow-xl">
      <div class="flex flex-col h-full">
        <!-- 头部 -->
        <div class="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">通知中心</h2>
          <button @click="close" class="text-gray-400 hover:text-gray-600">
            <X class="w-5 h-5" />
          </button>
        </div>
        
        <!-- 通知列表 -->
        <div class="flex-1 overflow-y-auto">
          <div v-if="notifications.length === 0" class="p-8 text-center">
            <Bell class="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p class="text-gray-500">暂无通知</p>
          </div>
          
          <div v-else class="divide-y divide-gray-200">
            <div
              v-for="notification in notifications"
              :key="notification.id"
              :class="[
                'p-4 hover:bg-gray-50 cursor-pointer',
                !notification.is_read && 'bg-blue-50'
              ]"
              @click="handleNotificationClick(notification)"
            >
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0">
                  <div :class="getNotificationIconClass(notification.type)">
                    <component :is="getNotificationIcon(notification.type)" class="w-4 h-4" />
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900">
                    {{ notification.title }}
                  </p>
                  <p class="text-sm text-gray-500 mt-1">
                    {{ notification.content }}
                  </p>
                  <p class="text-xs text-gray-400 mt-2">
                    {{ formatDate(notification.created_at) }}
                  </p>
                </div>
                <div v-if="!notification.is_read" class="w-2 h-2 bg-blue-500 rounded-full"></div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 底部操作 -->
        <div class="p-4 border-t border-gray-200">
          <button
            @click="markAllAsRead"
            class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            全部标记为已读
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { X, Bell, Heart, MessageCircle, UserPlus, AlertTriangle } from 'lucide-vue-next'
import { notificationsAPI } from '../../api/notifications'
import { formatDate } from '../../utils/date'

const show = ref(false)
const notifications = ref([])

const getNotificationIcon = (type) => {
  const icons = {
    like: Heart,
    comment: MessageCircle,
    follow: UserPlus,
    system: AlertTriangle
  }
  return icons[type] || Bell
}

const getNotificationIconClass = (type) => {
  const classes = {
    like: 'w-8 h-8 bg-red-100 text-red-600 rounded-full flex items-center justify-center',
    comment: 'w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center',
    follow: 'w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center',
    system: 'w-8 h-8 bg-yellow-100 text-yellow-600 rounded-full flex items-center justify-center'
  }
  return classes[type] || 'w-8 h-8 bg-gray-100 text-gray-600 rounded-full flex items-center justify-center'
}

const open = () => {
  show.value = true
  loadNotifications()
}

const close = () => {
  show.value = false
}

const loadNotifications = async () => {
  try {
    const response = await notificationsAPI.getNotifications()
    notifications.value = response.data
  } catch (error) {
    console.error('加载通知失败:', error)
  }
}

const handleNotificationClick = async (notification) => {
  if (!notification.is_read) {
    try {
      await notificationsAPI.markAsRead(notification.id)
      notification.is_read = true
    } catch (error) {
      console.error('标记通知已读失败:', error)
    }
  }
  
  // 根据通知类型跳转到相应页面
  if (notification.link) {
    window.location.href = notification.link
  }
}

const markAllAsRead = async () => {
  try {
    await notificationsAPI.markAllAsRead()
    notifications.value.forEach(n => n.is_read = true)
  } catch (error) {
    console.error('标记全部已读失败:', error)
  }
}

defineExpose({
  open,
  close
})
</script>
