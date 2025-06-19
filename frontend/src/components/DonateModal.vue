<template>
  <div v-if="isVisible" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click="closeModal">
    <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4 relative" @click.stop>
      <!-- 关闭按钮 -->
      <button @click="closeModal" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors">
        <X class="w-6 h-6" />
      </button>

      <!-- 标题 -->
      <div class="text-center mb-6">
        <div class="flex items-center justify-center mb-2">
          <Heart class="w-6 h-6 text-red-500 mr-2" />
          <h3 class="text-xl font-semibold text-gray-800">
            打赏支持 {{ authorName }}
          </h3>
        </div>
        <p class="text-gray-600 text-sm">
          如果您觉得作者的内容对您有帮助，可以请作者喝杯咖啡 ☕
        </p>
      </div>

      <!-- 收款码区域 -->
      <div class="text-center mb-6">
        <div class="bg-gray-50 rounded-lg p-4 mb-4">
          <img :src="qrCodeUrl" :alt="`${authorName}的收款码`" class="w-48 h-48 mx-auto rounded-lg shadow-sm"
            @error="handleImageError" />
        </div>

        <!-- 支付方式标识 -->
        <div class="flex items-center justify-center space-x-4 mb-4">
          <div class="flex items-center text-blue-600">
            <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-2">
              <span class="text-xs font-bold">支</span>
            </div>
            <span class="text-sm">支付宝</span>
          </div>
          <div class="text-gray-300">|</div>
          <div class="flex items-center text-green-600">
            <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mr-2">
              <span class="text-xs font-bold">微</span>
            </div>
            <span class="text-sm">微信支付</span>
          </div>
        </div>

        <p class="text-gray-500 text-xs">
          使用支付宝或微信扫描上方二维码即可打赏
        </p>
      </div>

      <!-- 预设金额按钮 -->
      <div class="mb-6">
        <p class="text-sm text-gray-600 mb-3 text-center">快速选择金额</p>
        <div class="grid grid-cols-4 gap-2">
          <button v-for="amount in presetAmounts" :key="amount" @click="selectAmount(amount)" :class="[
            'py-2 px-3 rounded-lg border text-sm font-medium transition-colors',
            selectedAmount === amount
              ? 'border-blue-500 bg-blue-50 text-blue-600'
              : 'border-gray-200 text-gray-600 hover:border-gray-300'
          ]">
            ¥{{ amount }}
          </button>
        </div>
      </div>

      <!-- 感谢信息 -->
      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
        <div class="flex items-start">
          <Gift class="w-5 h-5 text-yellow-600 mr-2 mt-0.5" />
          <div class="text-sm">
            <p class="text-yellow-800 font-medium mb-1">感谢您的支持！</p>
            <p class="text-yellow-700">
              您的打赏将激励作者创作更多优质内容
            </p>
          </div>
        </div>
      </div>

      <!-- 底部按钮 -->
      <div class="flex space-x-3">
        <button @click="closeModal"
          class="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors">
          取消
        </button>
        <button @click="handleDonate"
          class="flex-1 py-2 px-4 bg-gradient-to-r from-red-500 to-pink-500 text-white rounded-lg hover:from-red-600 hover:to-pink-600 transition-colors">
          <Heart class="w-4 h-4 inline mr-1" />
          打赏支持
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { X, Heart, Gift } from 'lucide-vue-next'
import { useToastStore } from '../stores/toast'

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  authorName: {
    type: String,
    default: '作者'
  },
  authorId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['close'])

const toastStore = useToastStore()

// 预设打赏金额
const presetAmounts = [5, 10, 20, 50]
const selectedAmount = ref(10)

// 收款码URL - 你可以根据作者ID动态设置不同的收款码
const qrCodeUrl = computed(() => {
  // 这里可以根据作者ID返回不同的收款码
  // 目前统一使用一个收款码，如果没有则使用占位符
  return '/images/donate/alipay-qr.jpg'
})

// 选择金额
const selectAmount = (amount) => {
  selectedAmount.value = amount
}

// 关闭模态框
const closeModal = () => {
  emit('close')
}

// 处理图片加载错误
const handleImageError = (event) => {
  // 如果图片加载失败，使用占位符
  event.target.src = '/images/donate/placeholder.svg'
  toastStore.info('正在使用示例收款码，请联系作者获取真实收款码')
}

// 处理打赏
const handleDonate = () => {
  toastStore.success(`感谢您的 ¥${selectedAmount.value} 打赏支持！`)
  closeModal()
}
</script>

<style scoped>
/* 模态框动画 */
.fixed {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.bg-white {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
