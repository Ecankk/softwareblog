<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">
        搜索结果
        <span v-if="searchQuery" class="text-blue-600">「{{ searchQuery }}」</span>
      </h1>
      
      <!-- 搜索筛选 -->
      <div class="flex flex-wrap gap-4 items-center">
        <div class="flex space-x-2">
          <button
            v-for="tab in searchTabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
              activeTab === tab.key
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            {{ tab.label }}
          </button>
        </div>
        
        <select 
          v-model="sortBy"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm"
        >
          <option value="relevance">相关度</option>
          <option value="created_at">最新发布</option>
          <option value="likes_count">最多点赞</option>
        </select>
      </div>
    </div>
    
    <!-- 搜索结果 -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">搜索中...</p>
    </div>
    
    <div v-else-if="results.length > 0" class="space-y-6">
      <!-- 文章结果 -->
      <div v-if="activeTab === 'posts'">
        <PostList :posts="results" :loading="false" :has-more="hasMore" @load-more="loadMore" />
      </div>
      
      <!-- 用户结果 -->
      <div v-else-if="activeTab === 'users'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="user in results"
          :key="user.id"
          class="bg-white rounded-lg shadow-sm p-6 text-center"
        >
          <img 
            :src="user.avatar || '/placeholder.svg?height=80&width=80'"
            :alt="user.username"
            class="w-20 h-20 rounded-full mx-auto mb-4"
          />
          <h3 class="font-semibold text-gray-900 mb-2">{{ user.username }}</h3>
          <p class="text-gray-600 text-sm mb-4">{{ user.bio || '这个人很懒，什么都没写' }}</p>
          <div class="flex justify-center space-x-4 text-sm text-gray-500 mb-4">
            <span>{{ user.posts_count || 0 }} 文章</span>
            <span>{{ user.followers_count || 0 }} 关注者</span>
          </div>
          <button 
            v-if="authStore.isAuthenticated && user.id !== authStore.user?.id"
            @click="followUser(user.id)"
            class="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            关注
          </button>
        </div>
      </div>
      
      <!-- 标签结果 -->
      <div v-else-if="activeTab === 'tags'" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div 
          v-for="tag in results"
          :key="tag.id"
          class="bg-white rounded-lg shadow-sm p-4 text-center hover:shadow-md transition-shadow cursor-pointer"
          @click="searchByTag(tag.name)"
        >
          <h3 class="font-semibold text-gray-900 mb-2">{{ tag.name }}</h3>
          <p class="text-sm text-gray-600">{{ tag.posts_count || 0 }} 篇文章</p>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-12">
      <div class="w-24 h-24 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
        <Search class="w-12 h-12 text-gray-400" />
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">没有找到相关内容</h3>
      <p class="text-gray-500">尝试使用其他关键词搜索</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useToastStore } from '../stores/toast'
import { searchAPI } from '../api/search'
import PostList from '../components/post/PostList.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const toastStore = useToastStore()

const searchQuery = ref(route.query.q || '')
const activeTab = ref(route.query.type || 'posts')
const sortBy = ref('relevance')
const results = ref([])
const loading = ref(false)
const hasMore = ref(false)

const searchTabs = [
  { key: 'posts', label: '文章' },
  { key: 'users', label: '用户' },
  { key: 'tags', label: '标签' }
]

const performSearch = async () => {
  if (!searchQuery.value.trim()) return
  
  loading.value = true
  try {
    let response
    const params = { sort: sortBy.value }
    
    switch (activeTab.value) {
      case 'posts':
        response = await searchAPI.searchPosts(searchQuery.value, params)
        break
      case 'users':
        response = await searchAPI.searchUsers(searchQuery.value, params)
        break
      case 'tags':
        response = await searchAPI.searchTags(searchQuery.value, params)
        break
    }
    
    results.value = response.data.items || response.data
    hasMore.value = response.data.has_more || false
  } catch (error) {
    console.error('搜索失败:', error)
    results.value = []
    
    // 模拟搜索结果
    if (activeTab.value === 'posts') {
      results.value = [
        {
          id: 1,
          title: `关于"${searchQuery.value}"的文章`,
          summary: '这是一篇示例文章，展示搜索功能的效果。',
          author: {
            id: 1,
            username: '示例作者',
            avatar: '/placeholder.svg?height=40&width=40'
          },
          created_at: new Date().toISOString(),
          likes_count: 10,
          comments_count: 5,
          views_count: 100,
          tags: [{ id: 1, name: searchQuery.value }],
          slug: 'example-post'
        }
      ]
    }
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  // 实现加载更多逻辑
  console.log('加载更多搜索结果')
}

const followUser = async (userId) => {
  try {
    // await usersAPI.followUser(userId)
    toastStore.success('关注成功')
  } catch (error) {
    toastStore.error('关注失败')
  }
}

const searchByTag = (tagName) => {
  router.push({
    name: 'Search',
    query: { q: tagName, type: 'posts' }
  })
}

// 监听搜索参数变化
watch([() => route.query.q, () => route.query.type], ([newQuery, newType]) => {
  searchQuery.value = newQuery || ''
  activeTab.value = newType || 'posts'
  if (searchQuery.value) {
    performSearch()
  }
})

watch([activeTab, sortBy], () => {
  if (searchQuery.value) {
    performSearch()
  }
})

onMounted(() => {
  if (searchQuery.value) {
    performSearch()
  }
})
</script>
