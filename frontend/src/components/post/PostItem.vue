<template>
  <article class="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-6">
    <!-- 作者信息 -->
    <div class="flex items-center space-x-3 mb-4">
      <router-link :to="`/user/${post.author.id}`">
        <img
          :src="getAvatarUrl(post.author)"
          :alt="post.author.username"
          class="w-10 h-10 rounded-full hover:ring-2 hover:ring-blue-500 transition-all"
        />
      </router-link>
      <div class="flex-1">
        <div class="flex items-center space-x-2">
          <router-link 
            :to="`/user/${post.author.id}`"
            class="font-medium text-gray-900 hover:text-blue-600"
          >
            {{ post.author.username }}
          </router-link>
          <span v-if="post.author.is_member" class="px-2 py-0.5 bg-yellow-100 text-yellow-800 text-xs rounded-full">
            会员
          </span>
        </div>
        <p class="text-sm text-gray-500">{{ formatDate(post.created_at) }}</p>
      </div>
      
      <!-- 更多操作 -->
      <div class="relative">
        <button 
          @click="showMenu = !showMenu"
          class="p-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100"
        >
          <MoreHorizontal class="w-4 h-4" />
        </button>
        
        <div 
          v-if="showMenu"
          class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10"
        >
          <button 
            @click="handleReport"
            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            举报
          </button>
          <button 
            v-if="canEdit"
            @click="handleEdit"
            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            编辑
          </button>
          <button 
            v-if="canDelete"
            @click="handleDelete"
            class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
          >
            删除
          </button>
        </div>
      </div>
    </div>
    
    <!-- 文章内容 -->
    <div class="mb-4">
      <router-link :to="`/post/${post.slug}`">
        <h2 class="text-xl font-semibold text-gray-900 mb-2 hover:text-blue-600 transition-colors">
          {{ post.title }}
        </h2>
      </router-link>
      
      <p class="text-gray-600 mb-3 line-clamp-3">
        {{ post.summary }}
      </p>
      
      <!-- 封面图 -->
      <div v-if="post.cover_image" class="mb-3">
        <router-link :to="`/post/${post.slug}`">
          <img 
            :src="post.cover_image"
            :alt="post.title"
            class="w-full h-48 object-cover rounded-lg hover:opacity-90 transition-opacity"
          />
        </router-link>
      </div>
      
      <!-- 标签 -->
      <div v-if="post.tags && post.tags.length > 0" class="flex flex-wrap gap-2 mb-3">
        <span 
          v-for="tag in post.tags"
          :key="tag.id"
          class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full hover:bg-gray-200 cursor-pointer"
        >
          {{ tag.name }}
        </span>
      </div>
    </div>
    
    <!-- 互动按钮 -->
    <div class="flex items-center justify-between pt-4 border-t border-gray-100">
      <div class="flex items-center space-x-6">
        <!-- 点赞 -->
        <button 
          @click="handleLike"
          :class="[
            'flex items-center space-x-1 text-sm transition-colors',
            post.is_liked 
              ? 'text-red-500 hover:text-red-600' 
              : 'text-gray-500 hover:text-red-500'
          ]"
        >
          <Heart :class="{ 'fill-current': post.is_liked }" class="w-4 h-4" />
          <span>{{ post.likes_count || 0 }}</span>
        </button>
        
        <!-- 评论 -->
        <router-link 
          :to="`/post/${post.slug}#comments`"
          class="flex items-center space-x-1 text-sm text-gray-500 hover:text-blue-500 transition-colors"
        >
          <MessageCircle class="w-4 h-4" />
          <span>{{ post.comments_count || 0 }}</span>
        </router-link>
        
        <!-- 浏览量 -->
        <div class="flex items-center space-x-1 text-sm text-gray-500">
          <Eye class="w-4 h-4" />
          <span>{{ post.views_count || 0 }}</span>
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <!-- 收藏 -->
        <button 
          @click="handleBookmark"
          :class="[
            'p-2 rounded-full transition-colors',
            post.is_bookmarked 
              ? 'text-yellow-500 hover:text-yellow-600 bg-yellow-50' 
              : 'text-gray-400 hover:text-yellow-500 hover:bg-yellow-50'
          ]"
        >
          <Bookmark :class="{ 'fill-current': post.is_bookmarked }" class="w-4 h-4" />
        </button>
        
        <!-- 分享 -->
        <button 
          @click="handleShare"
          class="p-2 text-gray-400 hover:text-blue-500 rounded-full hover:bg-blue-50 transition-colors"
        >
          <Share2 class="w-4 h-4" />
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Heart, 
  MessageCircle, 
  Eye, 
  Bookmark, 
  Share2, 
  MoreHorizontal 
} from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { postsAPI } from '../../api/posts'
import { formatDate } from '../../utils/date'

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['like', 'bookmark', 'share', 'delete'])

const router = useRouter()
const authStore = useAuthStore()

const showMenu = ref(false)

const canEdit = computed(() => {
  return authStore.isAuthenticated &&
         (authStore.user?.id === props.post.author.id || authStore.user?.role === 'admin')
})

const canDelete = computed(() => {
  return authStore.isAuthenticated &&
         (authStore.user?.id === props.post.author.id || authStore.user?.role === 'admin')
})

const handleLike = () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  emit('like', props.post.id, props.post.is_liked)
}

const handleBookmark = () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  emit('bookmark', props.post.id, props.post.is_bookmarked)
}

const handleShare = () => {
  emit('share', props.post)
}

const handleReport = () => {
  // 实现举报功能
  console.log('举报文章:', props.post.id)
}

const handleEdit = () => {
  router.push(`/edit-post/${props.post.id}`)
}

const handleDelete = async () => {
  if (confirm('确定要删除这篇文章吗？此操作不可撤销。')) {
    try {
      await postsAPI.deletePost(props.post.id)
      // 发出删除事件，让父组件处理
      emit('delete', props.post.id)
    } catch (error) {
      console.error('删除文章失败:', error)
      // 这里可以添加错误提示
    }
  }
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
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
