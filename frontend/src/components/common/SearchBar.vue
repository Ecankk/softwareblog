<template>
  <div class="relative">
    <div class="relative">
      <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
      <input
        v-model="searchQuery"
        @keyup.enter="handleSearch"
        @input="debouncedSearch"
        type="text"
        placeholder="搜索文章、用户、话题..."
        class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      />
    </div>
    
    <!-- 搜索建议 -->
    <div 
      v-if="showSuggestions && suggestions.length > 0"
      class="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50"
    >
      <div class="py-2">
        <div 
          v-for="suggestion in suggestions" 
          :key="suggestion.id"
          @click="selectSuggestion(suggestion)"
          class="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center space-x-3"
        >
          <div class="flex-shrink-0">
            <div 
              v-if="suggestion.type === 'post'"
              class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center"
            >
              <FileText class="w-4 h-4 text-blue-600" />
            </div>
            <div 
              v-else-if="suggestion.type === 'user'"
              class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center"
            >
              <User class="w-4 h-4 text-green-600" />
            </div>
            <div 
              v-else
              class="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center"
            >
              <Hash class="w-4 h-4 text-purple-600" />
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-900 truncate">
              {{ suggestion.title || suggestion.name }}
            </p>
            <p class="text-xs text-gray-500 truncate">
              {{ suggestion.description || suggestion.bio }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, FileText, User, Hash } from 'lucide-vue-next'
import { searchAPI } from '../../api/search'

const router = useRouter()

const searchQuery = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)
let searchTimeout = null

// 防抖搜索
const debouncedSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  if (searchQuery.value.trim().length < 2) {
    suggestions.value = []
    showSuggestions.value = false
    return
  }
  
  searchTimeout = setTimeout(async () => {
    try {
      const query = searchQuery.value.trim()

      // 如果查询为空，不显示建议
      if (!query) {
        suggestions.value = []
        showSuggestions.value = false
        return
      }

      const searchResults = []

      // 使用统一的API调用
      try {
        const postsResponse = await searchAPI.searchPosts(query, { limit: 3 })
        const posts = postsResponse.data.items || []
        posts.forEach(post => {
          searchResults.push({
            id: `post-${post.id}`,
            type: 'post',
            title: post.title,
            description: post.summary || '点击查看详情',
            slug: post.slug
          })
        })
      } catch (error) {
        console.log('文章搜索失败:', error)
      }

      try {
        const usersResponse = await searchAPI.searchUsers(query, { limit: 2 })
        const users = usersResponse.data.items || []
        users.forEach(user => {
          searchResults.push({
            id: `user-${user.id}`,
            type: 'user',
            name: user.username,
            bio: user.bio || '这个人很懒，什么都没写',
            userId: user.id
          })
        })
      } catch (error) {
        console.log('用户搜索失败:', error)
      }

      suggestions.value = searchResults.slice(0, 5) // 最多显示5个建议
      showSuggestions.value = suggestions.value.length > 0
    } catch (error) {
      console.error('获取搜索建议失败:', error)
      suggestions.value = []
      showSuggestions.value = false
    }
  }, 300)
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    showSuggestions.value = false
    router.push({
      name: 'Search',
      query: { q: searchQuery.value }
    })
  }
}

const selectSuggestion = (suggestion) => {
  showSuggestions.value = false

  if (suggestion.type === 'post') {
    router.push(`/post/${suggestion.slug}`)
  } else if (suggestion.type === 'user') {
    router.push(`/user/${suggestion.userId}`)
  } else if (suggestion.type === 'tag') {
    router.push({
      name: 'Search',
      query: { q: suggestion.name, type: 'tag' }
    })
  }
}

// 点击外部关闭建议框
const handleClickOutside = (event) => {
  const searchContainer = event.target.closest('.relative')
  if (!searchContainer) {
    showSuggestions.value = false
  }
}

// 监听路由变化，关闭建议框
watch(() => router.currentRoute.value, () => {
  showSuggestions.value = false
})

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
