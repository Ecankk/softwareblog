<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow-sm p-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">意见反馈</h1>
      
      <div class="grid md:grid-cols-2 gap-8">
        <!-- 反馈表单 -->
        <div>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">提交反馈</h2>
          <form @submit.prevent="submitFeedback" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">反馈类型</label>
              <select
                v-model="feedback.type"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">请选择反馈类型</option>
                <option value="bug">Bug报告</option>
                <option value="feature">功能建议</option>
                <option value="ui">界面优化</option>
                <option value="performance">性能问题</option>
                <option value="content">内容问题</option>
                <option value="other">其他</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">优先级</label>
              <div class="flex space-x-4">
                <label class="flex items-center">
                  <input
                    v-model="feedback.priority"
                    type="radio"
                    value="low"
                    class="mr-2"
                  />
                  <span class="text-green-600">低</span>
                </label>
                <label class="flex items-center">
                  <input
                    v-model="feedback.priority"
                    type="radio"
                    value="medium"
                    class="mr-2"
                  />
                  <span class="text-yellow-600">中</span>
                </label>
                <label class="flex items-center">
                  <input
                    v-model="feedback.priority"
                    type="radio"
                    value="high"
                    class="mr-2"
                  />
                  <span class="text-red-600">高</span>
                </label>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">标题</label>
              <input
                v-model="feedback.title"
                type="text"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="简要描述问题或建议"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">详细描述</label>
              <textarea
                v-model="feedback.description"
                required
                rows="6"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="请详细描述您遇到的问题或建议..."
              ></textarea>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">重现步骤（可选）</label>
              <textarea
                v-model="feedback.steps"
                rows="3"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="如果是Bug，请描述重现步骤..."
              ></textarea>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">联系方式（可选）</label>
              <input
                v-model="feedback.contact"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="如需回复，请留下邮箱"
              />
            </div>
            
            <button
              type="submit"
              :disabled="submitting"
              class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {{ submitting ? '提交中...' : '提交反馈' }}
            </button>
          </form>
        </div>
        
        <!-- 反馈指南 -->
        <div class="space-y-6">
          <section>
            <h2 class="text-2xl font-semibold text-gray-800 mb-4">反馈指南</h2>
            <div class="space-y-4">
              <div class="bg-blue-50 border-l-4 border-blue-500 p-4">
                <h3 class="font-medium text-blue-800 mb-2">Bug报告</h3>
                <p class="text-blue-700 text-sm">
                  请详细描述问题现象、重现步骤、预期结果和实际结果。
                </p>
              </div>
              
              <div class="bg-green-50 border-l-4 border-green-500 p-4">
                <h3 class="font-medium text-green-800 mb-2">功能建议</h3>
                <p class="text-green-700 text-sm">
                  说明建议的功能、使用场景和预期效果。
                </p>
              </div>
              
              <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4">
                <h3 class="font-medium text-yellow-800 mb-2">界面优化</h3>
                <p class="text-yellow-700 text-sm">
                  描述当前界面的不足和改进建议。
                </p>
              </div>
            </div>
          </section>
          
          <section>
            <h2 class="text-2xl font-semibold text-gray-800 mb-4">处理流程</h2>
            <div class="space-y-3">
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">1</div>
                <span class="text-gray-700">收到反馈</span>
              </div>
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-sm font-bold">2</div>
                <span class="text-gray-700">评估优先级</span>
              </div>
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 bg-purple-500 text-white rounded-full flex items-center justify-center text-sm font-bold">3</div>
                <span class="text-gray-700">安排处理</span>
              </div>
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center text-sm font-bold">4</div>
                <span class="text-gray-700">反馈结果</span>
              </div>
            </div>
          </section>
          
          <section>
            <h2 class="text-2xl font-semibold text-gray-800 mb-4">感谢支持</h2>
            <div class="bg-gray-50 p-6 rounded-lg">
              <p class="text-gray-700 leading-relaxed">
                您的每一条反馈都是我们改进的动力。我们会认真对待每一个建议，
                持续优化产品体验。感谢您的支持！
              </p>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToastStore } from '../stores/toast'

const toastStore = useToastStore()

const feedback = ref({
  type: '',
  priority: 'medium',
  title: '',
  description: '',
  steps: '',
  contact: ''
})

const submitting = ref(false)

const submitFeedback = async () => {
  submitting.value = true
  
  try {
    // 模拟提交请求
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    toastStore.success('反馈提交成功！感谢您的建议。')
    
    // 重置表单
    feedback.value = {
      type: '',
      priority: 'medium',
      title: '',
      description: '',
      steps: '',
      contact: ''
    }
  } catch (error) {
    toastStore.error('提交失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

document.title = '意见反馈 - 博客论坛'
</script>
