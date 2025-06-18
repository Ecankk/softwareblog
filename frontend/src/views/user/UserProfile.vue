<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="bg-white rounded-lg shadow-sm p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">个人中心</h1>
      
      <!-- 用户信息卡片 -->
      <div class="bg-gray-50 rounded-lg p-6 mb-8">
        <div class="flex items-center space-x-6">
          <div class="relative">
            <img
              :src="authStore.user?.avatar || '/placeholder.svg?height=80&width=80'"
              :alt="authStore.user?.username"
              class="w-20 h-20 rounded-full object-cover"
            />
            <button
              @click="$refs.avatarInput.click()"
              class="absolute bottom-0 right-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center hover:bg-blue-700 transition-colors"
              title="更换头像"
            >
              <Camera class="w-3 h-3" />
            </button>
            <input
              ref="avatarInput"
              type="file"
              accept="image/*"
              @change="handleAvatarChange"
              class="hidden"
            />
          </div>
          <div class="flex-1">
            <h2 class="text-xl font-semibold text-gray-900">{{ authStore.user?.username || authStore.user?.email }}</h2>
            <p class="text-gray-600 mt-1">{{ authStore.user?.bio || '这个人很懒，什么都没写' }}</p>
            <div class="flex items-center space-x-4 mt-2 text-sm text-gray-500">
              <span>{{ userStats.posts }} 篇文章</span>
              <span>{{ userStats.followers }} 关注者</span>
              <span>{{ userStats.following }} 关注中</span>
            </div>
          </div>
          <button
            @click="showEditProfile = true"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            编辑资料
          </button>
        </div>
      </div>
      
      <!-- 标签页 -->
      <div class="border-b border-gray-200 mb-6">
        <nav class="-mb-px flex space-x-8">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm',
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
      <div class="min-h-96">
        <!-- 我的文章 -->
        <div v-if="activeTab === 'posts'">
          <div v-if="userPosts.length > 0" class="space-y-4">
            <div 
              v-for="post in userPosts"
              :key="post.id"
              class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900 mb-2">{{ post.title }}</h3>
                  <p class="text-gray-600 text-sm mb-2">{{ post.summary }}</p>
                  <div class="flex items-center space-x-4 text-xs text-gray-500">
                    <span>{{ formatDate(post.created_at) }}</span>
                    <span>{{ post.views_count }} 浏览</span>
                    <span>{{ post.likes_count }} 点赞</span>
                    <span>{{ post.comments_count }} 评论</span>
                  </div>
                </div>
                <div class="flex items-center space-x-2 ml-4">
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
            </div>
          </div>
          <div v-else class="text-center py-12 text-gray-500">
            还没有发布任何文章
          </div>
        </div>
        
        <!-- 收藏的文章 -->
        <div v-else-if="activeTab === 'bookmarks'">
          <div class="text-center py-12 text-gray-500">
            暂无收藏的文章
          </div>
        </div>
        
        <!-- 关注的用户 -->
        <div v-else-if="activeTab === 'following'">
          <div class="text-center py-12 text-gray-500">
            暂无关注的用户
          </div>
        </div>
        
        <!-- 浏览历史 -->
        <div v-else-if="activeTab === 'history'">
          <div class="text-center py-12 text-gray-500">
            暂无浏览历史
          </div>
        </div>
      </div>
    </div>
    
    <!-- 编辑资料弹窗 -->
    <div v-if="showEditProfile" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">编辑个人资料</h3>
        
        <form @submit.prevent="updateProfile" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
            <input
              v-model="profileForm.username"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">个人简介</label>
            <textarea
              v-model="profileForm.bio"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="showEditProfile = false"
              class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              保存
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { Camera } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { usersAPI } from '../../api/users'
import { postsAPI } from '../../api/posts'
import { formatDate } from '../../utils/date'

const authStore = useAuthStore()
const toastStore = useToastStore()

const activeTab = ref('posts')
const showEditProfile = ref(false)
const userPosts = ref([])
const userStats = ref({
  posts: 0,
  followers: 0,
  following: 0
})

const profileForm = reactive({
  username: '',
  bio: ''
})

const tabs = [
  { key: 'posts', label: '我的文章' },
  { key: 'bookmarks', label: '收藏' },
  { key: 'following', label: '关注' },
  { key: 'history', label: '浏览历史' }
]

const loadUserData = async () => {
  try {
    // 获取用户详细信息
    const userResponse = await usersAPI.getUserProfile(authStore.user.id)
    const userData = userResponse.data

    userStats.value = {
      posts: userData.post_count || 0,
      followers: userData.followers_count || 0,
      following: userData.following_count || 0
    }

    // 获取用户的文章
    const postsResponse = await usersAPI.getUserPosts(authStore.user.id)
    userPosts.value = postsResponse.data
  } catch (error) {
    console.error('加载用户数据失败:', error)
    // 使用模拟数据作为后备
    userStats.value = {
      posts: 0,
      followers: 0,
      following: 0
    }
    userPosts.value = []
  }
}

const handleAvatarChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    toastStore.error('请选择图片文件')
    return
  }

  // 检查文件大小（限制为2MB）
  if (file.size > 2 * 1024 * 1024) {
    toastStore.error('图片大小不能超过2MB')
    return
  }

  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await usersAPI.uploadAvatar(authStore.user.id, formData)

    // 更新用户头像
    authStore.user.avatar = response.data.url
    toastStore.success('头像更新成功')
  } catch (error) {
    console.error('头像上传失败:', error)
    toastStore.error('头像上传失败')
  }
}

const updateProfile = async () => {
  const success = await authStore.updateProfile(profileForm)
  if (success) {
    showEditProfile.value = false
  }
}

const deletePost = async (postId) => {
  if (confirm('确定要删除这篇文章吗？')) {
    try {
      await postsAPI.deletePost(postId)
      userPosts.value = userPosts.value.filter(post => post.id !== postId)
      userStats.value.posts--
      toastStore.success('文章删除成功')
    } catch (error) {
      console.error('删除文章失败:', error)
      toastStore.error('删除失败')
    }
  }
}

onMounted(() => {
  loadUserData()
  
  // 初始化编辑表单
  profileForm.username = authStore.user?.username || ''
  profileForm.bio = authStore.user?.bio || ''
})
</script>
