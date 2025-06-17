<template>
  <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-sm">B</span>
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
          <!-- 匿名频道 -->
          <router-link 
            v-if="authStore.isAuthenticated"
            to="/anonymous" 
            class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
          >
            匿名频道
          </router-link>
          
          <!-- 发布文章 -->
          <router-link 
            v-if="authStore.isAuthenticated"
            to="/create-post" 
            class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
          >
            发布文章
          </router-link>
          
          <!-- 通知 -->
          <button 
            v-if="authStore.isAuthenticated"
            @click="toggleNotifications"
            class="relative p-2 text-gray-600 hover:text-gray-900"
          >
            <Bell class="w-5 h-5" />
            <span 
              v-if="unreadCount > 0"
              class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
            >
              {{ unreadCount > 99 ? '99+' : unreadCount }}
            </span>
          </button>
          
          <!-- 用户菜单 -->
          <div v-if="authStore.isAuthenticated" class="relative">
            <button 
              @click="toggleUserMenu"
              class="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-100"
            >
              <img 
                :src="authStore.user?.avatar || '/placeholder.svg?height=32&width=32'" 
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
                v-if="authStore.isAdmin"
                to="/admin"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                @click="showUserMenu = false"
              >
                管理后台
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
import { Bell, ChevronDown } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import SearchBar from '../common/SearchBar.vue'

const router = useRouter()
const authStore = useAuthStore()

const showUserMenu = ref(false)
const showNotifications = ref(false)
const unreadCount = ref(0)

// 点击外部关闭菜单
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showUserMenu.value = false
    showNotifications.value = false
  }
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
  showNotifications.value = false
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  showUserMenu.value = false
}

const handleLogout = () => {
  authStore.logout()
  showUserMenu.value = false
  router.push('/')
}


onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
