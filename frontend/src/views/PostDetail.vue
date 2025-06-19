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
            <img :src="getAvatarUrl(post.author)" :alt="post.author?.username" class="w-12 h-12 rounded-full" />
            <div>
              <p class="font-medium text-gray-900">{{ post.author?.username }}</p>
              <p class="text-sm text-gray-500">{{ formatDate(post.created_at) }}</p>
            </div>
          </div>

          <!-- 文章操作 -->
          <div class="flex items-center space-x-2">
            <button @click="handleLike" :class="[
              'flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors',
              post.is_liked
                ? 'bg-red-50 text-red-600 hover:bg-red-100'
                : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
            ]">
              <Heart :class="{ 'fill-current': post.is_liked }" class="w-4 h-4" />
              <span>{{ post.likes_count || 0 }}</span>
            </button>

            <button @click="handleBookmark" :class="[
              'flex items-center space-x-1 px-3 py-2 rounded-lg transition-colors',
              post.is_bookmarked
                ? 'bg-yellow-50 text-yellow-600 hover:bg-yellow-100'
                : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
            ]">
              <Bookmark :class="{ 'fill-current': post.is_bookmarked }" class="w-4 h-4" />
              <span>收藏</span>
            </button>

            <button @click="handleShare"
              class="flex items-center space-x-1 px-3 py-2 bg-gray-50 text-gray-600 rounded-lg hover:bg-gray-100 transition-colors">
              <Share2 class="w-4 h-4" />
              <span>分享</span>
            </button>

            <!-- 打赏按钮 -->
            <DonateButton v-if="authStore.isAuthenticated && post.author_id !== authStore.user?.id"
              :authorName="post.author_name || '作者'" :authorId="post.author_id" variant="secondary" size="sm"
              text="打赏" />
          </div>
        </div>

        <!-- 标签 -->
        <div v-if="post.tags && post.tags.length > 0" class="flex flex-wrap gap-2 mt-4">
          <span v-for="tag in post.tags" :key="tag.id" class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
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
      <router-link to="/posts" class="text-blue-600 hover:text-blue-800">返回文章列表</router-link>
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
import DonateButton from '../components/DonateButton.vue'
import { marked } from 'marked'

const route = useRoute()
const authStore = useAuthStore()
const toastStore = useToastStore()

const post = ref(null)
const loading = ref(true)

// 处理YAML前置内容和渲染Markdown
const renderedContent = computed(() => {
  if (!post.value?.content) return ''

  let content = String(post.value.content)

  // 移除YAML前置内容 (--- 开头和结尾的部分)
  content = content.replace(/^---\s*\n[\s\S]*?\n---\s*\n/, '')

  try {
    // 配置marked选项
    const html = marked.parse(content, {
      breaks: true,
      gfm: true,
      sanitize: false
    })

    // 添加自定义样式
    return addCustomStyles(html)
  } catch (error) {
    console.error('Markdown渲染失败:', error)
    return `<p class="text-red-600">Markdown渲染失败: ${error.message}</p>`
  }
})

