<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 页面头部 -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">API 文档</h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          为开发者提供完整的 API 接口文档，支持第三方应用集成和扩展开发
        </p>
      </div>

      <!-- 快速开始 -->
      <div class="bg-white rounded-lg shadow p-8 mb-8">
        <h2 class="text-2xl font-semibold text-gray-900 mb-6">快速开始</h2>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4">获取 API 密钥</h3>
            <div class="bg-gray-50 rounded-lg p-4 mb-4">
              <code class="text-sm text-gray-800">
                curl -X POST https://api.blogforum.com/auth/token \<br>
                &nbsp;&nbsp;-H "Content-Type: application/json" \<br>
                &nbsp;&nbsp;-d '{"email": "your@email.com", "password": "password"}'
              </code>
            </div>
            <p class="text-sm text-gray-600">
              使用你的账户凭据获取访问令牌，用于后续 API 调用的身份验证。
            </p>
          </div>
          
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4">发起第一个请求</h3>
            <div class="bg-gray-50 rounded-lg p-4 mb-4">
              <code class="text-sm text-gray-800">
                curl -X GET https://api.blogforum.com/posts \<br>
                &nbsp;&nbsp;-H "Authorization: Bearer YOUR_TOKEN"
              </code>
            </div>
            <p class="text-sm text-gray-600">
              获取文章列表，这是一个简单的 GET 请求示例。
            </p>
          </div>
        </div>
      </div>

      <!-- API 端点列表 -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- 侧边导航 -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-lg shadow p-6 sticky top-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">API 分类</h3>
            <nav class="space-y-2">
              <button
                v-for="category in apiCategories"
                :key="category.key"
                @click="activeCategory = category.key"
                :class="[
                  'w-full text-left px-3 py-2 rounded-md text-sm transition-colors',
                  activeCategory === category.key
                    ? 'bg-blue-100 text-blue-700 font-medium'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                ]"
              >
                <div class="flex items-center space-x-2">
                  <component :is="category.icon" class="w-4 h-4" />
                  <span>{{ category.label }}</span>
                </div>
              </button>
            </nav>
          </div>
        </div>

        <!-- API 详情 -->
        <div class="lg:col-span-3">
          <div v-for="category in apiCategories" :key="category.key">
            <div v-if="activeCategory === category.key" class="space-y-6">
              <div v-for="endpoint in category.endpoints" :key="endpoint.path" class="bg-white rounded-lg shadow">
                <div class="p-6 border-b">
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center space-x-3">
                      <span :class="[
                        'px-2 py-1 rounded text-xs font-medium',
                        endpoint.method === 'GET' ? 'bg-green-100 text-green-800' :
                        endpoint.method === 'POST' ? 'bg-blue-100 text-blue-800' :
                        endpoint.method === 'PUT' ? 'bg-yellow-100 text-yellow-800' :
                        endpoint.method === 'DELETE' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      ]">
                        {{ endpoint.method }}
                      </span>
                      <code class="text-sm font-mono text-gray-800">{{ endpoint.path }}</code>
                    </div>
                    <button class="text-blue-600 hover:text-blue-800 text-sm">
                      试用 API
                    </button>
                  </div>
                  <h4 class="text-lg font-medium text-gray-900 mb-2">{{ endpoint.title }}</h4>
                  <p class="text-gray-600">{{ endpoint.description }}</p>
                </div>

                <div class="p-6">
                  <!-- 参数 -->
                  <div v-if="endpoint.parameters" class="mb-6">
                    <h5 class="text-sm font-medium text-gray-900 mb-3">参数</h5>
                    <div class="overflow-x-auto">
                      <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                          <tr>
                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">名称</th>
                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">类型</th>
                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">必需</th>
                            <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">描述</th>
                          </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                          <tr v-for="param in endpoint.parameters" :key="param.name">
                            <td class="px-4 py-2 text-sm font-mono text-gray-900">{{ param.name }}</td>
                            <td class="px-4 py-2 text-sm text-gray-600">{{ param.type }}</td>
                            <td class="px-4 py-2 text-sm">
                              <span :class="[
                                'px-2 py-1 rounded-full text-xs',
                                param.required ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'
                              ]">
                                {{ param.required ? '必需' : '可选' }}
                              </span>
                            </td>
                            <td class="px-4 py-2 text-sm text-gray-600">{{ param.description }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <!-- 示例请求 -->
                  <div class="mb-6">
                    <h5 class="text-sm font-medium text-gray-900 mb-3">示例请求</h5>
                    <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                      <pre class="text-sm text-green-400"><code>{{ endpoint.example }}</code></pre>
                    </div>
                  </div>

                  <!-- 响应示例 -->
                  <div>
                    <h5 class="text-sm font-medium text-gray-900 mb-3">响应示例</h5>
                    <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                      <pre class="text-sm text-blue-400"><code>{{ endpoint.response }}</code></pre>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- SDK 和工具 -->
      <div class="mt-12 bg-white rounded-lg shadow p-8">
        <h2 class="text-2xl font-semibold text-gray-900 mb-6">SDK 和开发工具</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="sdk in sdks" :key="sdk.name" class="border rounded-lg p-6 hover:shadow-md transition-shadow">
            <div class="flex items-center space-x-3 mb-4">
              <component :is="sdk.icon" class="w-8 h-8 text-blue-600" />
              <h3 class="text-lg font-medium text-gray-900">{{ sdk.name }}</h3>
            </div>
            <p class="text-gray-600 mb-4">{{ sdk.description }}</p>
            <div class="flex space-x-3">
              <button class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700">
                下载
              </button>
              <button class="border border-gray-300 text-gray-700 px-4 py-2 rounded-md text-sm hover:bg-gray-50">
                文档
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能预告 -->
      <div class="mt-8 bg-gradient-to-r from-indigo-50 to-cyan-50 rounded-lg p-6">
        <div class="flex items-center space-x-3 mb-4">
          <Zap class="h-6 w-6 text-indigo-600" />
          <h3 class="text-lg font-semibold text-gray-900">即将推出的 API 功能</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">GraphQL 支持</h4>
            <p class="text-sm text-gray-600 mt-1">灵活的数据查询</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">Webhook 通知</h4>
            <p class="text-sm text-gray-600 mt-1">实时事件推送</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">批量操作</h4>
            <p class="text-sm text-gray-600 mt-1">高效的批量处理</p>
          </div>
          <div class="bg-white rounded-lg p-4">
            <h4 class="font-medium text-gray-900">API 版本控制</h4>
            <p class="text-sm text-gray-600 mt-1">向后兼容保证</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  FileText, 
  Users, 
  MessageCircle, 
  Heart, 
  Shield,
  Code,
  Smartphone,
  Globe,
  Zap
} from 'lucide-vue-next'

