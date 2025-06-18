<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-3xl font-bold text-gray-900">消息中心</h1>
        <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2">
          <Plus class="w-4 h-4" />
          <span>新建对话</span>
        </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- 对话列表 -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow">
            <!-- 搜索和筛选 -->
            <div class="p-4 border-b">
              <div class="relative mb-4">
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="搜索对话..."
                  class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div class="flex space-x-2">
                <button 
                  v-for="filter in messageFilters" 
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

            <!-- 对话列表 -->
            <div class="divide-y divide-gray-200 max-h-96 overflow-y-auto">
              <div 
                v-for="conversation in conversations" 
                :key="conversation.id"
                :class="[
                  'p-4 hover:bg-gray-50 cursor-pointer transition-colors',
                  selectedConversation?.id === conversation.id ? 'bg-blue-50 border-r-2 border-blue-500' : ''
                ]"
                @click="selectedConversation = conversation"
              >
                <div class="flex items-center space-x-3">
                  <div class="relative">
                    <img 
                      :src="conversation.avatar" 
                      :alt="conversation.name"
                      class="w-10 h-10 rounded-full"
                    />
                    <div 
                      v-if="conversation.online"
                      class="absolute bottom-0 right-0 w-3 h-3 bg-green-400 rounded-full border-2 border-white"
                    ></div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between">
                      <p class="text-sm font-medium text-gray-900 truncate">
                        {{ conversation.name }}
                      </p>
                      <p class="text-xs text-gray-500">{{ conversation.time }}</p>
                    </div>
                    <p class="text-sm text-gray-500 truncate">{{ conversation.lastMessage }}</p>
                  </div>
                  <div v-if="conversation.unread" class="w-2 h-2 bg-blue-600 rounded-full"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 聊天区域 -->
        <div class="lg:col-span-2">
          <div v-if="selectedConversation" class="bg-white rounded-lg shadow h-96 flex flex-col">
            <!-- 聊天头部 -->
            <div class="p-4 border-b flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <img 
                  :src="selectedConversation.avatar" 
                  :alt="selectedConversation.name"
                  class="w-10 h-10 rounded-full"
                />
                <div>
                  <h3 class="font-medium text-gray-900">{{ selectedConversation.name }}</h3>
                  <p class="text-sm text-gray-500">
                    {{ selectedConversation.online ? '在线' : '离线' }}
                  </p>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <button class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                  <Phone class="w-5 h-5" />
                </button>
                <button class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                  <Video class="w-5 h-5" />
                </button>
                <button class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                  <MoreVertical class="w-5 h-5" />
                </button>
              </div>
            </div>

            <!-- 消息列表 -->
            <div class="flex-1 p-4 overflow-y-auto space-y-4">
              <div v-for="message in mockMessages" :key="message.id" 
                   :class="[
                     'flex',
                     message.sender === 'me' ? 'justify-end' : 'justify-start'
                   ]">
                <div :class="[
                  'max-w-xs lg:max-w-md px-4 py-2 rounded-lg',
                  message.sender === 'me' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-900'
                ]">
                  <p class="text-sm">{{ message.content }}</p>
                  <p :class="[
                    'text-xs mt-1',
                    message.sender === 'me' ? 'text-blue-100' : 'text-gray-500'
                  ]">
                    {{ message.time }}
                  </p>
                </div>
              </div>
            </div>

            <!-- 输入区域 -->
            <div class="p-4 border-t">
              <div class="flex items-center space-x-3">
                <button class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                  <Paperclip class="w-5 h-5" />
                </button>
                <button class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100">
                  <Smile class="w-5 h-5" />
                </button>
                <input
                  type="text"
                  placeholder="输入消息..."
                  class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button class="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700">
                  <Send class="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-else class="bg-white rounded-lg shadow h-96 flex items-center justify-center">
            <div class="text-center text-gray-500">
              <MessageCircle class="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <h3 class="text-lg font-medium text-gray-900 mb-2">选择一个对话</h3>
              <p>从左侧选择一个对话开始聊天</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能预告 -->
      <div class="mt-8 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6">
        <div class="flex items-center space-x-3 mb-4">
          <Zap class="h-6 w-6 text-green-600" />
          <h3 class="text-lg font-semibold text-gray-900">即将推出的消息功能</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">实时聊天</h4>
            <p class="text-sm text-gray-600 mt-1">WebSocket 实时消息</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">文件传输</h4>
            <p class="text-sm text-gray-600 mt-1">支持图片、文档发送</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">群组聊天</h4>
            <p class="text-sm text-gray-600 mt-1">多人群组讨论</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">消息加密</h4>
            <p class="text-sm text-gray-600 mt-1">端到端加密保护</p>
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
  Search, 
  Phone, 
  Video, 
  MoreVertical, 
  Paperclip, 
  Smile, 
  Send, 
  MessageCircle,
  Zap
} from 'lucide-vue-next'

const activeFilter = ref('all')
const selectedConversation = ref(null)

const messageFilters = [
  { key: 'all', label: '全部' },
  { key: 'unread', label: '未读' },
  { key: 'groups', label: '群组' }
]

const conversations = ref([
  {
    id: 1,
    name: '张三',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=zhang',
    lastMessage: '你好，关于那篇文章...',
    time: '2分钟前',
    unread: true,
    online: true
  },
  {
    id: 2,
    name: '李四',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=li',
    lastMessage: '谢谢你的帮助！',
    time: '1小时前',
    unread: false,
    online: false
  },
  {
    id: 3,
    name: '技术讨论群',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=group',
    lastMessage: '王五: 有人用过这个框架吗？',
    time: '3小时前',
    unread: true,
    online: true
  }
])

const mockMessages = ref([
  {
    id: 1,
    sender: 'other',
    content: '你好！看到你的文章了，写得很不错',
    time: '14:30'
  },
  {
    id: 2,
    sender: 'me',
    content: '谢谢！有什么问题可以随时交流',
    time: '14:32'
  },
  {
    id: 3,
    sender: 'other',
    content: '关于第三部分的实现，能详细说说吗？',
    time: '14:35'
  }
])
</script>
