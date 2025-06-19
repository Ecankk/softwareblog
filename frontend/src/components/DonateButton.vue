<template>
  <button
    @click="openDonateModal"
    :class="[
      'inline-flex items-center px-4 py-2 rounded-lg font-medium transition-all duration-200',
      variant === 'primary' 
        ? 'bg-gradient-to-r from-red-500 to-pink-500 text-white hover:from-red-600 hover:to-pink-600 shadow-md hover:shadow-lg'
        : variant === 'secondary'
        ? 'bg-white border border-red-200 text-red-600 hover:bg-red-50 hover:border-red-300'
        : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
      size === 'sm' ? 'text-sm px-3 py-1.5' : 'text-base px-4 py-2'
    ]"
  >
    <Heart :class="[
      'mr-2',
      size === 'sm' ? 'w-4 h-4' : 'w-5 h-5'
    ]" />
    {{ text }}
  </button>

  <!-- 打赏模态框 -->
  <DonateModal
    :isVisible="showDonateModal"
    :authorName="authorName"
    :authorId="authorId"
    @close="closeDonateModal"
  />
</template>

<script setup>
import { ref } from 'vue'
import { Heart } from 'lucide-vue-next'
import DonateModal from './DonateModal.vue'

const props = defineProps({
  authorName: {
    type: String,
    required: true
  },
  authorId: {
    type: Number,
    required: true
  },
  text: {
    type: String,
    default: '打赏支持'
  },
  variant: {
    type: String,
    default: 'primary', // primary, secondary, ghost
    validator: (value) => ['primary', 'secondary', 'ghost'].includes(value)
  },
  size: {
    type: String,
    default: 'md', // sm, md
    validator: (value) => ['sm', 'md'].includes(value)
  }
})

const showDonateModal = ref(false)

const openDonateModal = () => {
  showDonateModal.value = true
}

const closeDonateModal = () => {
  showDonateModal.value = false
}
</script>

<style scoped>
/* 按钮悬停效果 */
button {
  transform: translateY(0);
}

button:hover {
  transform: translateY(-1px);
}

button:active {
  transform: translateY(0);
}
</style>
