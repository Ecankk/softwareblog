<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- 页面头部 -->
      <div class="text-center mb-16">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">产品路线图</h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          探索我们的产品发展规划，了解即将推出的激动人心的新功能
        </p>
      </div>

      <!-- 当前版本 -->
      <div class="mb-16">
        <div class="flex items-center mb-8">
          <div class="w-4 h-4 bg-green-500 rounded-full mr-4"></div>
          <h2 class="text-2xl font-bold text-gray-900">当前版本 v1.0</h2>
          <span class="ml-4 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">已发布</span>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="feature in currentFeatures" :key="feature.name" class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center mb-4">
              <component :is="feature.icon" class="w-8 h-8 text-green-600 mr-3" />
              <h3 class="text-lg font-semibold text-gray-900">{{ feature.name }}</h3>
            </div>
            <p class="text-gray-600">{{ feature.description }}</p>
          </div>
        </div>
      </div>

      <!-- 即将推出 -->
      <div class="mb-16">
        <div class="flex items-center mb-8">
          <div class="w-4 h-4 bg-blue-500 rounded-full mr-4"></div>
          <h2 class="text-2xl font-bold text-gray-900">即将推出 v1.1</h2>
          <span class="ml-4 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">开发中</span>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="feature in upcomingFeatures" :key="feature.name" class="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <component :is="feature.icon" class="w-8 h-8 text-blue-600 mr-3" />
                <h3 class="text-lg font-semibold text-gray-900">{{ feature.name }}</h3>
              </div>
              <span class="text-sm text-blue-600 font-medium">{{ feature.progress }}%</span>
            </div>
            <p class="text-gray-600 mb-4">{{ feature.description }}</p>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div 
                class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                :style="{ width: feature.progress + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 规划中 -->
      <div class="mb-16">
        <div class="flex items-center mb-8">
          <div class="w-4 h-4 bg-purple-500 rounded-full mr-4"></div>
          <h2 class="text-2xl font-bold text-gray-900">规划中 v2.0</h2>
          <span class="ml-4 px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">设计阶段</span>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="feature in plannedFeatures" :key="feature.name" class="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
            <div class="flex items-center mb-4">
              <component :is="feature.icon" class="w-8 h-8 text-purple-600 mr-3" />
              <h3 class="text-lg font-semibold text-gray-900">{{ feature.name }}</h3>
            </div>
            <p class="text-gray-600 mb-4">{{ feature.description }}</p>
            <div class="flex items-center text-sm text-purple-600">
              <Clock class="w-4 h-4 mr-1" />
              <span>预计 {{ feature.eta }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 社区反馈 -->
      <div class="bg-white rounded-lg shadow p-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">社区反馈</h2>
        <p class="text-gray-600 mb-6">
          我们重视每一位用户的意见和建议。如果你有任何功能需求或改进建议，请告诉我们！
        </p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center p-6 bg-gray-50 rounded-lg">
            <MessageSquare class="w-12 h-12 text-blue-600 mx-auto mb-4" />
            <h3 class="text-lg font-semibold text-gray-900 mb-2">功能建议</h3>
            <p class="text-gray-600 mb-4">提出你希望看到的新功能</p>
            <button class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
              提交建议
            </button>
          </div>
          
          <div class="text-center p-6 bg-gray-50 rounded-lg">
            <Bug class="w-12 h-12 text-red-600 mx-auto mb-4" />
            <h3 class="text-lg font-semibold text-gray-900 mb-2">问题反馈</h3>
            <p class="text-gray-600 mb-4">报告你遇到的问题或错误</p>
            <button class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700">
              报告问题
            </button>
          </div>
          
          <div class="text-center p-6 bg-gray-50 rounded-lg">
            <Star class="w-12 h-12 text-yellow-600 mx-auto mb-4" />
            <h3 class="text-lg font-semibold text-gray-900 mb-2">功能投票</h3>
            <p class="text-gray-600 mb-4">为你最期待的功能投票</p>
            <button class="bg-yellow-600 text-white px-4 py-2 rounded-md hover:bg-yellow-700">
              参与投票
            </button>
          </div>
        </div>
      </div>

      <!-- 版本历史 -->
      <div class="mt-16">
        <h2 class="text-2xl font-bold text-gray-900 mb-8">版本历史</h2>
        <div class="space-y-6">
          <div v-for="version in versionHistory" :key="version.version" class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center">
                <h3 class="text-lg font-semibold text-gray-900">{{ version.version }}</h3>
                <span class="ml-3 px-2 py-1 bg-gray-100 text-gray-800 rounded text-sm">{{ version.date }}</span>
              </div>
              <span :class="[
                'px-3 py-1 rounded-full text-sm font-medium',
                version.type === 'major' ? 'bg-red-100 text-red-800' :
                version.type === 'minor' ? 'bg-blue-100 text-blue-800' :
                'bg-green-100 text-green-800'
              ]">
                {{ version.type === 'major' ? '重大更新' : version.type === 'minor' ? '功能更新' : '修复更新' }}
              </span>
            </div>
            <ul class="space-y-2">
              <li v-for="change in version.changes" :key="change" class="flex items-start">
                <div class="w-2 h-2 bg-gray-400 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <span class="text-gray-600">{{ change }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  FileText, 
  Users, 
  MessageCircle, 
  Heart, 
  Search,
  Bell,
  BarChart3,
  Smartphone,
  Globe,
  Zap,
  Brain,
  Shield,
  Clock,
  MessageSquare,
  Bug,
  Star
} from 'lucide-vue-next'

