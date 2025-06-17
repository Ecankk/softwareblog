<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- 全局Loading -->
    <LoadingSpinner v-if="globalStore.isLoading" />
    
    <!-- Toast通知 -->
    <Toast />
    
    <!-- 主要内容 -->
    <div class="flex flex-col min-h-screen">
      <!-- 顶部导航 -->
      <Header />
      
      <!-- 主内容区域 -->
      <main class="flex-1">
        <router-view />
      </main>
      
      <!-- 底部信息 -->
      <Footer />
    </div>
    
    <!-- 通知中心 -->
    <NotificationCenter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useGlobalStore } from './stores/global'
import { useAuthStore } from './stores/auth'
import Header from './components/layout/Header.vue'
import Footer from './components/layout/Footer.vue'
import LoadingSpinner from './components/common/LoadingSpinner.vue'
import Toast from './components/common/Toast.vue'
import NotificationCenter from './components/common/NotificationCenter.vue'

const globalStore = useGlobalStore()
const authStore = useAuthStore()

onMounted(() => {
  // 初始化应用
  authStore.initAuth()
})
</script>

<style>
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

/* 自定义样式 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Markdown编辑器样式 */
.toastui-editor-defaultUI {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
}

.toastui-editor-defaultUI-toolbar {
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
}
</style>
