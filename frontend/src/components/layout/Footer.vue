<template>
  <footer class="bg-gray-900 text-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- 网站信息 -->
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center shadow-md">
              <BookOpen class="w-5 h-5 text-white" />
            </div>
            <span class="text-xl font-bold">博客论坛</span>
          </div>
          <p class="text-gray-400 mb-4 max-w-md">
            一个专业的技术博客和讨论社区，汇聚优质内容和活跃用户，共同构建知识分享平台。
          </p>
          <div class="flex space-x-4">
            <a href="https://github.com/Ecankk/softwareblog" target="_blank" rel="noopener noreferrer" class="text-gray-400 hover:text-white transition-colors">
              <span class="sr-only">GitHub</span>
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <span class="sr-only">Twitter</span>
              <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84"/>
              </svg>
            </a>
          </div>
        </div>
        
        <!-- 快速链接 -->
        <div>
          <h3 class="text-sm font-semibold text-gray-400 tracking-wider uppercase mb-4">
            快速链接
          </h3>
          <ul class="space-y-2">
            <li>
              <router-link to="/" class="text-gray-300 hover:text-white transition-colors">
                首页
              </router-link>
            </li>
            <li>
              <router-link to="/search" class="text-gray-300 hover:text-white transition-colors">
                搜索
              </router-link>
            </li>
            <li>
              <router-link to="/activities" class="text-gray-300 hover:text-white transition-colors">
                社区活动
              </router-link>
            </li>
            <li>
              <router-link to="/anonymous" class="text-gray-300 hover:text-white transition-colors">
                匿名频道
              </router-link>
            </li>
            <li>
              <router-link to="/api-docs" class="text-gray-300 hover:text-white transition-colors">
                API 文档
              </router-link>
            </li>
            <li>
              <router-link to="/roadmap" class="text-gray-300 hover:text-white transition-colors">
                产品路线图
              </router-link>
            </li>
          </ul>
        </div>
        
        <!-- 帮助支持 -->
        <div>
          <h3 class="text-sm font-semibold text-gray-400 tracking-wider uppercase mb-4">
            帮助支持
          </h3>
          <ul class="space-y-2">
            <li>
              <router-link to="/guide" class="text-gray-300 hover:text-white transition-colors">
                使用指南
              </router-link>
            </li>
            <li>
              <router-link to="/rules" class="text-gray-300 hover:text-white transition-colors">
                社区规则
              </router-link>
            </li>
            <li>
              <router-link to="/contact" class="text-gray-300 hover:text-white transition-colors">
                联系我们
              </router-link>
            </li>
            <li>
              <router-link to="/feedback" class="text-gray-300 hover:text-white transition-colors">
                意见反馈
              </router-link>
            </li>
          </ul>
        </div>
      </div>
      
      <div class="mt-8 pt-8 border-t border-gray-800 flex flex-col sm:flex-row justify-between items-center">
        <p class="text-gray-400 text-sm">
          © 2025 博客论坛. 保留所有权利.
        </p>
        <div class="mt-4 sm:mt-0 flex space-x-6">
          <a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">
            隐私政策
          </a>
          <a href="#" class="text-gray-400 hover:text-white text-sm transition-colors">
            服务条款
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { BookOpen } from 'lucide-vue-next'
</script>