const currentFeatures = [
  {
    name: '文章管理',
    description: '创建、编辑、发布和管理文章，支持 Markdown 格式',
    icon: FileText
  },
  {
    name: '用户系统',
    description: '用户注册、登录、个人资料管理和关注系统',
    icon: Users
  },
  {
    name: '评论互动',
    description: '文章评论、点赞和收藏功能',
    icon: MessageCircle
  },
  {
    name: '搜索功能',
    description: '全文搜索文章、用户和标签',
    icon: Search
  },
  {
    name: '管理后台',
    description: '管理员后台，管理用户、文章和系统设置',
    icon: Shield
  },
  {
    name: '匿名频道',
    description: '匿名消息发布和浏览功能',
    icon: MessageSquare
  }
]

const upcomingFeatures = [
  {
    name: '实时消息',
    description: 'WebSocket 实时聊天和通知推送',
    icon: Bell,
    progress: 75
  },
  {
    name: '数据分析',
    description: '用户行为分析和内容统计图表',
    icon: BarChart3,
    progress: 60
  },
  {
    name: '移动端优化',
    description: 'PWA 支持和移动端体验优化',
    icon: Smartphone,
    progress: 40
  },
  {
    name: '多语言支持',
    description: '国际化支持，多语言界面',
    icon: Globe,
    progress: 20
  }
]

const plannedFeatures = [
  {
    name: 'AI 内容助手',
    description: 'AI 驱动的内容推荐和写作辅助',
    icon: Brain,
    eta: '2024 Q4'
  },
  {
    name: '高级编辑器',
    description: '富文本编辑器和协作编辑功能',
    icon: FileText,
    eta: '2025 Q1'
  },
  {
    name: '社区活动',
    description: '在线活动组织和参与系统',
    icon: Users,
    eta: '2025 Q1'
  },
  {
    name: '插件系统',
    description: '第三方插件支持和扩展市场',
    icon: Zap,
    eta: '2025 Q2'
  },
  {
    name: '高级安全',
    description: '两步验证和高级安全功能',
    icon: Shield,
    eta: '2025 Q2'
  },
  {
    name: 'API 生态',
    description: '完整的 REST API 和 GraphQL 支持',
    icon: Globe,
    eta: '2025 Q3'
  }
]

const versionHistory = [
  {
    version: 'v1.0.0',
    date: '2024-06-18',
    type: 'major',
    changes: [
      '首次正式发布',
      '完整的文章管理系统',
      '用户注册和认证',
      '评论和互动功能',
      '管理员后台',
      '搜索功能'
    ]
  },
  {
    version: 'v0.9.0',
    date: '2024-06-10',
    type: 'minor',
    changes: [
      '添加匿名频道功能',
      '优化用户界面',
      '修复若干已知问题',
      '性能优化'
    ]
  },
  {
    version: 'v0.8.0',
    date: '2024-06-01',
    type: 'minor',
    changes: [
      '实现关注系统',
      '添加通知功能',
      '优化移动端体验',
      '增加头像系统'
    ]
  }
]
</script>