// 添加自定义样式的函数
const addCustomStyles = (html) => {
  if (!html) return ''

  return html
    // 标题样式
    .replace(/<h1>/g, '<h1 class="text-3xl font-bold mb-6 text-gray-900 border-b border-gray-200 pb-2 mt-8">')
    .replace(/<h2>/g, '<h2 class="text-2xl font-bold mb-4 text-gray-900 mt-8">')
    .replace(/<h3>/g, '<h3 class="text-xl font-semibold mb-3 text-gray-900 mt-6">')
    .replace(/<h4>/g, '<h4 class="text-lg font-semibold mb-2 text-gray-800 mt-4">')
    .replace(/<h5>/g, '<h5 class="text-base font-semibold mb-2 text-gray-800 mt-4">')
    .replace(/<h6>/g, '<h6 class="text-sm font-semibold mb-2 text-gray-700 mt-4">')
    // 段落样式
    .replace(/<p>/g, '<p class="mb-4 text-gray-700 leading-relaxed">')
    // 链接样式
    .replace(/<a /g, '<a class="text-blue-600 hover:text-blue-800 underline transition-colors" target="_blank" rel="noopener noreferrer" ')
    // 代码块样式
    .replace(/<pre><code class="language-(\w+)">/g, '<div class="my-6"><div class="bg-gray-800 text-white px-4 py-2 text-sm font-mono rounded-t-lg"><span class="text-gray-300">$1</span></div><pre class="bg-gray-900 text-gray-100 p-4 rounded-b-lg overflow-x-auto"><code class="text-sm language-$1">')
    .replace(/<pre><code>/g, '<div class="my-6"><div class="bg-gray-800 text-white px-4 py-2 text-sm font-mono rounded-t-lg"><span class="text-gray-300">text</span></div><pre class="bg-gray-900 text-gray-100 p-4 rounded-b-lg overflow-x-auto"><code class="text-sm">')
    .replace(/<\/code><\/pre>/g, '</code></pre></div>')
    // 行内代码样式
    .replace(/<code>/g, '<code class="bg-gray-100 text-red-600 px-2 py-1 rounded text-sm font-mono">')
    // 引用样式
    .replace(/<blockquote>/g, '<blockquote class="border-l-4 border-blue-500 pl-4 py-2 my-6 bg-blue-50 text-gray-700 italic">')
    // 列表样式
    .replace(/<ul>/g, '<ul class="list-disc list-inside mb-4 space-y-2 text-gray-700">')
    .replace(/<ol>/g, '<ol class="list-decimal list-inside mb-4 space-y-2 text-gray-700">')
    .replace(/<li>/g, '<li class="leading-relaxed">')
    // 表格样式
    .replace(/<table>/g, '<div class="my-6 overflow-x-auto"><table class="min-w-full border border-gray-200 rounded-lg overflow-hidden">')
    .replace(/<\/table>/g, '</table></div>')
    .replace(/<thead>/g, '<thead class="bg-gray-50">')
    .replace(/<tbody>/g, '<tbody class="bg-white divide-y divide-gray-200">')
    .replace(/<th>/g, '<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">')
    .replace(/<td>/g, '<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">')
    // 水平线样式
    .replace(/<hr>/g, '<hr class="my-8 border-gray-300">')
    // 图片样式 - 添加错误处理
    .replace(/<img /g, '<div class="my-6 text-center"><img class="max-w-full h-auto rounded-lg shadow-md mx-auto" onerror="this.style.display=\'none\'; this.nextElementSibling.style.display=\'block\';" ')
    .replace(/<\/img>/g, '/><div style="display:none;" class="text-gray-500 text-sm mt-2">图片加载失败</div></div>')
}

// HTML转义函数
const escapeHtml = (text) => {
  const div = document.createElement('div')
  div.textContent = text
  return div.innerHTML
}

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
    } else {
      await postsAPI.likePost(post.value.id)
    }

    // 只有API调用成功后才更新状态
    post.value.is_liked = !post.value.is_liked
    post.value.likes_count = post.value.likes_count + (post.value.is_liked ? 1 : -1)
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

const handleBookmark = async () => {
  if (!authStore.isAuthenticated) {
    toastStore.error('请先登录')
    return
  }

  try {
    if (post.value.is_bookmarked) {
      await postsAPI.unbookmarkPost(post.value.id)
    } else {
      await postsAPI.bookmarkPost(post.value.id)
    }

    // 只有API调用成功后才更新状态和显示消息
    post.value.is_bookmarked = !post.value.is_bookmarked

    // 显示成功消息
    if (post.value.is_bookmarked) {
      toastStore.success('收藏成功')
    } else {
      toastStore.success('已取消收藏')
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

// 导入头像工具函数
import { getAvatarUrl } from '../utils/avatar'



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
