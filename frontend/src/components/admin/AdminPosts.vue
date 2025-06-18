<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-900">文章管理</h2>
      <div class="text-sm text-gray-500">
        共 {{ totalPosts }} 篇文章
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>

    <!-- 文章列表 -->
    <div v-else class="bg-white shadow rounded-lg overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                文章信息
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                作者
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                统计
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                创建时间
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="post in posts" :key="post.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="flex flex-col">
                  <div class="text-sm font-medium text-gray-900 max-w-xs truncate">
                    {{ post.title }}
                  </div>
                  <div class="text-sm text-gray-500 max-w-xs truncate">
                    {{ post.summary || '无摘要' }}
                  </div>
                  <div class="flex flex-wrap gap-1 mt-1">
                    <span 
                      v-for="tag in post.tags?.slice(0, 3)" 
                      :key="tag"
                      class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <img 
                    :src="getAvatarUrl(post.author)" 
                    :alt="post.author?.username"
                    class="h-8 w-8 rounded-full mr-3"
                  />
                  <div>
                    <div class="text-sm font-medium text-gray-900">
                      {{ post.author?.username || '未知用户' }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ post.author?.email }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900">
                  <div>{{ post.likes_count || 0 }} 点赞</div>
                  <div>{{ post.comment_count || 0 }} 评论</div>
                  <div>{{ post.views_count || 0 }} 浏览</div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500">
                {{ formatDate(post.created_at) }}
              </td>
              <td class="px-6 py-4 text-sm font-medium space-x-2">
                <router-link 
                  :to="`/post/${post.slug}`"
                  class="text-blue-600 hover:text-blue-900"
                  target="_blank"
                >
                  查看
                </router-link>
                <router-link 
                  :to="`/edit-post/${post.id}`"
                  class="text-green-600 hover:text-green-900"
                >
                  编辑
                </router-link>
                <button 
                  @click="confirmDelete(post)"
                  class="text-red-600 hover:text-red-900"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div v-if="totalPosts > limit" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
        <div class="flex items-center justify-between">
          <div class="text-sm text-gray-700">
            显示第 {{ (currentPage - 1) * limit + 1 }} 到 {{ Math.min(currentPage * limit, totalPosts) }} 条，共 {{ totalPosts }} 条
          </div>
          <div class="flex space-x-2">
            <button
              @click="loadPosts(currentPage - 1)"
              :disabled="currentPage <= 1"
              class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
            >
              上一页
            </button>
            <button
              @click="loadPosts(currentPage + 1)"
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
        <h3 class="text-lg font-medium text-gray-900 mb-4">确认删除</h3>
        <p class="text-sm text-gray-500 mb-6">
          确定要删除文章 "{{ postToDelete?.title }}" 吗？此操作不可撤销。
        </p>
        <div class="flex justify-end space-x-3">
          <button
            @click="showDeleteDialog = false"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            取消
          </button>
          <button
            @click="deletePost"
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
import { ref, onMounted } from 'vue'
import { useToastStore } from '../../stores/toast'
import { adminAPI } from '../../api/admin'
import { getAvatarUrl } from '../../utils/avatar'

const toastStore = useToastStore()

const posts = ref([])
const loading = ref(false)
const deleting = ref(false)
const currentPage = ref(1)
const limit = ref(20)
const totalPosts = ref(0)
const hasMore = ref(false)
const showDeleteDialog = ref(false)
const postToDelete = ref(null)

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '未知'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 加载文章列表
const loadPosts = async (page = 1) => {
  loading.value = true
  try {
    const response = await adminAPI.getAllPosts({ page, limit: limit.value })
    const data = response.data || response
    
    posts.value = data.items || []
    totalPosts.value = data.total || 0
    hasMore.value = data.has_more || false
    currentPage.value = page
  } catch (error) {
    console.error('获取文章列表失败:', error)
    toastStore.showToast('获取文章列表失败', 'error')
  } finally {
    loading.value = false
  }
}

// 确认删除
const confirmDelete = (post) => {
  postToDelete.value = post
  showDeleteDialog.value = true
}

// 删除文章
const deletePost = async () => {
  if (!postToDelete.value) return

  deleting.value = true
  try {
    await adminAPI.deletePost(postToDelete.value.id)
    toastStore.showToast('文章删除成功', 'success')
    showDeleteDialog.value = false
    postToDelete.value = null
    
    // 重新加载当前页
    await loadPosts(currentPage.value)
  } catch (error) {
    console.error('删除文章失败:', error)
    toastStore.showToast('删除文章失败', 'error')
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadPosts()
})
</script>
