<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">设置</h1>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- 侧边导航 -->
        <div class="lg:col-span-1">
          <nav class="space-y-1">
            <button
              v-for="tab in settingTabs"
              :key="tab.key"
              @click="activeTab = tab.key"
              :class="[
                'w-full flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors',
                activeTab === tab.key
                  ? 'bg-blue-100 text-blue-700'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
              ]"
            >
              <component :is="tab.icon" class="w-5 h-5 mr-3" />
              {{ tab.label }}
            </button>
          </nav>
        </div>

        <!-- 设置内容 -->
        <div class="lg:col-span-3">
          <!-- 个人资料 -->
          <div v-if="activeTab === 'profile'" class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">个人资料</h2>
            
            <div class="space-y-6">
              <!-- 头像设置 -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">头像</label>
                <div class="flex items-center space-x-4">
                  <img 
                    src="https://api.dicebear.com/7.x/avataaars/svg?seed=current" 
                    alt="当前头像"
                    class="w-16 h-16 rounded-full"
                  />
                  <div>
                    <button class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700">
                      更换头像
                    </button>
                    <p class="text-sm text-gray-500 mt-1">支持 JPG、PNG 格式，最大 2MB</p>
                  </div>
                </div>
              </div>

              <!-- 基本信息 -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
                  <input 
                    type="text" 
                    value="示例用户"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
                  <input 
                    type="email" 
                    value="user@example.com"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">个人简介</label>
                <textarea 
                  rows="4"
                  placeholder="介绍一下自己..."
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                ></textarea>
              </div>

              <div class="flex justify-end">
                <button class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700">
                  保存更改
                </button>
              </div>
            </div>
          </div>

          <!-- 通知设置 -->
          <div v-if="activeTab === 'notifications'" class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">通知设置</h2>
            
            <div class="space-y-6">
              <div v-for="notification in notificationSettings" :key="notification.key">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-sm font-medium text-gray-900">{{ notification.title }}</h3>
                    <p class="text-sm text-gray-500">{{ notification.description }}</p>
                  </div>
                  <div class="flex space-x-4">
                    <label class="flex items-center">
                      <input type="checkbox" :checked="notification.email" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                      <span class="ml-2 text-sm text-gray-700">邮箱</span>
                    </label>
                    <label class="flex items-center">
                      <input type="checkbox" :checked="notification.push" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500" />
                      <span class="ml-2 text-sm text-gray-700">推送</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 隐私设置 -->
          <div v-if="activeTab === 'privacy'" class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">隐私设置</h2>
            
            <div class="space-y-6">
              <div v-for="privacy in privacySettings" :key="privacy.key">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-sm font-medium text-gray-900">{{ privacy.title }}</h3>
                    <p class="text-sm text-gray-500">{{ privacy.description }}</p>
                  </div>
                  <select class="border border-gray-300 rounded-md px-3 py-2 text-sm">
                    <option v-for="option in privacy.options" :key="option.value" :value="option.value">
                      {{ option.label }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>

          <!-- 安全设置 -->
          <div v-if="activeTab === 'security'" class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">安全设置</h2>
            
            <div class="space-y-6">
              <!-- 密码修改 -->
              <div>
                <h3 class="text-sm font-medium text-gray-900 mb-4">修改密码</h3>
                <div class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">当前密码</label>
                    <input 
                      type="password" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">新密码</label>
                    <input 
                      type="password" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">确认新密码</label>
                    <input 
                      type="password" 
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <button class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700">
                    更新密码
                  </button>
                </div>
              </div>

              <!-- 两步验证 -->
              <div class="border-t pt-6">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-sm font-medium text-gray-900">两步验证</h3>
                    <p class="text-sm text-gray-500">为账户添加额外的安全保护</p>
                  </div>
                  <button class="bg-green-600 text-white px-4 py-2 rounded-md text-sm hover:bg-green-700">
                    启用
                  </button>
                </div>
              </div>

              <!-- 登录设备 -->
              <div class="border-t pt-6">
                <h3 class="text-sm font-medium text-gray-900 mb-4">登录设备</h3>
                <div class="space-y-3">
                  <div v-for="device in loginDevices" :key="device.id" class="flex items-center justify-between p-3 border rounded-lg">
                    <div class="flex items-center space-x-3">
                      <component :is="device.icon" class="w-5 h-5 text-gray-400" />
                      <div>
                        <p class="text-sm font-medium text-gray-900">{{ device.name }}</p>
                        <p class="text-sm text-gray-500">{{ device.location }} • {{ device.time }}</p>
                      </div>
                    </div>
                    <button v-if="!device.current" class="text-red-600 hover:text-red-800 text-sm">
                      注销
                    </button>
                    <span v-else class="text-green-600 text-sm">当前设备</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 主题设置 -->
          <div v-if="activeTab === 'appearance'" class="bg-white rounded-lg shadow p-6">
            <h2 class="text-xl font-semibold text-gray-900 mb-6">外观设置</h2>
            
            <div class="space-y-6">
              <!-- 主题选择 -->
              <div>
                <h3 class="text-sm font-medium text-gray-900 mb-4">主题</h3>
                <div class="grid grid-cols-3 gap-4">
                  <div v-for="theme in themes" :key="theme.key" 
                       :class="[
                         'p-4 border-2 rounded-lg cursor-pointer transition-colors',
                         selectedTheme === theme.key ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                       ]"
                       @click="selectedTheme = theme.key">
                    <div :class="['w-full h-20 rounded mb-2', theme.preview]"></div>
                    <p class="text-sm font-medium text-center">{{ theme.name }}</p>
                  </div>
                </div>
              </div>

              <!-- 字体大小 -->
              <div>
                <h3 class="text-sm font-medium text-gray-900 mb-4">字体大小</h3>
                <div class="flex items-center space-x-4">
                  <span class="text-sm text-gray-500">小</span>
                  <input type="range" min="12" max="20" value="14" class="flex-1" />
                  <span class="text-sm text-gray-500">大</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能预告 -->
      <div class="mt-8 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6">
        <div class="flex items-center space-x-3 mb-4">
          <Zap class="h-6 w-6 text-purple-600" />
          <h3 class="text-lg font-semibold text-gray-900">即将推出的设置功能</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">数据导出</h4>
            <p class="text-sm text-gray-600 mt-1">导出个人数据</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">API 密钥</h4>
            <p class="text-sm text-gray-600 mt-1">第三方应用集成</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">高级自定义</h4>
            <p class="text-sm text-gray-600 mt-1">更多个性化选项</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  User, 
  Bell, 
  Shield, 
  Lock, 
  Palette, 
  Monitor,
  Smartphone,
  Zap
} from 'lucide-vue-next'

