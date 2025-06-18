<template>
  <div class="comment-form">
    <div class="flex space-x-3">
      <!-- 当前用户头像 -->
      <div class="flex-shrink-0">
        <img 
          :src="authStore.user?.avatar || '/placeholder.svg?height=40&width=40'" 
          :alt="authStore.user?.username"
          class="w-10 h-10 rounded-full"
        />
      </div>
      
      <!-- 评论输入区域 -->
      <div class="flex-1">
        <div class="border border-gray-300 rounded-lg overflow-hidden focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500">
          <textarea
            v-model="content"
            :placeholder="placeholder"
            rows="3"
            class="w-full p-3 border-none resize-none focus:outline-none"
            @keydown.ctrl.enter="handleSubmit"
          ></textarea>
          
          <!-- 工具栏 -->
          <div class="bg-gray-50 px-3 py-2 flex items-center justify-between">
            <div class="flex items-center space-x-2 text-sm text-gray-500">
              <span>Ctrl + Enter 快速发布</span>
            </div>
            
            <div class="flex items-center space-x-2">
              <button
                v-if="showCancel"
                @click="handleCancel"
                type="button"
                class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 transition-colors"
              >
                取消
              </button>
              <button
                @click="handleSubmit"
                :disabled="!content.trim() || isSubmitting"
                class="px-4 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <span v-if="isSubmitting">发布中...</span>
                <span v-else>{{ submitText }}</span>
              </button>
            </div>
          </div>
        </div>
        
        <!-- 错误提示 -->
        <div v-if="error" class="mt-2 text-sm text-red-600">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { commentsAPI } from '../../api/comments'

const props = defineProps({
  postId: {
    type: Number,
    required: true
  },
  parentId: {
    type: Number,
    default: null
  },
  placeholder: {
    type: String,
    default: '写下你的评论...'
  },
  submitText: {
    type: String,
    default: '发布评论'
  },
  showCancel: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'cancel'])

const authStore = useAuthStore()
const toastStore = useToastStore()

const content = ref('')
const isSubmitting = ref(false)
const error = ref('')

const handleSubmit = async () => {
  if (!content.value.trim()) {
    error.value = '评论内容不能为空'
    return
  }
  
  if (!authStore.isAuthenticated) {
    toastStore.error('请先登录')
    return
  }
  
  isSubmitting.value = true
  error.value = ''
  
  try {
    const commentData = {
      content: content.value.trim(),
      parentId: props.parentId
    }
    
    const response = await commentsAPI.createComment(props.postId, commentData)
    
    emit('submit', response.data)
    content.value = ''
    toastStore.success('评论发布成功')
  } catch (err) {
    console.error('发布评论失败:', err)
    error.value = err.response?.data?.detail || '发布评论失败'
  } finally {
    isSubmitting.value = false
  }
}

const handleCancel = () => {
  content.value = ''
  error.value = ''
  emit('cancel')
}
</script>

<style scoped>
.comment-form {
  @apply mb-6;
}
</style>
