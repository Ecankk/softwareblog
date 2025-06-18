<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex flex-col lg:flex-row gap-8">
      <!-- 主内容区域 -->
      <div class="flex-1">
        <!-- 筛选和排序 -->
        <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div class="flex flex-wrap gap-2">
              <button
                v-for="tab in tabs"
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
            
            <div class="flex items-center gap-4">
              <!-- 标签筛选 -->
              <select 
                v-model="selectedTag"
                class="border border-gray-300 rounded-lg px-3 py-2 text-sm"
              >
                <option value="">所有标签</option>
                <option v-for="tag in tags" :key="tag.id" :value="tag.name">
                  {{ tag.name }}
                </option>
              </select>
              
              <!-- 排序方式 -->
              <select 
                v-model="sortBy"
                class="border border-gray-300 rounded-lg px-3 py-2 text-sm"
              >
                <option value="created_at">最新发布</option>
                <option value="likes_count">最多点赞</option>
                <option value="comments_count">最多评论</option>
                <option value="views_count">最多浏览</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- 文章列表 -->
        <PostList 
          :posts="posts"
          :loading="loading"
          :has-more="hasMore"
          @load-more="loadMore"
        />
      </div>
      
      <!-- 侧边栏 -->
      <div class="w-full lg:w-80">
        <div class="space-y-6">
          <!-- 热门标签 -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">热门标签</h3>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="tag in popularTags"
                :key="tag.id"
                @click="filterByTag(tag.name)"
                class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors"
              >
                {{ tag.name }}
                <span class="ml-1 text-xs text-gray-500">{{ tag.count }}</span>
              </button>
            </div>
          </div>
          
          <!-- 推荐作者 -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">推荐作者</h3>
            <div class="space-y-4">
              <div 
                v-for="author in recommendedAuthors"
                :key="author.id"
                class="flex items-center justify-between"
              >
                <div class="flex items-center space-x-3">
                  <img
                    :src="getAvatarUrl(author)"
                    :alt="author.username"
                    class="w-10 h-10 rounded-full cursor-pointer hover:opacity-80 transition-opacity"
                    @click="$router.push(`/user/${author.id}`)"
                  />
                  <div>
                    <p
                      class="font-medium text-gray-900 cursor-pointer hover:text-blue-600 transition-colors"
                      @click="$router.push(`/user/${author.id}`)"
                    >
                      {{ author.username }}
                    </p>
                    <p class="text-sm text-gray-500">{{ author.posts_count }} 篇文章</p>
                  </div>
                </div>
                <button 
                  v-if="authStore.isAuthenticated"
                  @click="followAuthor(author.id)"
                  class="px-3 py-1 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
                >
                  关注
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { postsAPI } from '../api/posts'
import { tagsAPI } from '../api/tags'
import { usersAPI } from '../api/users'
import PostList from '../components/post/PostList.vue'

const authStore = useAuthStore()

const posts = ref([])
const tags = ref([])
const popularTags = ref([])
const recommendedAuthors = ref([])
const loading = ref(false)
const hasMore = ref(true)
const currentPage = ref(1)

const activeTab = ref('latest')
const selectedTag = ref('')
const sortBy = ref('created_at')

const tabs = [
  { key: 'latest', label: '最新' },
  { key: 'hot', label: '热门' },
  { key: 'following', label: '关注', requiresAuth: true }
]

// It's important to call `useAuthStore` outside of conditional blocks.
useAuthStore();

const loadPosts = async (reset = false) => {
  if (loading.value) return
  
  loading.value = true
  try {
    const params = {
      page: reset ? 1 : currentPage.value,
      sort: sortBy.value,
      tag: selectedTag.value,
      type: activeTab.value
    }
    
    const response = await postsAPI.getPosts(params)
    
    if (reset) {
      posts.value = response.data.items
      currentPage.value = 1
    } else {
      posts.value.push(...response.data.items)
    }
    
    hasMore.value = response.data.has_more
    currentPage.value++
  } catch (error) {
    console.error('加载文章失败:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  if (hasMore.value && !loading.value) {
    loadPosts()
  }
}

const loadTags = async () => {
  try {
    const tagsResponse = await tagsAPI.getTags()
    tags.value = tagsResponse.data
    // 使用前5个标签作为热门标签
    popularTags.value = tagsResponse.data.slice(0, 5).map(tag => ({
      ...tag,
      count: tag.post_count || 0
    }))
  } catch (error) {
    console.error('加载标签失败:', error)
  }
}

const loadRecommendedAuthors = async () => {
  try {
    // 暂时使用模拟数据，因为后端还没有推荐作者接口
    recommendedAuthors.value = [
      {
        id: 1,
        username: "管理员",
        avatar: "/users/1/avatar.svg",
        posts_count: 1
      },
      {
        id: 3,
        username: "前端开发者",
        avatar: "/users/3/avatar.svg",
        posts_count: 1
      },
      {
        id: 4,
        username: "后端工程师",
        avatar: "/users/4/avatar.svg",
        posts_count: 1
      }
    ]
  } catch (error) {
    console.error('加载推荐作者失败:', error)
  }
}

// 获取头像URL的辅助函数
const getAvatarUrl = (user) => {
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

const filterByTag = (tagName) => {
  selectedTag.value = tagName
}

const followAuthor = async (authorId) => {
  try {
    await usersAPI.followUser(authorId)
    // 更新推荐作者列表
    loadRecommendedAuthors()
  } catch (error) {
    console.error('关注失败:', error)
  }
}

// 监听筛选条件变化
watch([activeTab, selectedTag, sortBy], () => {
  loadPosts(true)
})

onMounted(() => {
  loadPosts(true)
  loadTags()
  loadRecommendedAuthors()
})
</script>
