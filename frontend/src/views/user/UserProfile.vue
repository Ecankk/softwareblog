<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="bg-white rounded-lg shadow-sm p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">个人中心</h1>

      <!-- 用户信息卡片 -->
      <div class="bg-gray-50 rounded-lg p-6 mb-8">
        <div class="flex items-center space-x-6">
          <div class="relative">
            <img :src="getAvatarUrl(currentUser?.avatar)" :alt="currentUser?.username"
              class="w-20 h-20 rounded-full object-cover" @error="handleAvatarError" />
            <button v-if="isOwnProfile" @click="$refs.avatarInput.click()"
              class="absolute bottom-0 right-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center hover:bg-blue-700 transition-colors"
              title="更换头像">
              <Camera class="w-3 h-3" />
            </button>
            <input ref="avatarInput" type="file" accept="image/*" @change="handleAvatarChange" class="hidden" />
          </div>
          <div class="flex-1">
            <h2 class="text-xl font-semibold text-gray-900">{{ currentUser?.username || currentUser?.email }}</h2>
            <p class="text-gray-600 mt-1">{{ currentUser?.bio || '这个人很懒，什么都没写' }}</p>
            <div class="flex items-center space-x-4 mt-2 text-sm text-gray-500">
              <span>{{ userStats.posts }} 篇文章</span>
              <span>{{ userStats.followers }} 关注者</span>
              <span>{{ userStats.following }} 关注中</span>
            </div>
          </div>
          <!-- 操作按钮区域 -->
          <div class="flex items-center space-x-3">
            <!-- 自己的资料页面 -->
            <button v-if="isOwnProfile" @click="showEditProfile = true"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              编辑资料
            </button>

            <!-- 其他用户的资料页面 -->
            <template v-else-if="authStore.isAuthenticated">
              <!-- 关注按钮 -->
              <button @click="toggleFollow()" :class="[
                'px-4 py-2 rounded-lg transition-colors',
                isFollowing
                  ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              ]">
                {{ isFollowing ? '已关注' : '关注' }}
              </button>

              <!-- 打赏按钮 -->
              <DonateButton :authorName="currentUser?.username || '作者'" :authorId="viewingUserId" variant="secondary"
                size="md" />
            </template>
          </div>
        </div>
      </div>

      <!-- 标签页 -->
      <div class="border-b border-gray-200 mb-6">
        <nav class="-mb-px flex space-x-8">
          <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key" :class="[
            'py-2 px-1 border-b-2 font-medium text-sm',
            activeTab === tab.key
              ? 'border-blue-500 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]">
            {{ tab.label }}
          </button>
        </nav>
      </div>

      <!-- 标签页内容 -->
      <div class="min-h-96">
        <!-- 我的文章 -->
        <div v-if="activeTab === 'posts'">
          <div v-if="userPosts.length > 0" class="space-y-4">
            <div v-for="post in userPosts" :key="post.id"
              class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
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
                <div v-if="canEditPost(post)" class="flex items-center space-x-2 ml-4">
                  <router-link :to="`/edit-post/${post.id}`" class="text-blue-600 hover:text-blue-800 text-sm">
                    编辑
                  </router-link>
                  <button @click="deletePost(post.id)" class="text-red-600 hover:text-red-800 text-sm">
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
          <div v-if="userBookmarks.length > 0" class="space-y-4">
            <div v-for="post in userBookmarks" :key="post.id"
              class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <router-link :to="`/posts/${post.slug}`"
                    class="font-semibold text-gray-900 hover:text-blue-600 mb-2 block">
                    {{ post.title }}
                  </router-link>
                  <p class="text-gray-600 text-sm mb-2">{{ post.summary }}</p>
                  <div class="flex items-center space-x-4 text-xs text-gray-500">
                    <span>收藏于 {{ formatDate(post.bookmarked_at) }}</span>
                    <span>{{ post.views_count }} 浏览</span>
                    <span>{{ post.likes_count }} 点赞</span>
                    <span>{{ post.comments_count }} 评论</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-12 text-gray-500">
            暂无收藏的文章
          </div>
        </div>

        <!-- 关注的用户 -->
        <div v-else-if="activeTab === 'following'">
          <div v-if="userFollowing.length > 0" class="space-y-4">
            <div v-for="user in userFollowing" :key="user.id"
              class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <img :src="getAvatarUrl(user.avatar)" :alt="user.username"
                    class="w-12 h-12 rounded-full object-cover cursor-pointer hover:ring-2 hover:ring-blue-500 transition-all"
                    @click="goToUserProfile(user.id)" @error="handleAvatarError" />
                  <div>
                    <h3 class="font-semibold text-gray-900 cursor-pointer hover:text-blue-600 transition-colors"
                      @click="goToUserProfile(user.id)">
                      {{ user.username }}
                    </h3>
                    <p class="text-sm text-gray-600">{{ user.bio || '这个人很懒，什么都没写' }}</p>
                    <p class="text-xs text-gray-500">{{ user.followers_count }} 关注者</p>
                  </div>
                </div>
                <!-- 在关注列表中显示取消关注按钮 -->
                <button v-if="!isOwnProfile && authStore.isAuthenticated && activeTab === 'following'"
                  @click="unfollowUser(user)"
                  class="px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors text-sm">
                  取消关注
                </button>
                <!-- 在其他地方显示关注/已关注按钮 -->
                <button v-else-if="!isOwnProfile && authStore.isAuthenticated && activeTab !== 'following'"
                  @click="toggleFollowUser(user)" :class="[
                    'px-4 py-2 rounded-lg transition-colors text-sm',
                    user.is_following
                      ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  ]">
                  {{ user.is_following ? '已关注' : '关注' }}
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-12 text-gray-500">
            暂无关注的用户
          </div>
        </div>

        <!-- 浏览历史 -->
        <div v-else-if="activeTab === 'history'">
          <div v-if="userHistory.length > 0" class="space-y-4">
            <div v-for="post in userHistory" :key="post.id"
              class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <router-link :to="`/posts/${post.slug}`"
                    class="font-semibold text-gray-900 hover:text-blue-600 mb-2 block">
                    {{ post.title }}
                  </router-link>
                  <p class="text-gray-600 text-sm mb-2">{{ post.summary }}</p>
                  <div class="flex items-center space-x-4 text-xs text-gray-500">
                    <span>访问于 {{ formatDate(post.visited_at) }}</span>
                    <span>{{ post.views_count }} 浏览</span>
                    <span>{{ post.likes_count }} 点赞</span>
                    <span>{{ post.comments_count }} 评论</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-12 text-gray-500">
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
            <input v-model="profileForm.username" type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">个人简介</label>
            <textarea v-model="profileForm.bio" rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"></textarea>
          </div>

          <div class="flex justify-end space-x-3">
            <button type="button" @click="showEditProfile = false"
              class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300">
              取消
            </button>
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              保存
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Camera } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { usersAPI } from '../../api/users'
import { postsAPI } from '../../api/posts'
import { followsAPI } from '../../api/follows'
import { formatDate } from '../../utils/date'
import { getAvatarUrl as getAvatarUrlUtil, handleAvatarError as handleAvatarErrorUtil } from '../../utils/avatar'
import DonateButton from '../../components/DonateButton.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const toastStore = useToastStore()

