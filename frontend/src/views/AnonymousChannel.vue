<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-900 mb-2">匿名频道</h1>
        <p class="text-gray-600">在这里，你可以匿名分享想法和讨论话题</p>
      </div>
      
      <!-- 发布匿名消息 -->
      <div class="bg-gray-50 rounded-lg p-6 mb-8">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">发布匿名消息</h3>
        <textarea
          v-model="newMessage"
          rows="4"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="分享你的想法..."
        ></textarea>
        <div class="mt-4 flex justify-end">
          <button
            @click="submitMessage"
            :disabled="!newMessage.trim() || submitting"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ submitting ? '发布中...' : '匿名发布' }}
          </button>
        </div>
      </div>
      
      <!-- 匿名消息列表 -->
      <div class="space-y-6">
        <div 
          v-for="message in messages"
          :key="message.id"
          class="bg-gray-50 rounded-lg p-6"
        >
          <div class="flex items-start space-x-4">
            <div class="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
              <span class="text-gray-600 font-medium">匿</span>
            </div>
            <div class="flex-1">
              <p class="text-gray-900 mb-2">{{ message.content }}</p>
              <div class="flex items-center space-x-4 text-sm text-gray-500">
                <span>{{ formatDate(message.created_at) }}</span>
                <button 
                  @click="likeMessage(message.id)"
                  :class="[
                    'flex items-center space-x-1',
                    message.is_liked ? 'text-red-500' : 'text-gray-500 hover:text-red-500'
                  ]"
                >
                  <Heart :class="{ 'fill-current': message.is_liked }" class="w-4 h-4" />
                  <span>{{ message.likes_count || 0 }}</span>
                </button>
                <button class="text-gray-500 hover:text-blue-500">
                  回复
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="messages.length === 0" class="text-center py-12 text-gray-500">
          还没有匿名消息，来发布第一条吧！
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Heart } from 'lucide-vue-next'
import { useToastStore } from '../stores/toast'
import { formatDate } from '../utils/date'

const toastStore = useToastStore()

const newMessage = ref('')
const submitting = ref(false)
const messages = ref([])

const submitMessage = async () => {
  if (!newMessage.value.trim()) return
  
  submitting.value = true
  try {
    // 模拟提交匿名消息
    const message = {
      id: Date.now(),
      content: newMessage.value,
      created_at: new Date().toISOString(),
      likes_count: 0,
      is_liked: false
    }
    
    messages.value.unshift(message)
    newMessage.value = ''
    toastStore.success('匿名消息发布成功')
  } catch (error) {
    toastStore.error('发布失败')
  } finally {
    submitting.value = false
  }
}

const likeMessage = async (messageId) => {
  const message = messages.value.find(m => m.id === messageId)
  if (message) {
    if (message.is_liked) {
      message.likes_count--
    } else {
      message.likes_count++
    }
    message.is_liked = !message.is_liked
  }
}

onMounted(() => {
  // 模拟加载匿名消息
  messages.value = [
    {
      id: 1,
      content: '今天心情不错，想和大家分享一下最近学到的新技术...',
      created_at: new Date(Date.now() - 3600000).toISOString(),
      likes_count: 5,
      is_liked: false
    },
    {
      id: 2,
      content: '有没有人和我一样觉得学习编程很有趣？',
      created_at: new Date(Date.now() - 7200000).toISOString(),
      likes_count: 3,
      is_liked: false
    }
  ]
})
</script>
