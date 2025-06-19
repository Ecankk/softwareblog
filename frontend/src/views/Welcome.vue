<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">

    <!-- 主要内容 -->
    <main>
      <!-- 英雄区域 -->
      <section class="relative py-20 lg:py-32">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center">
            <h1 class="text-4xl lg:text-6xl font-bold text-gray-900 mb-6">
              欢迎来到
              <span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                博客论坛
              </span>
            </h1>
            <p class="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              一个专为开发者和技术爱好者打造的知识分享平台。在这里，你可以分享经验、学习新技术、与同行交流，共同成长。
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <router-link to="/posts"
                class="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl transform hover:-translate-y-1">
                开始探索
              </router-link>
              <router-link to="/register"
                class="border border-blue-600 text-blue-600 px-8 py-3 rounded-lg text-lg font-medium hover:bg-blue-50 transition-colors">
                立即加入
              </router-link>
            </div>
          </div>
        </div>

        <!-- 装饰性元素 -->
        <div class="absolute top-20 left-10 w-20 h-20 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
        <div
          class="absolute bottom-20 right-10 w-32 h-32 bg-purple-200 rounded-full opacity-20 animate-pulse delay-1000">
        </div>
      </section>

      <!-- 特色功能 -->
      <section class="py-20 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">平台特色</h2>
            <p class="text-lg text-gray-600">为技术人员量身定制的功能体验</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- 功能卡片 -->
            <div class="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mb-4">
                <Edit class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">Markdown编辑</h3>
              <p class="text-gray-600">支持完整的Markdown语法，代码高亮，让你的技术文章更加专业。</p>
            </div>

            <div class="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div class="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mb-4">
                <Users class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">社区互动</h3>
              <p class="text-gray-600">关注感兴趣的作者，参与讨论，建立你的技术人脉圈。</p>
            </div>

            <div
              class="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div class="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center mb-4">
                <Heart class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">打赏支持</h3>
              <p class="text-gray-600">为优质内容打赏，支持作者创作，营造良好的知识分享氛围。</p>
            </div>

            <div
              class="bg-gradient-to-br from-yellow-50 to-yellow-100 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div class="w-12 h-12 bg-yellow-600 rounded-lg flex items-center justify-center mb-4">
                <Search class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">智能搜索</h3>
              <p class="text-gray-600">快速找到你需要的技术文章和解决方案。</p>
            </div>

            <div class="bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div class="w-12 h-12 bg-red-600 rounded-lg flex items-center justify-center mb-4">
                <Tag class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">标签分类</h3>
              <p class="text-gray-600">通过标签快速分类和查找相关技术内容。</p>
            </div>

            <div
              class="bg-gradient-to-br from-indigo-50 to-indigo-100 p-6 rounded-xl hover:shadow-lg transition-shadow">
              <div class="w-12 h-12 bg-indigo-600 rounded-lg flex items-center justify-center mb-4">
                <MessageCircle class="w-6 h-6 text-white" />
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">评论交流</h3>
              <p class="text-gray-600">在文章下方进行深入讨论，分享见解和经验。</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 统计数据 -->
      <section class="py-20 bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="text-center mb-16">
            <h2 class="text-3xl font-bold text-gray-900 mb-4">平台数据</h2>
            <p class="text-lg text-gray-600">不断成长的技术社区</p>
          </div>

          <div class="grid grid-cols-2 lg:grid-cols-4 gap-8">
            <div class="text-center">
              <div class="text-4xl font-bold text-blue-600 mb-2">{{ stats.users }}+</div>
              <div class="text-gray-600">注册用户</div>
            </div>
            <div class="text-center">
              <div class="text-4xl font-bold text-green-600 mb-2">{{ stats.posts }}+</div>
              <div class="text-gray-600">技术文章</div>
            </div>
            <div class="text-center">
              <div class="text-4xl font-bold text-purple-600 mb-2">{{ stats.comments }}+</div>
              <div class="text-gray-600">互动评论</div>
            </div>
            <div class="text-center">
              <div class="text-4xl font-bold text-red-600 mb-2">{{ stats.views }}+</div>
              <div class="text-gray-600">文章阅读</div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA区域 -->
      <section class="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 class="text-3xl font-bold text-white mb-4">准备好开始你的技术分享之旅了吗？</h2>
          <p class="text-xl text-blue-100 mb-8">加入我们，与千万技术人员一起成长</p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link to="/register"
              class="bg-white text-blue-600 px-8 py-3 rounded-lg text-lg font-medium hover:bg-gray-100 transition-colors shadow-lg">
              立即注册
            </router-link>
            <router-link to="/posts"
              class="border border-white text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-white/10 transition-colors">
              浏览文章
            </router-link>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Edit, Users, Heart, Search, Tag, MessageCircle } from 'lucide-vue-next'

// 统计数据
const stats = ref({
  users: 0,
  posts: 0,
  comments: 0,
  views: 0
})

// 动画计数效果
const animateNumber = (target, key, duration = 2000) => {
  const start = 0
  const increment = target / (duration / 16)
  let current = start

  const timer = setInterval(() => {
    current += increment
    if (current >= target) {
      current = target
      clearInterval(timer)
    }
    stats.value[key] = Math.floor(current)
  }, 16)
}

onMounted(() => {
  // 启动数字动画
  setTimeout(() => {
    animateNumber(1200, 'users')
    animateNumber(850, 'posts')
    animateNumber(3200, 'comments')
    animateNumber(15000, 'views')
  }, 500)
})
</script>

<style scoped>
/* 自定义动画 */
@keyframes float {

  0%,
  100% {
    transform: translateY(0px);
  }

  50% {
    transform: translateY(-20px);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}
</style>
