<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">加载中...</p>
    </div>
    
    <div v-else-if="user" class="space-y-8">
      <!-- 用户信息卡片 -->
      <div class="bg-white rounded-lg shadow-sm p-8">
        <div class="flex flex-col md:flex-row items-start md:items-center space-y-4 md:space-y-0 md:space-x-6">
          <!-- 头像 -->
          <img 
            :src="getAvatarUrl(user)"
            :alt="user.username"
            class="w-24 h-24 rounded-full mx-auto md:mx-0"
          />
          
          <!-- 用户信息 -->
          <div class="flex-1 text-center md:text-left">
            <h1 class="text-3xl font-bold text-gray-900">{{ user.username || user.email }}</h1>
            <p v-if="user.bio" class="text-gray-600 mt-2">{{ user.bio }}</p>
            <div class="flex justify-center md:justify-start items-center space-x-6 mt-4 text-sm text-gray-500">
              <span>{{ user.followers_count || 0 }} 粉丝</span>
              <span>{{ user.following_count || 0 }} 关注</span>
              <span>{{ userPosts.length }} 文章</span>
            </div>
          </div>
          
          <!-- 操作按钮 -->
          <div class="flex space-x-3">
            <!-- 关注按钮（非本人时显示） -->
            <FollowButton
              v-if="authStore.isAuthenticated && authStore.user?.id !== user.id"
              :userId="user.id"
              :initialFollowStatus="isFollowing"
              :key="`follow-${user.id}-${isFollowing}`"
              @follow-changed="handleFollowChanged"
            />
            
            <!-- 编辑资料按钮（本人时显示） -->
            <router-link
              v-if="authStore.isAuthenticated && authStore.user?.id === user.id"
              to="/profile"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              编辑资料
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- 标签页导航 -->
      <div class="bg-white rounded-lg shadow-sm">
        <div class="border-b border-gray-200">
          <nav class="flex space-x-8 px-6">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="activeTab = tab.key"
              :class="[
                'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
                activeTab === tab.key
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>
        
        <!-- 标签页内容 -->
        <div class="p-6">
          <!-- 文章列表 -->
          <div v-if="activeTab === 'posts'">
            <div v-if="userPosts.length === 0" class="text-center py-12 text-gray-500">
              <FileText class="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>暂无发布的文章</p>
            </div>
            
            <div v-else class="space-y-6">
              <article
                v-for="post in userPosts"
                :key="post.id"
                class="border-b border-gray-200 pb-6 last:border-b-0"
              >
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <router-link
                      :to="`/post/${post.slug}`"
                      class="block group"
                    >
                      <h3 class="text-xl font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                        {{ post.title }}
                      </h3>
                    </router-link>
                    
                    <p v-if="post.summary" class="text-gray-600 mt-2 line-clamp-2">
                      {{ post.summary }}
                    </p>
                    
                    <div class="flex items-center space-x-4 mt-4 text-sm text-gray-500">
                      <span>{{ formatDate(post.created_at) }}</span>
                      <span>{{ post.views || 0 }} 阅读</span>
                      <span>{{ post.likes || 0 }} 点赞</span>
                    </div>
                    
                    <!-- 标签 -->
                    <div v-if="post.tags && post.tags.length > 0" class="flex flex-wrap gap-2 mt-3">
                      <span
                        v-for="tag in post.tags"
                        :key="tag"
                        class="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full"
                      >
                        {{ tag }}
                      </span>
                    </div>
                  </div>
                  
                  <!-- 编辑/删除按钮（仅作者可见） -->
                  <div v-if="authStore.user?.id === user.id" class="ml-4 flex space-x-2">
                    <router-link
                      :to="`/edit-post/${post.id}`"
                      class="text-blue-600 hover:text-blue-800 text-sm"
                    >
                      编辑
                    </router-link>
                    <button
                      @click="deletePost(post.id)"
                      class="text-red-600 hover:text-red-800 text-sm"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </article>
            </div>
          </div>
          
          <!-- 关注列表 -->
          <div v-else-if="activeTab === 'following'">
            <div v-if="followingList.length === 0" class="text-center py-12 text-gray-500">
              <Users class="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>暂无关注的用户</p>
            </div>
            
            <div v-else class="grid md:grid-cols-2 gap-4">
              <div
                v-for="followUser in followingList"
                :key="followUser.id"
                class="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <img 
                    :src="getAvatarUrl(followUser)"
                    :alt="followUser.username"
                    class="w-10 h-10 rounded-full cursor-pointer"
                    @click="$router.push(`/user/${followUser.id}`)"
                  />
                  <div>
                    <p 
                      class="font-medium text-gray-900 cursor-pointer hover:text-blue-600"
                      @click="$router.push(`/user/${followUser.id}`)"
                    >
                      {{ followUser.username }}
                    </p>
                    <p class="text-sm text-gray-500">{{ followUser.followers_count || 0 }} 粉丝</p>
                  </div>
                </div>
                
                <FollowButton
                  v-if="authStore.isAuthenticated && authStore.user?.id !== followUser.id"
                  :userId="followUser.id"
                  :initialFollowStatus="followUser.is_following"
                />
              </div>
            </div>
          </div>
          
          <!-- 粉丝列表 -->
          <div v-else-if="activeTab === 'followers'">
            <div v-if="followersList.length === 0" class="text-center py-12 text-gray-500">
              <Users class="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p>暂无粉丝</p>
            </div>
            
            <div v-else class="grid md:grid-cols-2 gap-4">
              <div
                v-for="follower in followersList"
                :key="follower.id"
                class="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <img 
                    :src="getAvatarUrl(follower)"
                    :alt="follower.username"
                    class="w-10 h-10 rounded-full cursor-pointer"
                    @click="$router.push(`/user/${follower.id}`)"
                  />
                  <div>
                    <p 
                      class="font-medium text-gray-900 cursor-pointer hover:text-blue-600"
                      @click="$router.push(`/user/${follower.id}`)"
                    >
                      {{ follower.username }}
                    </p>
                    <p class="text-sm text-gray-500">{{ follower.followers_count || 0 }} 粉丝</p>
                  </div>
                </div>
                
                <FollowButton
                  v-if="authStore.isAuthenticated && authStore.user?.id !== follower.id"
                  :userId="follower.id"
                  :initialFollowStatus="follower.is_following"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-12">
      <p class="text-gray-500">用户不存在</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { FileText, Users } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useToastStore } from '../stores/toast'
