<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 页面头部 -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">社区活动</h1>
          <p class="mt-2 text-gray-600">参与精彩活动，与社区成员互动交流</p>
        </div>
        <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2">
          <Plus class="w-4 h-4" />
          <span>创建活动</span>
        </button>
      </div>

      <!-- 活动筛选 -->
      <div class="bg-white rounded-lg shadow p-6 mb-8">
        <div class="flex flex-wrap items-center gap-4">
          <div class="flex items-center space-x-2">
            <Filter class="w-5 h-5 text-gray-400" />
            <span class="text-sm font-medium text-gray-700">筛选：</span>
          </div>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="filter in activityFilters"
              :key="filter.key"
              :class="[
                'px-3 py-1 rounded-full text-sm font-medium transition-colors',
                activeFilter === filter.key
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
              @click="activeFilter = filter.key"
            >
              {{ filter.label }}
            </button>
          </div>
        </div>
      </div>

      <!-- 热门活动轮播 -->
      <div class="bg-white rounded-lg shadow mb-8 overflow-hidden">
        <div class="p-6 border-b">
          <h2 class="text-xl font-semibold text-gray-900">热门活动</h2>
        </div>
        <div class="relative h-64 bg-gradient-to-r from-blue-500 to-purple-600">
          <div class="absolute inset-0 bg-black bg-opacity-30"></div>
          <div class="relative h-full flex items-center justify-center text-white text-center">
            <div>
              <h3 class="text-2xl font-bold mb-2">2024 年度技术分享大会</h3>
              <p class="text-lg mb-4">汇聚行业专家，分享前沿技术</p>
              <div class="flex items-center justify-center space-x-4 text-sm">
                <div class="flex items-center space-x-1">
                  <Calendar class="w-4 h-4" />
                  <span>2024年12月15日</span>
                </div>
                <div class="flex items-center space-x-1">
                  <MapPin class="w-4 h-4" />
                  <span>线上直播</span>
                </div>
                <div class="flex items-center space-x-1">
                  <Users class="w-4 h-4" />
                  <span>1,234 人参与</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 活动列表 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- 活动卡片 -->
        <div class="lg:col-span-2 space-y-6">
          <div v-for="activity in activities" :key="activity.id" class="bg-white rounded-lg shadow overflow-hidden">
            <div class="relative h-48">
              <img :src="activity.image" :alt="activity.title" class="w-full h-full object-cover" />
              <div class="absolute top-4 left-4">
                <span :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  activity.status === 'upcoming' ? 'bg-blue-100 text-blue-800' :
                  activity.status === 'ongoing' ? 'bg-green-100 text-green-800' :
                  'bg-gray-100 text-gray-800'
                ]">
                  {{ getStatusText(activity.status) }}
                </span>
              </div>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ activity.title }}</h3>
              <p class="text-gray-600 mb-4">{{ activity.description }}</p>
              
              <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
                <div class="flex items-center space-x-4">
                  <div class="flex items-center space-x-1">
                    <Calendar class="w-4 h-4" />
                    <span>{{ activity.date }}</span>
                  </div>
                  <div class="flex items-center space-x-1">
                    <MapPin class="w-4 h-4" />
                    <span>{{ activity.location }}</span>
                  </div>
                </div>
                <div class="flex items-center space-x-1">
                  <Users class="w-4 h-4" />
                  <span>{{ activity.participants }} 人参与</span>
                </div>
              </div>

              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <img :src="activity.organizer.avatar" :alt="activity.organizer.name" class="w-8 h-8 rounded-full" />
                  <span class="text-sm text-gray-600">{{ activity.organizer.name }}</span>
                </div>
                <div class="flex space-x-2">
                  <button class="px-4 py-2 border border-gray-300 rounded-md text-sm hover:bg-gray-50">
                    了解详情
                  </button>
                  <button :class="[
                    'px-4 py-2 rounded-md text-sm',
                    activity.joined 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  ]">
                    {{ activity.joined ? '已参与' : '立即参与' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 侧边栏 -->
        <div class="space-y-6">
          <!-- 活动日历 -->
          <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">活动日历</h3>
            <div class="bg-gray-100 rounded-lg h-64 flex items-center justify-center">
              <div class="text-center text-gray-500">
                <Calendar class="w-12 h-12 mx-auto mb-2" />
                <p>日历组件开发中...</p>
                <p class="text-sm">将集成日历视图</p>
              </div>
            </div>
          </div>

          <!-- 我的活动 -->
          <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">我的活动</h3>
            <div class="space-y-3">
              <div v-for="myActivity in myActivities" :key="myActivity.id" class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div :class="[
                  'w-3 h-3 rounded-full',
                  myActivity.status === 'upcoming' ? 'bg-blue-500' :
                  myActivity.status === 'ongoing' ? 'bg-green-500' :
                  'bg-gray-500'
                ]"></div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ myActivity.title }}</p>
                  <p class="text-xs text-gray-500">{{ myActivity.date }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 活动统计 -->
          <div class="bg-white rounded-lg shadow p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">活动统计</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">参与活动</span>
                <span class="text-sm font-medium text-gray-900">12 个</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">创建活动</span>
                <span class="text-sm font-medium text-gray-900">3 个</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600">获得徽章</span>
                <span class="text-sm font-medium text-gray-900">5 个</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能预告 -->
      <div class="mt-8 bg-gradient-to-r from-orange-50 to-red-50 rounded-lg p-6">
        <div class="flex items-center space-x-3 mb-4">
          <Zap class="h-6 w-6 text-orange-600" />
          <h3 class="text-lg font-semibold text-gray-900">即将推出的活动功能</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">在线直播</h4>
            <p class="text-sm text-gray-600 mt-1">实时视频直播活动</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">活动签到</h4>
            <p class="text-sm text-gray-600 mt-1">二维码签到系统</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">成就徽章</h4>
            <p class="text-sm text-gray-600 mt-1">参与活动获得徽章</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">活动回放</h4>
            <p class="text-sm text-gray-600 mt-1">错过的活动可回看</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  Plus, 
  Filter, 
  Calendar, 
  MapPin, 
  Users,
  Zap
} from 'lucide-vue-next'

const activeFilter = ref('all')

const activityFilters = [
  { key: 'all', label: '全部' },
  { key: 'upcoming', label: '即将开始' },
  { key: 'ongoing', label: '进行中' },
  { key: 'finished', label: '已结束' },
  { key: 'online', label: '线上活动' },
  { key: 'offline', label: '线下活动' }
]

const activities = ref([
  {
    id: 1,
    title: 'Vue.js 3.0 实战分享',
    description: '深入了解 Vue.js 3.0 的新特性和最佳实践，包括 Composition API、性能优化等内容。',
    image: 'https://images.unsplash.com/photo-1517180102446-f3ece451e9d8?w=400&h=200&fit=crop',
    date: '2024年6月20日 19:00',
    location: '线上直播',
    participants: 156,
    status: 'upcoming',
    joined: false,
    organizer: {
      name: '技术团队',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=tech'
    }
  },
  {
    id: 2,
    title: '开源项目贡献指南',
    description: '学习如何为开源项目做贡献，从提交 PR 到代码审查的完整流程。',
    image: 'https://images.unsplash.com/photo-1556075798-4825dfaaf498?w=400&h=200&fit=crop',
    date: '2024年6月25日 14:00',
    location: '北京·中关村',
    participants: 89,
    status: 'upcoming',
    joined: true,
    organizer: {
      name: '开源社区',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=opensource'
    }
  }
])

const myActivities = ref([
  { id: 1, title: 'Vue.js 实战分享', date: '6月20日', status: 'upcoming' },
  { id: 2, title: '开源贡献指南', date: '6月25日', status: 'upcoming' },
  { id: 3, title: 'React 技术沙龙', date: '6月15日', status: 'finished' }
])

const getStatusText = (status) => {
  const statusMap = {
    upcoming: '即将开始',
    ongoing: '进行中',
    finished: '已结束'
  }
  return statusMap[status] || '未知'
}
</script>
