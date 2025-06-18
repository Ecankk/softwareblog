<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-900">用户管理</h2>
      <div class="text-sm text-gray-500">
        共 {{ totalUsers }} 个用户
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- 用户列表 -->
    <div v-else class="bg-white shadow rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                用户信息
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                角色
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                统计
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                注册时间
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <img 
                    :src="getAvatarUrl(user)" 
                    :alt="user.username"
                    class="h-10 w-10 rounded-full mr-4"
                  />
                  <div>
                    <div class="text-sm font-medium text-gray-900">
                      {{ user.username || '未设置用户名' }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ user.email }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span 
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    user.role === 'admin' 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-green-100 text-green-800'
                  ]"
                >
                  {{ user.role === 'admin' ? '管理员' : '普通用户' }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">
                  <div>{{ user.post_count || 0 }} 篇文章</div>
                  <div>{{ user.comment_count || 0 }} 条评论</div>
                  <div>{{ user.followers_count || 0 }} 粉丝</div>
                  <div>{{ user.following_count || 0 }} 关注</div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                {{ formatDate(user.created_at) }}
              </td>
              <td class="px-6 py-4 text-sm font-medium space-x-2">
                <router-link 
                  :to="`/user/${user.id}`"
                  class="text-blue-600 hover:text-blue-900"
                  target="_blank"
                >
                  查看
                </router-link>
                <button 
                  v-if="user.role !== 'admin' && user.id !== currentUserId"
                  @click="confirmDelete(user)"
                  class="text-red-600 hover:text-red-900"
                >
                  删除
                </button>
                <span 
                  v-else-if="user.role === 'admin'"
                  class="text-gray-400"
                >
                  管理员
                </span>
                <span 
                  v-else
                  class="text-gray-400"
                >
                  当前用户
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div v-if="totalUsers > limit" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-700">
            显示第 {{ (currentPage - 1) * limit + 1 }} 到 {{ Math.min(currentPage * limit, totalUsers) }} 条，共 {{ totalUsers }} 条
          </div>
          <div class="flex space-x-2">
            <button
              @click="loadUsers(currentPage - 1)"
              :disabled="currentPage <= 1"
              class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              上一页
            </button>
            <button
              @click="loadUsers(currentPage + 1)"
              :disabled="!hasMore"
              class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              下一页
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 删除确认对话框 -->
    <div v-if="showDeleteDialog" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-medium text-gray-900 mb-4">确认删除用户</h3>
        <p class="text-sm text-gray-500 mb-6">
          确定要删除用户 "{{ userToDelete?.username || userToDelete?.email }}" 吗？
          <br><br>
          <strong class="text-red-600">警告：此操作将删除该用户的所有数据，包括文章、评论等，且不可撤销！</strong>
        </p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteDialog = false"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            取消
          </button>
          <button
            @click="deleteUser"
            :disabled="deleting"
            class="px-4 py-2 bg-red-600 text-white rounded-md text-sm font-medium hover:bg-red-700 disabled:opacity-50"
          >
            {{ deleting ? '删除中...' : '确认删除' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { adminAPI } from '../../api/admin'
import { getAvatarUrl } from '../../utils/avatar'

const authStore = useAuthStore()
const toastStore = useToastStore()

const users = ref([])
const loading = ref(false)
const deleting = ref(false)
const currentPage = ref(1)
const limit = ref(20)
const totalUsers = ref(0)
const hasMore = ref(false)
const showDeleteDialog = ref(false)
const userToDelete = ref(null)

// 当前用户ID
const currentUserId = computed(() => authStore.user?.id)

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 加载用户列表
const loadUsers = async (page = 1) => {
  loading.value = true
  try {
    const response = await adminAPI.getAllUsers({ page, limit: limit.value })
    const data = response.data || response
    
    users.value = data.items || []
    totalUsers.value = data.total || 0
    hasMore.value = data.has_more || false
    currentPage.value = page
  } catch (error) {
    console.error('获取用户列表失败:', error)
    toastStore.showToast('获取用户列表失败', 'error')
  } finally {
    loading.value = false
  }
}

// 确认删除
const confirmDelete = (user) => {
  userToDelete.value = user
  showDeleteDialog.value = true
}

// 删除用户
const deleteUser = async () => {
  if (!userToDelete.value) return

  deleting.value = true
  try {
    await adminAPI.deleteUser(userToDelete.value.id)
    toastStore.showToast('用户删除成功', 'success')
    showDeleteDialog.value = false
    userToDelete.value = null
    
    // 重新加载当前页
    await loadUsers(currentPage.value)
  } catch (error) {
    console.error('删除用户失败:', error)
    toastStore.showToast('删除用户失败', 'error')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadUsers()
})
</script>