const activeTab = ref('posts')
const showEditProfile = ref(false)
const userPosts = ref([])
const userBookmarks = ref([])
const userHistory = ref([])
const userFollowing = ref([])
const currentUser = ref(null)
const isFollowing = ref(false) // 当前用户是否关注了这个用户
const userStats = ref({
  posts: 0,
  followers: 0,
  following: 0
})

// 计算当前查看的用户ID
const viewingUserId = computed(() => {
  return parseInt(route.params.id) || authStore.user?.id
})

// 判断是否是查看自己的资料
const isOwnProfile = computed(() => {
  return viewingUserId.value === authStore.user?.id
})

const profileForm = reactive({
  username: '',
  bio: ''
})

// 计算可用的标签页
const tabs = computed(() => {
  const baseTabs = [
    { key: 'posts', label: isOwnProfile.value ? '我的文章' : '文章' }
  ]

  // 只有查看自己的资料时才显示这些标签页
  if (isOwnProfile.value) {
    baseTabs.push(
      { key: 'bookmarks', label: '收藏' },
      { key: 'following', label: '关注' },
      { key: 'history', label: '浏览历史' }
    )
  }

  return baseTabs
})

const loadUserData = async () => {
  try {
    const userId = viewingUserId.value

    // 获取用户详细信息
    const userResponse = await usersAPI.getUserProfile(userId)
    const userData = userResponse.data
    currentUser.value = userData

    userStats.value = {
      posts: userData.post_count || 0,
      followers: userData.followers_count || 0,
      following: userData.following_count || 0
    }

    // 如果不是查看自己的资料，检查关注状态
    if (!isOwnProfile.value && authStore.isAuthenticated) {
      try {
        const followStatusResponse = await followsAPI.checkFollowStatus(userId)
        isFollowing.value = followStatusResponse.data.is_following || false
      } catch (error) {
        console.error('检查关注状态失败:', error)
        isFollowing.value = false
      }
    } else {
      isFollowing.value = false
    }

    // 获取用户的文章
    const postsResponse = await usersAPI.getUserPosts(userId)
    userPosts.value = postsResponse.data.items || postsResponse.data

    // 如果是查看自己的资料，获取收藏列表和浏览历史
    if (isOwnProfile.value) {
      try {
        const bookmarksResponse = await usersAPI.getUserBookmarks(userId)
        userBookmarks.value = bookmarksResponse.data.items || bookmarksResponse.data
      } catch (error) {
        console.error('加载收藏失败:', error)
        userBookmarks.value = []
      }

      try {
        const historyResponse = await usersAPI.getUserHistory(userId)
        userHistory.value = historyResponse.data || []
      } catch (error) {
        console.error('加载浏览历史失败:', error)
        userHistory.value = []
      }

      try {
        const followingResponse = await usersAPI.getUserFollowing(userId)
        userFollowing.value = followingResponse.data || []
      } catch (error) {
        console.error('加载关注列表失败:', error)
        userFollowing.value = []
      }
    }
  } catch (error) {
    console.error('加载用户数据失败:', error)
    // 使用模拟数据作为后备
    userStats.value = {
      posts: 0,
      followers: 0,
      following: 0
    }
    userPosts.value = []
    userBookmarks.value = []
    userHistory.value = []
    userFollowing.value = []
    currentUser.value = authStore.user
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

const getAvatarUrl = (avatar) => {
  const user = currentUser.value || { id: viewingUserId.value, avatar }
  return getAvatarUrlUtil(user)
}

const handleAvatarError = (event) => {
  const user = currentUser.value || { id: viewingUserId.value }
  handleAvatarErrorUtil(event, user)
}

// 权限检查函数
const canEditPost = (post) => {
  // 必须登录
  if (!authStore.isAuthenticated) {
    return false
  }

  // 管理员可以编辑所有文章
  if (authStore.user?.role === 'admin') {
    return true
  }

  // 只有作者本人可以编辑自己的文章
  return post.authorId === authStore.user?.id
}

const goToUserProfile = (userId) => {
  if (userId === authStore.user?.id) {
    // 如果是自己，跳转到不带参数的个人中心
    router.push('/profile')
  } else {
    // 如果是其他用户，跳转到带用户ID的页面
    router.push(`/user/${userId}`)
  }
}

const toggleFollow = async () => {
  const targetUserId = viewingUserId.value
  try {
    if (isFollowing.value) {
      // 取消关注
      await followsAPI.unfollowUser(targetUserId)
      isFollowing.value = false
      userStats.value.followers = Math.max(0, userStats.value.followers - 1)
      toastStore.success('已取消关注')
    } else {
      // 关注用户
      await followsAPI.followUser(targetUserId)
      isFollowing.value = true
      userStats.value.followers = userStats.value.followers + 1
      toastStore.success('关注成功')
    }
  } catch (error) {
    console.error('关注操作失败:', error)
    if (error.response?.status === 400) {
      const errorMsg = error.response.data?.detail || '操作失败'
      if (errorMsg.includes('已经关注')) {
        toastStore.warning('已经关注过该用户')
        isFollowing.value = true
      } else if (errorMsg.includes('未关注')) {
        toastStore.warning('还未关注该用户')
        isFollowing.value = false
      } else {
        toastStore.error(errorMsg)
      }
    } else {
      toastStore.error('网络错误，请稍后重试')
    }
  }
}

const followUser = async (userId = null) => {
  // 确保userId是数字类型，如果不是则使用viewingUserId
  const targetUserId = (typeof userId === 'number' && userId > 0) ? userId : viewingUserId.value
  try {
    await followsAPI.followUser(targetUserId)
    toastStore.success('关注成功')
    // 重新加载用户数据
    loadUserData()
  } catch (error) {
    console.error('关注失败:', error)
    toastStore.error('关注失败')
  }
}

const toggleFollowUser = async (user) => {
  try {
    if (user.is_following) {
      // 取消关注
      await followsAPI.unfollowUser(user.id)
      user.is_following = false
      user.followers_count = Math.max(0, user.followers_count - 1)
      toastStore.success('已取消关注')
    } else {
      // 关注用户
      await followsAPI.followUser(user.id)
      user.is_following = true
      user.followers_count = user.followers_count + 1
      toastStore.success('关注成功')
    }
  } catch (error) {
    console.error('关注操作失败:', error)
    if (error.response?.status === 400) {
      const errorMsg = error.response.data?.detail || '操作失败'
      if (errorMsg.includes('已经关注')) {
        toastStore.warning('已经关注过该用户')
        user.is_following = true
      } else if (errorMsg.includes('未关注')) {
        toastStore.warning('还未关注该用户')
        user.is_following = false
      } else {
        toastStore.error(errorMsg)
      }
    } else {
      toastStore.error('网络错误，请稍后重试')
    }
  }
}

const unfollowUser = async (user) => {
  try {
    await followsAPI.unfollowUser(user.id)
    // 从关注列表中移除该用户
    const index = userFollowing.value.findIndex(u => u.id === user.id)
    if (index > -1) {
      userFollowing.value.splice(index, 1)
    }
    // 更新统计数据
    userStats.value.following = Math.max(0, userStats.value.following - 1)
    toastStore.success('已取消关注')
  } catch (error) {
    console.error('取消关注失败:', error)
    if (error.response?.status === 400) {
      const errorMsg = error.response.data?.detail || '操作失败'
      toastStore.error(errorMsg)
    } else {
      toastStore.error('网络错误，请稍后重试')
    }
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

// 监听路由变化
watch(() => route.params.id, () => {
  // 重置到文章标签页
  activeTab.value = 'posts'
  // 重置关注状态
  isFollowing.value = false
  loadUserData()
})

// 监听是否是自己的资料页面变化
watch(isOwnProfile, (newValue) => {
  // 如果切换到其他用户的资料页面，重置到文章标签页
  if (!newValue) {
    activeTab.value = 'posts'
  }
})

onMounted(() => {
  loadUserData()

  // 初始化编辑表单
  profileForm.username = authStore.user?.username || ''
  profileForm.bio = authStore.user?.bio || ''
})
</script>