import { usersAPI } from '../api/users'
import { postsAPI } from '../api/posts'
import { followsAPI } from '../api/follows'
import FollowButton from '../components/user/FollowButton.vue'

const route = useRoute()
const authStore = useAuthStore()
const toastStore = useToastStore()

const user = ref(null)
const userPosts = ref([])
const followingList = ref([])
const followersList = ref([])
const loading = ref(true)
const activeTab = ref('posts')
const isFollowing = ref(false)

const tabs = [
  { key: 'posts', label: '文章' },
  { key: 'following', label: '关注' },
  { key: 'followers', label: '粉丝' }
]

// 导入头像工具函数
import { getAvatarUrl } from '../utils/avatar'

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const loadUserData = async (userId) => {
  loading.value = true
  // 重置关注状态
  isFollowing.value = false

  try {
    // 加载用户信息
    const userResponse = await usersAPI.getUserById(userId)
    user.value = userResponse.data

    // 如果是其他用户且已登录，立即检查关注状态
    if (authStore.isAuthenticated && authStore.user?.id !== parseInt(userId)) {
      try {
        const followStatusResponse = await followsAPI.checkFollowStatus(userId)
        isFollowing.value = followStatusResponse.data.isFollowing
      } catch (error) {
        console.error('检查关注状态失败:', error)
        isFollowing.value = false
      }
    }

    // 并行加载其他数据
    const [postsResponse, followingResponse, followersResponse] = await Promise.all([
      postsAPI.getUserPosts(userId),
      followsAPI.getUserFollowing(userId),
      followsAPI.getUserFollowers(userId)
    ])

    userPosts.value = postsResponse.data
    followingList.value = followingResponse.data
    followersList.value = followersResponse.data

  } catch (error) {
    console.error('加载用户数据失败:', error)
    toastStore.error('加载用户信息失败')
  } finally {
    loading.value = false
  }
}

const handleFollowChanged = (data) => {
  // 更新本地关注状态
  isFollowing.value = data.isFollowing

  // 更新粉丝数
  if (user.value) {
    user.value.followers_count += data.isFollowing ? 1 : -1
  }
}

const deletePost = async (postId) => {
  if (!confirm('确定要删除这篇文章吗？')) return
  
  try {
    await postsAPI.deletePost(postId)
    userPosts.value = userPosts.value.filter(post => post.id !== postId)
    toastStore.success('文章删除成功')
  } catch (error) {
    console.error('删除文章失败:', error)
    toastStore.error('删除文章失败')
  }
}

// 监听路由变化
watch(() => route.params.id, (newId) => {
  if (newId) {
    loadUserData(parseInt(newId))
  }
}, { immediate: true })

onMounted(() => {
  const userId = parseInt(route.params.id)
  if (userId) {
    loadUserData(userId)
  }
})
</script>