const activeTab = ref('profile')
const selectedTheme = ref('light')

const settingTabs = [
  { key: 'profile', label: '个人资料', icon: User },
  { key: 'notifications', label: '通知', icon: Bell },
  { key: 'privacy', label: '隐私', icon: Shield },
  { key: 'security', label: '安全', icon: Lock },
  { key: 'appearance', label: '外观', icon: Palette }
]

const notificationSettings = [
  {
    key: 'comments',
    title: '新评论',
    description: '有人评论了你的文章',
    email: true,
    push: true
  },
  {
    key: 'follows',
    title: '新关注者',
    description: '有人关注了你',
    email: true,
    push: false
  },
  {
    key: 'likes',
    title: '点赞通知',
    description: '有人点赞了你的内容',
    email: false,
    push: true
  }
]

const privacySettings = [
  {
    key: 'profile_visibility',
    title: '个人资料可见性',
    description: '谁可以查看你的个人资料',
    options: [
      { value: 'public', label: '所有人' },
      { value: 'followers', label: '仅关注者' },
      { value: 'private', label: '仅自己' }
    ]
  },
  {
    key: 'email_visibility',
    title: '邮箱可见性',
    description: '是否在个人资料中显示邮箱',
    options: [
      { value: 'public', label: '公开' },
      { value: 'private', label: '隐藏' }
    ]
  }
]

const loginDevices = [
  {
    id: 1,
    name: 'Windows PC',
    location: '北京',
    time: '当前',
    current: true,
    icon: Monitor
  },
  {
    id: 2,
    name: 'iPhone 15',
    location: '上海',
    time: '2天前',
    current: false,
    icon: Smartphone
  }
]

const themes = [
  {
    key: 'light',
    name: '浅色',
    preview: 'bg-gradient-to-br from-white to-gray-100'
  },
  {
    key: 'dark',
    name: '深色',
    preview: 'bg-gradient-to-br from-gray-800 to-gray-900'
  },
  {
    key: 'auto',
    name: '自动',
    preview: 'bg-gradient-to-br from-blue-100 to-purple-100'
  }
]
</script>
