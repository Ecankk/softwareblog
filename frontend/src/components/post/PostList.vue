<template>
  <div class="space-y-6">
    <!-- 文章列表 -->
    <div v-if="posts.length > 0" class="space-y-4">
      <PostItem v-for="post in posts" :key="post.id" :post="post" @like="handleLike" @bookmark="handleBookmark"
        @share="handleShare" @delete="handleDelete" />
    </div>

    <!-- 空状态 -->
    <div v-else-if="!loading" class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
        <FileText class="w-12 h-12 text-gray-400" />
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">暂无文章</h3>
      <p class="text-gray-500">还没有发布任何文章</p>
    </div>

    <!-- 加载更多 -->
    <div v-if="hasMore" class="text-center py-6">
      <button @click="$emit('load-more')" :disabled="loading"
        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed">
        <span v-if="loading">加载中...</span>
        <span v-else>加载更多</span>
      </button>
    </div>

    <!-- 加载骨架屏 -->
    <div v-if="loading && posts.length === 0" class="space-y-4">
      <div v-for="i in 5" :key="i" class="bg-white rounded-lg shadow-sm p-6">
        <div class="animate-pulse">
          <div class="flex items-center space-x-3 mb-4">
            <div class="w-10 h-10 bg-gray-200 rounded-full"></div>
            <div class="flex-1">
              <div class="h-4 bg-gray-200 rounded w-1/4 mb-2"></div>
              <div class="h-3 bg-gray-200 rounded w-1/6"></div>
            </div>
          </div>
          <div class="h-6 bg-gray-200 rounded w-3/4 mb-3"></div>
          <div class="h-4 bg-gray-200 rounded w-full mb-2"></div>
          <div class="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FileText } from 'lucide-vue-next'
import PostItem from './PostItem.vue'
import { postsAPI } from '../../api/posts'
import { useToastStore } from '../../stores/toast'

const props = defineProps({
  posts: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  hasMore: {
    type: Boolean,
    default: false
  }
})

defineEmits(['load-more'])

const toastStore = useToastStore()

const handleLike = async (postId, isLiked) => {
  try {
    if (isLiked) {
      await postsAPI.unlikePost(postId)
    } else {
      await postsAPI.likePost(postId)
    }

    // 只有API调用成功后才更新状态
    const post = props.posts.find(p => p.id === postId)
    if (post) {
      post.is_liked = !isLiked
      post.likes_count = post.likes_count + (isLiked ? -1 : 1)
    }
  } catch (error) {
    console.error('点赞操作失败:', error)
    // 根据错误类型显示不同的消息
    if (error.response?.status === 400) {
      const errorMsg = error.response.data?.detail || '操作失败'
      if (errorMsg.includes('已经点赞')) {
        toastStore.warning('文章已经点赞过了')
      } else if (errorMsg.includes('未点赞')) {
        toastStore.warning('文章还未点赞')
      } else {
        toastStore.error(errorMsg)
      }
    } else {
      toastStore.error('网络错误，请稍后重试')
    }
  }
}

const handleBookmark = async (postId, isBookmarked) => {
  try {
    if (isBookmarked) {
      await postsAPI.unbookmarkPost(postId)
    } else {
      await postsAPI.bookmarkPost(postId)
    }

    // 只有API调用成功后才更新状态和显示消息
    const post = props.posts.find(p => p.id === postId)
    if (post) {
      post.is_bookmarked = !isBookmarked
      post.bookmarks_count = post.bookmarks_count + (isBookmarked ? -1 : 1)
    }

    // 显示成功消息
    if (isBookmarked) {
      toastStore.success('取消收藏成功')
    } else {
      toastStore.success('收藏成功')
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
    // 根据错误类型显示不同的消息
    if (error.response?.status === 400) {
      const errorMsg = error.response.data?.detail || '操作失败'
      if (errorMsg.includes('已经收藏')) {
        toastStore.warning('文章已经收藏过了')
      } else if (errorMsg.includes('未收藏')) {
        toastStore.warning('文章还未收藏')
      } else {
        toastStore.error(errorMsg)
      }
    } else {
      toastStore.error('网络错误，请稍后重试')
    }
  }
}

const handleShare = (post) => {
  // 实现分享功能
  if (navigator.share) {
    navigator.share({
      title: post.title,
      text: post.summary,
      url: window.location.origin + `/posts/${post.slug}`
    })
  } else {
    // 复制链接到剪贴板
    navigator.clipboard.writeText(window.location.origin + `/posts/${post.slug}`)
    toastStore.success('链接已复制到剪贴板')
  }
}

const handleDelete = (postId) => {
  // 发出删除事件，让父组件处理列表更新
  toastStore.success('文章删除成功')
  // 这里可以添加更多逻辑，比如从列表中移除文章
}
</script>
