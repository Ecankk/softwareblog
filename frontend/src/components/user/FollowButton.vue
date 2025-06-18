<template>
  <button
    @click="handleFollow"
    :disabled="loading || !authStore.isAuthenticated"
    :class="[
      'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
      isFollowing
        ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        : 'bg-blue-600 text-white hover:bg-blue-700',
      loading && 'opacity-50 cursor-not-allowed',
      !authStore.isAuthenticated && 'opacity-50 cursor-not-allowed'
    ]"
  >
    <span v-if="loading">
      {{ isFollowing ? '取消关注中...' : '关注中...' }}
    </span>
    <span v-else>
      {{ isFollowing ? '已关注' : '关注' }}
    </span>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { followsAPI } from '../../api/follows'

const props = defineProps({
  userId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['follow-changed'])

const authStore = useAuthStore()
const toastStore = useToastStore()

const isFollowing = ref(false)
const loading = ref(false)

const checkFollowStatus = async () => {
  if (!authStore.isAuthenticated || authStore.user?.id === props.userId) {
    return
  }

  try {
    const response = await followsAPI.checkFollowStatus(props.userId)
    isFollowing.value = response.data.isFollowing
  } catch (error) {
    console.error('检查关注状态失败:', error)
  }
}

const handleFollow = async () => {
  if (!authStore.isAuthenticated) {
    toastStore.error('请先登录')
    return
  }

  if (authStore.user?.id === props.userId) {
    toastStore.error('不能关注自己')
    return
  }

  loading.value = true

  try {
    if (isFollowing.value) {
      await followsAPI.unfollowUser(props.userId)
      isFollowing.value = false
      toastStore.success('取消关注成功')
    } else {
      await followsAPI.followUser(props.userId)
      isFollowing.value = true
      toastStore.success('关注成功')
    }

    emit('follow-changed', {
      userId: props.userId,
      isFollowing: isFollowing.value
    })
  } catch (error) {
    console.error('关注操作失败:', error)
    toastStore.error(error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  checkFollowStatus()
})
</script>
