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
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, FileText, User, Hash } from 'lucide-vue-next'

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
      // 模拟API调用
      suggestions.value = [
        {
          id: 1,
          type: 'post',
          title: '如何使用Vue 3构建现代Web应用',
          description: '详细介绍Vue 3的新特性和最佳实践',
          slug: 'vue3-modern-web-apps'
        },
        {
          id: 2,
          type: 'user',
          name: '张三',
          bio: '前端开发工程师',
        },
        {
          id: 3,
          type: 'tag',
          name: 'Vue.js',
          description: 'Vue.js相关文章'
        }
      ]
      showSuggestions.value = true
    } catch (error) {
      console.error('获取搜索建议失败:', error)
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
    router.push(`/user/${suggestion.id}`)
  } else {
    router.push({
      name: 'Search',
      query: { q: suggestion.name, type: 'tag' }
    })
  }
}

// 监听路由变化，关闭建议框
watch(() => router.currentRoute.value, () => {
  showSuggestions.value = false
})
</script>