const activeCategory = ref('posts')

const apiCategories = [
  {
    key: 'posts',
    label: '文章管理',
    icon: FileText,
    endpoints: [
      {
        method: 'GET',
        path: '/api/posts',
        title: '获取文章列表',
        description: '获取分页的文章列表，支持筛选和排序',
        parameters: [
          { name: 'page', type: 'integer', required: false, description: '页码，默认为 1' },
          { name: 'limit', type: 'integer', required: false, description: '每页数量，默认为 20' },
          { name: 'tag', type: 'string', required: false, description: '按标签筛选' }
        ],
        example: `curl -X GET "https://api.blogforum.com/posts?page=1&limit=10" \\
  -H "Authorization: Bearer YOUR_TOKEN"`,
        response: `{
  "items": [
    {
      "id": 1,
      "title": "示例文章",
      "content": "文章内容...",
      "author": {
        "id": 1,
        "username": "作者名"
      },
      "created_at": "2024-06-18T10:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "limit": 10
}`
      }
    ]
  },
  {
    key: 'users',
    label: '用户管理',
    icon: Users,
    endpoints: [
      {
        method: 'GET',
        path: '/api/users/{id}',
        title: '获取用户信息',
        description: '根据用户 ID 获取用户详细信息',
        parameters: [
          { name: 'id', type: 'integer', required: true, description: '用户 ID' }
        ],
        example: `curl -X GET "https://api.blogforum.com/users/1" \\
  -H "Authorization: Bearer YOUR_TOKEN"`,
        response: `{
  "id": 1,
  "username": "示例用户",
  "email": "user@example.com",
  "avatar": "https://...",
  "bio": "用户简介",
  "created_at": "2024-01-01T00:00:00Z"
}`
      }
    ]
  },
  {
    key: 'comments',
    label: '评论系统',
    icon: MessageCircle,
    endpoints: []
  },
  {
    key: 'auth',
    label: '身份认证',
    icon: Shield,
    endpoints: []
  }
]

const sdks = [
  {
    name: 'JavaScript SDK',
    description: '适用于 Web 和 Node.js 应用的官方 SDK',
    icon: Code
  },
  {
    name: 'Python SDK',
    description: '适用于 Python 应用的官方 SDK',
    icon: Code
  },
  {
    name: 'Mobile SDK',
    description: '适用于 iOS 和 Android 的移动端 SDK',
    icon: Smartphone
  }
]
</script>
