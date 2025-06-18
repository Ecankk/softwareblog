<template>
  <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center shadow-md">
              <BookOpen class="w-5 h-5 text-white" />
            </div>
            <span class="text-xl font-bold text-gray-900">博客论坛</span>
          </router-link>
        </div>
        
        <!-- 搜索框 -->
        <div class="flex-1 max-w-lg mx-8">
          <SearchBar />
        </div>
        
        <!-- 导航菜单 -->
        <nav class="flex items-center space-x-4">
          <!-- 导航链接 -->
          <router-link
            to="/activities"
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
          >
            活动
          </router-link>

          <router-link
            v-if="authStore.isAuthenticated"
            to="/anonymous"
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
          >
            匿名频道
          </router-link>

          <router-link
            v-if="authStore.isAuthenticated"
            to="/messages"
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
          >
            消息
          </router-link>
          
          <!-- 发布文章 -->
          <router-link 
            v-if="authStore.isAuthenticated"
            to="/create-post" 
            class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
          >
            发布文章
          </router-link>
          
          <!-- 通知中心 -->
          <NotificationCenter v-if="authStore.isAuthenticated" />
          
          <!-- 用户菜单 -->
          <div v-if="authStore.isAuthenticated" class="relative">
            <button 
              @click="toggleUserMenu"
              class="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-100"
            >
              <img
                :src="getAvatarUrl(authStore.user)"
                :alt="authStore.user?.username"
                class="w-8 h-8 rounded-full"
              />
              <ChevronDown class="w-4 h-4 text-gray-500" />
            </button>
            
            <!-- 下拉菜单 -->
            <div 
              v-if="showUserMenu"
              class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50"
            >
              <router-link
                :to="`/user/${authStore.user?.id}`"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                @click="showUserMenu = false"
              >
                个人中心
              </router-link>
              <router-link
                to="/settings"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                @click="showUserMenu = false"
              >
                设置
              </router-link>
              <router-link
                v-if="authStore.isAdmin"
                to="/admin"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                @click="showUserMenu = false"
              >
                管理后台
              </router-link>
              <router-link
                v-if="authStore.isAdmin"
                to="/analytics"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                @click="showUserMenu = false"
              >
                数据分析
              </router-link>
              <hr class="my-1">
              <button 
                @click="handleLogout"
                class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                退出登录
              </button>
            </div>
          </div>
          
          <!-- 登录/注册 -->
          <div v-else class="flex items-center space-x-2">
            <router-link 
              to="/login"
              class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              登录
            </router-link>
            <router-link 
              to="/register"
              class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
            >
              注册
            </router-link>
          </div>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronDown, BookOpen } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import SearchBar from '../common/SearchBar.vue'
import NotificationCenter from '../notification/NotificationCenter.vue'

const router = useRouter()
const authStore = useAuthStore()

const showUserMenu = ref(false)

// 点击外部关闭菜单
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showUserMenu.value = false
  }
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const handleLogout = () => {
  authStore.logout()
  showUserMenu.value = false
  router.push('/')
}

// 导入头像工具函数
import { getAvatarUrl } from '../../utils/avatar'


onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
