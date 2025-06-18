<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>
    
    <div v-else-if="post" class="bg-white rounded-lg shadow-sm">
      <!-- 文章头部 -->
      <div class="p-6 border-b border-gray-200">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ post.title }}</h1>
        
        <!-- 作者信息 -->
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <img
              :src="getAvatarUrl(post.author)"
              :alt="post.author?.username"
              class="w-12 h-12 rounded-full"
            />
            <div>
              <p class="font-medium text-gray-900">{{ post.author?.username }}</p>
              <p class="text-sm text-gray-500">{{ formatDate(post.created_at) }}</p>
            </div>
          </div>
          
          <!-- 文章操作 -->
          <div class="flex items-center space-x-2">
            <button 
              @click="handleLike"
              :class="[
                'flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors',
                post.is_liked 
                  ? 'bg-red-50 text-red-600 hover:bg-red-100' 
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              ]"
            >
              <Heart :class="{ 'fill-current': post.is_liked }" class="w-4 h-4" />
              <span>{{ post.likes_count || 0 }}</span>
            </button>
            
            <button 
              @click="handleBookmark"
              :class="[
                'flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors',
                post.is_bookmarked 
                  ? 'bg-yellow-50 text-yellow-600 hover:bg-yellow-100' 
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              ]"
            >
              <Bookmark :class="{ 'fill-current': post.is_bookmarked }" class="w-4 h-4" />
              <span>收藏</span>
            </button>
            
            <button 
              @click="handleShare"
              class="flex items-center space-x-1 px-3 py-2 bg-gray-50 text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <Share2 class="w-4 h-4" />
              <span>分享</span>
            </button>
          </div>
        </div>
        
        <!-- 标签 -->
        <div v-if="post.tags && post.tags.length > 0" class="flex flex-wrap gap-2 mt-4">
          <span 
            v-for="tag in post.tags"
            :key="tag.id"
            class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
          >
            {{ tag.name }}
          </span>
        </div>
      </div>
      
      <!-- 文章内容 -->
      <div class="p-6">
        <div class="prose prose-lg max-w-none" v-html="renderedContent"></div>
      </div>
      
      <!-- 评论区域 -->
      <div class="border-t border-gray-200 p-6">
        <CommentList :post-id="post.id" />
      </div>
    </div>
    
    <div v-else class="text-center py-12">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">文章不存在</h2>
      <p class="text-gray-600 mb-4">抱歉，您访问的文章不存在或已被删除。</p>
      <router-link to="/" class="text-blue-600 hover:text-blue-800">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Heart, Bookmark, Share2 } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useToastStore } from '../stores/toast'
import { postsAPI } from '../api/posts'
import { usersAPI } from '../api/users'
import { formatDate } from '../utils/date'
import CommentList from '../components/comment/CommentList.vue'

const route = useRoute()
const authStore = useAuthStore()
const toastStore = useToastStore()

const post = ref(null)
const loading = ref(true)

// 简单的Markdown渲染
const renderedContent = computed(() => {
  if (!post.value?.content) return ''
  
  let html = post.value.content
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*)\*/gim, '<em>$1</em>')
    .replace(/!\[([^\]]*)\]$$([^)]*)$$/gim, '<img alt="$1" src="$2" class="max-w-full h-auto rounded" />')
    .replace(/\[([^\]]*)\]$$([^)]*)$$/gim, '<a href="$2" class="text-blue-600 hover:text-blue-800 underline">$1</a>')
    .replace(/\n\n/gim, '</p><p>')
    .replace(/\n/gim, '<br>')
  
  return `<p>${html}</p>`
})

const loadPost = async () => {
  try {
    const response = await postsAPI.getPost(route.params.slug)
    post.value = response.data
  } catch (error) {
    console.error('加载文章失败:', error)
    post.value = null
  } finally {
    loading.value = false
  }
}

const handleLike = async () => {
  if (!authStore.isAuthenticated) {
    toastStore.error('请先登录')
    return
  }
  
  try {
    if (post.value.is_liked) {
      await postsAPI.unlikePost(post.value.id)
      post.value.likes_count--
    } else {
      await postsAPI.likePost(post.value.id)
      post.value.likes_count++
    }
    post.value.is_liked = !post.value.is_liked
  } catch (error) {
    toastStore.error('操作失败')
  }
}

const handleBookmark = async () => {
  if (!authStore.isAuthenticated) {
    toastStore.error('请先登录')
    return
  }
  
  try {
    if (post.value.is_bookmarked) {
      await postsAPI.unbookmarkPost(post.value.id)
      toastStore.success('已取消收藏')
    } else {
      await postsAPI.bookmarkPost(post.value.id)
      toastStore.success('收藏成功')
    }
    post.value.is_bookmarked = !post.value.is_bookmarked
  } catch (error) {
    toastStore.error('操作失败')
  }
}

const handleShare = () => {
  if (navigator.share) {
    navigator.share({
      title: post.value.title,
      text: post.value.summary,
      url: window.location.href
    })
  } else {
    navigator.clipboard.writeText(window.location.href)
    toastStore.success('链接已复制到剪贴板')
  }
}

// 获取头像URL的辅助函数
const getAvatarUrl = (user) => {
  if (!user) return '/placeholder.svg?height=48&width=48'

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



// 记录浏览历史
const recordHistory = async () => {
  if (authStore.isAuthenticated && post.value) {
    try {
      await usersAPI.addUserHistory(authStore.user.id, post.value.id)
    } catch (error) {
      console.error('记录浏览历史失败:', error)
    }
  }
}

onMounted(() => {
  loadPost()
})

// 监听文章加载完成，记录浏览历史
watch(post, (newPost) => {
  if (newPost) {
    recordHistory()
  }
})
</script>

<style scoped>
.prose h1 {
  @apply text-2xl font-bold mb-4 text-gray-900;
}

.prose h2 {
  @apply text-xl font-bold mb-3 text-gray-900;
}

.prose h3 {
  @apply text-lg font-bold mb-2 text-gray-900;
}

.prose p {
  @apply mb-4 text-gray-700 leading-relaxed;
}

.prose strong {
  @apply font-bold text-gray-900;
}

.prose em {
  @apply italic;
}
</style>
