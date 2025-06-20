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
                @click="switchTab(tab)"
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
import { useToastStore } from '../stores/toast'
import { postsAPI } from '../api/posts'
import { tagsAPI } from '../api/tags'
import { usersAPI } from '../api/users'
import { followsAPI } from '../api/follows'
import PostList from '../components/post/PostList.vue'

const authStore = useAuthStore()
const toastStore = useToastStore()

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
  { key: 'latest', label: '最新', sort: 'created_at' },
  { key: 'hot', label: '热门', sort: 'views_count' },
  { key: 'following', label: '关注', sort: 'created_at', requiresAuth: true }
]

// 切换标签页
const switchTab = (tab) => {
  activeTab.value = tab.key
  sortBy.value = tab.sort
}

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

// 导入头像工具函数
import { getAvatarUrl } from '../utils/avatar'

const filterByTag = (tagName) => {
  selectedTag.value = tagName
}

const followAuthor = async (authorId) => {
  if (!authStore.isAuthenticated) {
    toastStore.error('请先登录')
    return
  }

  try {
    await followsAPI.followUser(authorId)
    toastStore.success('关注成功')
    // 更新推荐作者列表
    loadRecommendedAuthors()
  } catch (error) {
    console.error('关注失败:', error)
    toastStore.error('关注失败')
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
