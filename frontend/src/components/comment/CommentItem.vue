<template>
  <div class="comment-item">
    <div class="flex space-x-3">
      <!-- 用户头像 -->
      <div class="flex-shrink-0">
        <img
          :src="getAvatarUrl(comment.author)"
          :alt="comment.author?.username"
          class="w-10 h-10 rounded-full"
        />
      </div>
      
      <!-- 评论内容 -->
      <div class="flex-1 min-w-0">
        <div class="bg-gray-50 rounded-lg p-3">
          <!-- 用户名和时间 -->
          <div class="flex items-center space-x-2 mb-2">
            <span class="font-medium text-gray-900">
              {{ comment.author?.username || '匿名用户' }}
            </span>
            <span class="text-sm text-gray-500">
              {{ formatDate(comment.created_at) }}
            </span>
          </div>
          
          <!-- 评论文本 -->
          <p class="text-gray-700 text-sm leading-relaxed">
            {{ comment.content }}
          </p>
        </div>
        
        <!-- 操作按钮 -->
        <div class="flex items-center space-x-4 mt-2 text-sm">
          <button 
            @click="handleLike"
            :class="[
              'flex items-center space-x-1 hover:text-blue-600 transition-colors',
              isLiked ? 'text-blue-600' : 'text-gray-500'
            ]"
          >
            <Heart :class="['w-4 h-4', isLiked && 'fill-current']" />
            <span>{{ comment.likes || 0 }}</span>
          </button>
          
          <button 
            @click="handleReply"
            class="flex items-center space-x-1 text-gray-500 hover:text-blue-600 transition-colors"
          >
            <MessageCircle class="w-4 h-4" />
            <span>回复</span>
          </button>
          
          <button 
            v-if="canDelete"
            @click="handleDelete"
            class="flex items-center space-x-1 text-gray-500 hover:text-red-600 transition-colors"
          >
            <Trash2 class="w-4 h-4" />
            <span>删除</span>
          </button>
        </div>
        
        <!-- 回复表单 -->
        <div v-if="showReplyForm" class="mt-3">
          <CommentForm 
            :post-id="postId"
            :parent-id="comment.id"
            placeholder="回复评论..."
            @submit="handleReplySubmit"
            @cancel="showReplyForm = false"
          />
        </div>
        
        <!-- 子评论 -->
        <div v-if="replies.length > 0" class="mt-4 space-y-3">
          <CommentItem
            v-for="reply in replies"
            :key="reply.id"
            :comment="reply"
            :post-id="postId"
            :replies="getChildReplies(reply.id)"
            @delete="$emit('delete', $event)"
            @like="$emit('like', $event)"
            @reply="$emit('reply', $event)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Heart, MessageCircle, Trash2 } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import CommentForm from './CommentForm.vue'

const props = defineProps({
  comment: {
    type: Object,
    required: true
  },
  postId: {
    type: Number,
    required: true
  },
  replies: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['delete', 'like', 'reply'])

const authStore = useAuthStore()
const showReplyForm = ref(false)
const isLiked = ref(false) // 实际应用中需要从后端获取用户是否已点赞

const canDelete = computed(() => {
  return authStore.isAuthenticated && (
    authStore.user?.id === props.comment.authorId ||
    authStore.user?.role === 'admin'
  )
})

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

const getChildReplies = (parentId) => {
  return props.replies.filter(reply => reply.parentId === parentId)
}

const handleLike = () => {
  emit('like', props.comment.id)
}

const handleReply = () => {
  if (!authStore.isAuthenticated) {
    // 提示用户登录
    return
  }
  showReplyForm.value = !showReplyForm.value
}

const handleDelete = () => {
  if (confirm('确定要删除这条评论吗？')) {
    emit('delete', props.comment.id)
  }
}

const handleReplySubmit = (replyData) => {
  emit('reply', replyData)
  showReplyForm.value = false
}

// 获取头像URL的辅助函数
const getAvatarUrl = (user) => {
  if (!user) return '/placeholder.svg?height=40&width=40'

  if (user.avatar && user.avatar.startsWith('/users/')) {
    // 如果是SVG头像路径，添加后端服务器地址
    return `http://localhost:8000${user.avatar}`
  } else if (user.avatar) {
    // 如果是其他头像路径，直接使用
    return user.avatar
  } else {
    // 如果没有头像，使用默认SVG头像
    return `http://localhost:8000/users/${user.id}/avatar.svg`
  }
}
</script>

<style scoped>
.comment-item {
  @apply border-b border-gray-100 pb-4 last:border-b-0;
}
</style>
