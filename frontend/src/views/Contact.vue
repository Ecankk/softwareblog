<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow-sm p-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">联系我们</h1>
      
      <div class="grid md:grid-cols-2 gap-8">
        <!-- 联系方式 -->
        <div class="space-y-6">
          <section>
            <h2 class="text-2xl font-semibold text-gray-800 mb-4">联系方式</h2>
            <div class="space-y-4">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <span class="text-blue-600 text-lg">📧</span>
                </div>
                <div>
                  <p class="font-medium text-gray-900">邮箱</p>
                  <p class="text-gray-600">admin@blog.com</p>
                </div>
              </div>
              
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <span class="text-green-600 text-lg">💬</span>
                </div>
                <div>
                  <p class="font-medium text-gray-900">在线客服</p>
                  <p class="text-gray-600">工作日 9:00-18:00</p>
                </div>
              </div>
              
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <span class="text-purple-600 text-lg">📱</span>
                </div>
                <div>
                  <p class="font-medium text-gray-900">QQ群</p>
                  <p class="text-gray-600">123456789</p>
                </div>
              </div>
              
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                  <span class="text-red-600 text-lg">🐙</span>
                </div>
                <div>
                  <p class="font-medium text-gray-900">GitHub</p>
                  <p class="text-gray-600">github.com/blog-forum</p>
                </div>
              </div>
            </div>
          </section>
          
          <section>
            <h2 class="text-2xl font-semibold text-gray-800 mb-4">团队介绍</h2>
            <div class="bg-gray-50 p-6 rounded-lg">
              <p class="text-gray-700 leading-relaxed">
                我们是一个专注于技术分享和交流的团队，致力于为开发者提供优质的内容平台。
                如果您有任何建议或想法，欢迎随时与我们联系。
              </p>
            </div>
          </section>
        </div>
        
        <!-- 联系表单 -->
        <div>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">发送消息</h2>
          <form @submit.prevent="submitForm" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">姓名</label>
              <input
                v-model="form.name"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入您的姓名"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
              <input
                v-model="form.email"
                type="email"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请输入您的邮箱"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">主题</label>
              <select
                v-model="form.subject"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">请选择主题</option>
                <option value="bug">Bug反馈</option>
                <option value="feature">功能建议</option>
                <option value="cooperation">合作咨询</option>
                <option value="other">其他问题</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">消息内容</label>
              <textarea
                v-model="form.message"
                required
                rows="6"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请详细描述您的问题或建议..."
              ></textarea>
            </div>
            
            <button
              type="submit"
              :disabled="submitting"
              class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {{ submitting ? '发送中...' : '发送消息' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToastStore } from '../stores/toast'

const toastStore = useToastStore()

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const submitting = ref(false)

const submitForm = async () => {
  submitting.value = true
  
  try {
    // 模拟发送请求
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    toastStore.success('消息发送成功！我们会尽快回复您。')
    
    // 重置表单
    form.value = {
      name: '',
      email: '',
      subject: '',
      message: ''
    }
  } catch (error) {
    toastStore.error('发送失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

document.title = '联系我们 - 博客论坛'
</script>
