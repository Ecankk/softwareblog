<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="bg-white rounded-lg shadow-sm p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">发布文章</h1>
      
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- 标题 -->
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
            文章标题 *
          </label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            required
            class="input-field"
            placeholder="请输入文章标题"
          />
        </div>
        
        <!-- 摘要 -->
        <div>
          <label for="summary" class="block text-sm font-medium text-gray-700 mb-2">
            文章摘要
          </label>
          <textarea
            id="summary"
            v-model="form.summary"
            rows="3"
            class="input-field"
            placeholder="请输入文章摘要（可选）"
          ></textarea>
        </div>
        
        <!-- 封面图 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            封面图片
          </label>
          <div class="flex items-center space-x-4">
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              @change="handleFileChange"
              class="hidden"
            />
            <button
              type="button"
              @click="$refs.fileInput.click()"
              class="btn-secondary"
            >
              <Upload class="w-4 h-4 mr-2" />
              选择图片
            </button>
            <span v-if="form.coverImage" class="text-sm text-gray-600">
              {{ form.coverImage.name }}
            </span>
          </div>
          <div v-if="coverPreview" class="mt-4">
            <img :src="coverPreview" alt="封面预览" class="max-w-xs h-32 object-cover rounded-lg" />
          </div>
        </div>
        
        <!-- 标签 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            标签
          </label>
          <div class="flex flex-wrap gap-2 mb-2">
            <span
              v-for="tag in form.tags"
              :key="tag"
              class="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
            >
              {{ tag }}
              <button
                type="button"
                @click="removeTag(tag)"
                class="ml-2 text-blue-600 hover:text-blue-800"
              >
                <X class="w-3 h-3" />
              </button>
            </span>
          </div>
          <div class="flex items-center space-x-2">
            <input
              v-model="newTag"
              @keyup.enter="addTag"
              type="text"
              class="input-field"
              placeholder="输入标签后按回车添加"
            />
            <button
              type="button"
              @click="addTag"
              class="btn-secondary"
            >
              添加
            </button>
          </div>
        </div>
        
        <!-- 内容编辑器 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            文章内容 *
          </label>
          <MarkdownEditor v-model="form.content" />
        </div>
        
        <!-- 发布选项 -->
        <div class="flex items-center space-x-4">
          <label class="flex items-center">
            <input
              v-model="form.isDraft"
              type="checkbox"
              class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span class="ml-2 text-sm text-gray-700">保存为草稿</span>
          </label>
        </div>
        
        <!-- 提交按钮 -->
        <div class="flex justify-end space-x-4">
          <button
            type="button"
            @click="$router.go(-1)"
            class="btn-secondary"
          >
            取消
          </button>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="btn-primary disabled:opacity-50"
          >
            <span v-if="isSubmitting">发布中...</span>
            <span v-else>{{ form.isDraft ? '保存草稿' : '发布文章' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { Upload, X } from 'lucide-vue-next'
import { useAuthStore } from '../../stores/auth'
import { useToastStore } from '../../stores/toast'
import { postsAPI } from '../../api/posts'
import MarkdownEditor from '../../components/editor/MarkdownEditor.vue'

const router = useRouter()
const authStore = useAuthStore()
const toastStore = useToastStore()

const isSubmitting = ref(false)
const newTag = ref('')
const coverPreview = ref('')

const form = reactive({
  title: '',
  summary: '',
  content: '',
  tags: [],
  coverImage: null,
  isDraft: false
})

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    form.coverImage = file
    
    // 创建预览
    const reader = new FileReader()
    reader.onload = (e) => {
      coverPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const addTag = () => {
  const tag = newTag.value.trim()
  if (tag && !form.tags.includes(tag)) {
    form.tags.push(tag)
    newTag.value = ''
  }
}

const removeTag = (tag) => {
  const index = form.tags.indexOf(tag)
  if (index > -1) {
    form.tags.splice(index, 1)
  }
}

const handleSubmit = async () => {
  if (!form.title.trim() || !form.content.trim()) {
    toastStore.error('请填写标题和内容')
    return
  }
  
  isSubmitting.value = true
  
  try {
    const formData = new FormData()
    formData.append('title', form.title)
    formData.append('content', form.content)
    formData.append('summary', form.summary)
    formData.append('tags', JSON.stringify(form.tags))
    formData.append('is_draft', form.isDraft)
    
    if (form.coverImage) {
      formData.append('cover_image', form.coverImage)
    }
    
    const response = await postsAPI.createPost(formData)
    
    toastStore.success(form.isDraft ? '草稿保存成功' : '文章发布成功')
    router.push(`/post/${response.data.slug}`)
  } catch (error) {
    toastStore.error(error.response?.data?.detail || '发布失败')
  } finally {
    isSubmitting.value = false
  }
}
</script>
