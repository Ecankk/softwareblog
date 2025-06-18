<template>
  <div class="comment-list">
    <!-- 评论统计 -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-gray-900">
        评论 ({{ totalComments }})
      </h3>
      
      <!-- 排序选项 -->
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-500">排序：</span>
        <select 
          v-model="sortBy"
          @change="handleSortChange"
          class="text-sm border border-gray-300 rounded px-2 py-1 focus:outline-none focus:border-blue-500"
        >
          <option value="newest">最新</option>
          <option value="oldest">最早</option>
          <option value="likes">最热</option>
        </select>
      </div>
    </div>
    
    <!-- 评论表单 -->
    <div v-if="authStore.isAuthenticated" class="mb-8">
      <CommentForm 
        :post-id="postId"
        @submit="handleNewComment"
      />
    </div>
    
    <!-- 登录提示 -->
    <div v-else class="mb-8 p-4 bg-gray-50 rounded-lg text-center">
      <p class="text-gray-600 mb-3">登录后可以发表评论</p>
      <router-link 
        to="/login"
        class="inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      >
        立即登录
      </router-link>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
    
    <!-- 评论列表 -->
    <div v-else-if="topLevelComments.length > 0" class="space-y-6">
      <CommentItem
        v-for="comment in topLevelComments"
        :key="comment.id"
        :comment="comment"
        :post-id="postId"
        :replies="getChildComments(comment.id)"
        @delete="handleDeleteComment"
        @like="handleLikeComment"
        @reply="handleReplyComment"
      />
    </div>
    
    <!-- 空状态 -->
    <div v-else class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <MessageCircle class="w-16 h-16 mx-auto" />
      </div>
      <p class="text-gray-500 text-lg">暂无评论</p>
      <p class="text-gray-400 text-sm mt-2">成为第一个评论的人吧！</p>
    </div>
    
    <!-- 加载更多 -->
    <div v-if="hasMore && !loading" class="text-center mt-8">
      <button 
        @click="loadMore"
        class="px-6 py-2 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 transition-colors"
      >
        加载更多评论
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { MessageCircle } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { commentsAPI } from '../../api/comments'
import CommentForm from './CommentForm.vue'
import CommentItem from './CommentItem.vue'

const props = defineProps({
  postId: {
    type: Number,
    required: true
  }
})

const authStore = useAuthStore()
const toastStore = useToastStore()

const comments = ref([])
const loading = ref(false)
const sortBy = ref('newest')
const hasMore = ref(false)
const page = ref(1)

const totalComments = computed(() => comments.value.length)

const topLevelComments = computed(() => {
  const topLevel = comments.value.filter(comment => !comment.parentId)
  
  // 根据排序方式排序
  switch (sortBy.value) {
    case 'oldest':
      return topLevel.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
    case 'likes':
      return topLevel.sort((a, b) => (b.likes || 0) - (a.likes || 0))
    case 'newest':
    default:
      return topLevel.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  }
})

const getChildComments = (parentId) => {
  return comments.value.filter(comment => comment.parentId === parentId)
}

const loadComments = async () => {
  loading.value = true
  try {
    const response = await commentsAPI.getPostComments(props.postId)
    comments.value = response.data
  } catch (error) {
    console.error('加载评论失败:', error)
    toastStore.error('加载评论失败')
  } finally {
    loading.value = false
  }
}

const handleNewComment = (newComment) => {
  comments.value.unshift(newComment)
}

const handleReplyComment = (replyData) => {
  comments.value.push(replyData)
}

const handleDeleteComment = async (commentId) => {
  try {
    await commentsAPI.deleteComment(commentId)
    
    // 从列表中移除评论
    const index = comments.value.findIndex(c => c.id === commentId)
    if (index > -1) {
      comments.value.splice(index, 1)
    }
    
    toastStore.success('评论已删除')
  } catch (error) {
    console.error('删除评论失败:', error)
    toastStore.error('删除评论失败')
  }
}

const handleLikeComment = async (commentId) => {
  try {
    const response = await commentsAPI.likeComment(commentId)
    
    // 更新评论的点赞数
    const comment = comments.value.find(c => c.id === commentId)
    if (comment) {
      comment.likes = response.data.likes
    }
  } catch (error) {
    console.error('点赞失败:', error)
    toastStore.error('点赞失败')
  }
}

const handleSortChange = () => {
  // 排序逻辑在computed中处理
}

const loadMore = () => {
  // 实际应用中实现分页加载
  page.value++
}

onMounted(() => {
  loadComments()
})

// 监听postId变化，重新加载评论
watch(() => props.postId, () => {
  loadComments()
})
</script>

<style scoped>
.comment-list {
  @apply max-w-none;
}
</style>
