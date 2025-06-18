<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 管理员导航 -->
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <h1 class="text-xl font-bold text-gray-900">管理后台</h1>
            <div class="flex space-x-4">
              <button
                @click="activeTab = 'dashboard'"
                :class="[
                  'px-3 py-2 rounded-md text-sm font-medium',
                  activeTab === 'dashboard' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-600 hover:text-gray-900'
                ]"
              >
                仪表板
              </button>
              <button
                @click="activeTab = 'posts'"
                :class="[
                  'px-3 py-2 rounded-md text-sm font-medium',
                  activeTab === 'posts' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-600 hover:text-gray-900'
                ]"
              >
                文章管理
              </button>
              <button
                @click="activeTab = 'users'"
                :class="[
                  'px-3 py-2 rounded-md text-sm font-medium',
                  activeTab === 'users' 
                    ? 'bg-blue-100 text-blue-700' 
                    : 'text-gray-600 hover:text-gray-900'
                ]"
              >
                用户管理
              </button>
            </div>
          </div>
          <router-link 
            to="/" 
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
          >
            返回首页
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <!-- 仪表板 -->
      <div v-if="activeTab === 'dashboard'" class="space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Users class="h-8 w-8 text-blue-600" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">总用户数</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.users_count || 0 }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <FileText class="h-8 w-8 text-green-600" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">总文章数</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.posts_count || 0 }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <MessageCircle class="h-8 w-8 text-yellow-600" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">总评论数</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.comments_count || 0 }}</p>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Heart class="h-8 w-8 text-red-600" />
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-500">关注关系</p>
                <p class="text-2xl font-semibold text-gray-900">{{ stats.follows_count || 0 }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 文章管理 -->
      <AdminPosts v-if="activeTab === 'posts'" />

      <!-- 用户管理 -->
      <AdminUsers v-if="activeTab === 'users'" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Users, FileText, MessageCircle, Heart } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useToastStore } from '../stores/toast'
import { adminAPI } from '../api/admin'
import AdminPosts from '../components/admin/AdminPosts.vue'
import AdminUsers from '../components/admin/AdminUsers.vue'

const router = useRouter()
const authStore = useAuthStore()
const toastStore = useToastStore()

const activeTab = ref('dashboard')
const stats = ref({})
const loading = ref(false)

// 检查管理员权限
const checkAdminPermission = () => {
  if (!authStore.isAuthenticated || !authStore.isAdmin) {
    toastStore.showToast('无权限访问管理后台', 'error')
    router.push('/')
    return false
  }
  return true
}

// 获取统计信息
const loadStats = async () => {
  if (!checkAdminPermission()) return

  loading.value = true
  try {
    const response = await adminAPI.getStats()
    stats.value = response.data || response
  } catch (error) {
    console.error('获取统计信息失败:', error)
    toastStore.showToast('获取统计信息失败', 'error')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (checkAdminPermission()) {
    loadStats()
  }
})
</script>
