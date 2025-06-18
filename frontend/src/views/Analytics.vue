<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 页面头部 -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">数据分析</h1>
            <p class="mt-2 text-gray-600">深入了解平台数据趋势和用户行为</p>
          </div>
          <div class="flex items-center space-x-3">
            <select class="border border-gray-300 rounded-md px-3 py-2 text-sm">
              <option>最近7天</option>
              <option>最近30天</option>
              <option>最近90天</option>
              <option>自定义时间</option>
            </select>
            <button class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700">
              导出报告
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 核心指标卡片 -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <TrendingUp class="h-8 w-8 text-green-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">日活跃用户</p>
              <p class="text-2xl font-semibold text-gray-900">1,234</p>
              <p class="text-sm text-green-600">+12.5% 较昨日</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <Eye class="h-8 w-8 text-blue-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">页面浏览量</p>
              <p class="text-2xl font-semibold text-gray-900">45,678</p>
              <p class="text-sm text-blue-600">+8.3% 较昨日</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <FileText class="h-8 w-8 text-purple-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">新增文章</p>
              <p class="text-2xl font-semibold text-gray-900">89</p>
              <p class="text-sm text-purple-600">+15.2% 较昨日</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <MessageCircle class="h-8 w-8 text-orange-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">用户互动</p>
              <p class="text-2xl font-semibold text-gray-900">2,567</p>
              <p class="text-sm text-orange-600">+22.1% 较昨日</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 图表区域 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- 用户增长趋势 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">用户增长趋势</h3>
          <div class="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
            <div class="text-center text-gray-500">
              <BarChart3 class="h-12 w-12 mx-auto mb-2" />
              <p>图表组件开发中...</p>
              <p class="text-sm">将集成 Chart.js 或 ECharts</p>
            </div>
          </div>
        </div>

        <!-- 内容热度分析 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">内容热度分析</h3>
          <div class="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
            <div class="text-center text-gray-500">
              <PieChart class="h-12 w-12 mx-auto mb-2" />
              <p>饼图组件开发中...</p>
              <p class="text-sm">分析文章分类热度</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 详细数据表格 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- 热门文章排行 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">热门文章排行</h3>
          <div class="space-y-4">
            <div v-for="i in 5" :key="i" class="flex items-center space-x-3">
              <div class="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-sm font-medium text-blue-600">
                {{ i }}
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 truncate">
                  示例文章标题 {{ i }}
                </p>
                <p class="text-sm text-gray-500">{{ 1000 - i * 100 }} 次浏览</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 活跃用户排行 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">活跃用户排行</h3>
          <div class="space-y-4">
            <div v-for="i in 5" :key="i" class="flex items-center space-x-3">
              <img 
                :src="`https://api.dicebear.com/7.x/avataaars/svg?seed=user${i}`"
                :alt="`用户${i}`"
                class="w-8 h-8 rounded-full"
              />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900">用户{{ i }}</p>
                <p class="text-sm text-gray-500">{{ 50 - i * 5 }} 篇文章</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 标签云 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">热门标签</h3>
          <div class="flex flex-wrap gap-2">
            <span v-for="tag in popularTags" :key="tag.name" 
                  :class="[
                    'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium',
                    tag.level === 'high' ? 'bg-red-100 text-red-800' :
                    tag.level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  ]">
              {{ tag.name }}
            </span>
          </div>
        </div>
      </div>

      <!-- 功能预告 -->
      <div class="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
        <div class="flex items-center space-x-3 mb-4">
          <Zap class="h-6 w-6 text-blue-600" />
          <h3 class="text-lg font-semibold text-gray-900">即将推出的功能</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">实时数据流</h4>
            <p class="text-sm text-gray-600 mt-1">WebSocket 实时数据更新</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">AI 内容分析</h4>
            <p class="text-sm text-gray-600 mt-1">智能内容质量评估</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">用户画像</h4>
            <p class="text-sm text-gray-600 mt-1">深度用户行为分析</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  TrendingUp, 
  Eye, 
  FileText, 
  MessageCircle, 
  BarChart3, 
  PieChart,
  Zap
} from 'lucide-vue-next'

// 模拟数据
const popularTags = ref([
  { name: 'JavaScript', level: 'high' },
  { name: 'Vue.js', level: 'high' },
  { name: 'Python', level: 'medium' },
  { name: 'React', level: 'medium' },
  { name: 'Node.js', level: 'medium' },
  { name: 'TypeScript', level: 'low' },
  { name: 'CSS', level: 'low' },
  { name: 'HTML', level: 'low' }
])
</script>
