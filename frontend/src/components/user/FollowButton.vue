<template>
  <button
    @click="handleFollow"
    :disabled="loading || !authStore.isAuthenticated || isCurrentUser"
    :class="[
      'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center space-x-2',
      isCurrentUser
        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
        : isFollowing
          ? 'bg-gray-100 text-gray-700 hover:bg-red-50 hover:text-red-600 border border-gray-300 follow-btn'
          : 'bg-blue-600 text-white hover:bg-blue-700',
      loading && 'opacity-50 cursor-not-allowed'
    ]"
  >
    <div v-if="loading" class="animate-spin rounded-full h-4 w-4 border-2 border-current border-t-transparent"></div>

    <template v-else-if="isCurrentUser">
      <User class="w-4 h-4" />
      <span>这是你</span>
    </template>

    <template v-else-if="isFollowing">
      <UserCheck class="w-4 h-4" />
      <span class="follow-text">已关注</span>
      <span class="unfollow-text hidden">取消关注</span>
    </template>

    <template v-else>
      <UserPlus class="w-4 h-4" />
      <span>关注</span>
    </template>
  </button>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { User, UserPlus, UserCheck } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { followsAPI } from '../../api/follows'

const props = defineProps({
  userId: {
    type: Number,
    required: true
  },
  initialFollowStatus: {
    type: Boolean,
    default: undefined
  }
})

const emit = defineEmits(['follow-changed'])

const authStore = useAuthStore()
const toastStore = useToastStore()

const isFollowing = ref(false)
const loading = ref(false)

// 是否是当前用户
const isCurrentUser = computed(() => {
  return authStore.user?.id === props.userId
})

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

// 监听初始状态变化
watch(() => props.initialFollowStatus, (newStatus) => {
  if (newStatus !== undefined) {
    isFollowing.value = newStatus
  }
}, { immediate: true })

// 监听用户ID变化，重新检查状态
watch(() => props.userId, () => {
  if (props.initialFollowStatus === undefined) {
    checkFollowStatus()
  }
})

onMounted(() => {
  // 如果没有传入初始状态，主动检查
  if (props.initialFollowStatus === undefined) {
    checkFollowStatus()
  }
})
</script>

<style scoped>
/* 悬停时显示取消关注文本 */
.follow-btn:hover .follow-text {
  @apply hidden;
}

.follow-btn:hover .unfollow-text {
  @apply inline;
}
</style>
