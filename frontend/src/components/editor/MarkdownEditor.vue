<template>
  <div class="markdown-editor">
    <div class="border border-gray-300 rounded-lg overflow-hidden">
      <!-- 工具栏 -->
      <div class="bg-gray-50 border-b border-gray-300 p-2 flex items-center space-x-2">
        <button
          @click="insertMarkdown('**', '**')"
          class="p-2 hover:bg-gray-200 rounded"
          title="粗体"
        >
          <Bold class="w-4 h-4" />
        </button>
        <button
          @click="insertMarkdown('*', '*')"
          class="p-2 hover:bg-gray-200 rounded"
          title="斜体"
        >
          <Italic class="w-4 h-4" />
        </button>
        <button
          @click="insertMarkdown('# ', '')"
          class="p-2 hover:bg-gray-200 rounded"
          title="标题"
        >
          <Heading class="w-4 h-4" />
        </button>
        <button
          @click="insertMarkdown('[', '](url)')"
          class="p-2 hover:bg-gray-200 rounded"
          title="链接"
        >
          <Link class="w-4 h-4" />
        </button>
        <button
          @click="insertMarkdown('```\n', '\n```')"
          class="p-2 hover:bg-gray-200 rounded"
          title="代码块"
        >
          <Code class="w-4 h-4" />
        </button>
        <div class="flex-1"></div>
        <button
          @click="togglePreview"
          :class="[
            'p-2 rounded',
            showPreview ? 'bg-blue-100 text-blue-600' : 'hover:bg-gray-200'
          ]"
          title="预览"
        >
          <Eye class="w-4 h-4" />
        </button>
      </div>
      
      <!-- 编辑区域 -->
      <div class="flex" style="height: 400px;">
        <!-- 编辑器 -->
        <div :class="['flex-1', showPreview && 'border-r border-gray-300']">
          <textarea
            ref="textareaRef"
            v-model="content"
            @input="handleInput"
            @keydown="handleKeydown"
            class="w-full h-full p-4 resize-none border-none outline-none font-mono text-sm"
            placeholder="请输入Markdown内容..."
          ></textarea>
        </div>
        
        <!-- 预览区域 -->
        <div v-if="showPreview" class="flex-1 p-4 bg-gray-50 overflow-y-auto">
          <div class="prose prose-sm max-w-none" v-html="renderedContent"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { Bold, Italic, Heading, Link, Code, Eye } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const textareaRef = ref(null)
const showPreview = ref(false)

const content = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 简单的Markdown渲染（实际项目中建议使用marked或markdown-it）
const renderedContent = computed(() => {
  let html = content.value
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*)\*/gim, '<em>$1</em>')
    .replace(/!\[([^\]]*)\]$$([^$$]*)\)/gim, '<img alt="$1" src="$2" />')
    .replace(/\[([^\]]*)\]$$([^$$]*)\)/gim, '<a href="$2">$1</a>')
    .replace(/\n/gim, '<br>')
  
  return html
})

const handleInput = (event) => {
  content.value = event.target.value
}

const handleKeydown = (event) => {
  // Tab键插入空格
  if (event.key === 'Tab') {
    event.preventDefault()
    const start = event.target.selectionStart
    const end = event.target.selectionEnd
    const value = event.target.value
    event.target.value = value.substring(0, start) + '  ' + value.substring(end)
    event.target.selectionStart = event.target.selectionEnd = start + 2
    handleInput(event)
  }
}

const insertMarkdown = async (before, after) => {
  const textarea = textareaRef.value
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selectedText = textarea.value.substring(start, end)
  
  const newText = before + selectedText + after
  const newValue = textarea.value.substring(0, start) + newText + textarea.value.substring(end)
  
  content.value = newValue
  
  await nextTick()
  textarea.focus()
  textarea.selectionStart = start + before.length
  textarea.selectionEnd = start + before.length + selectedText.length
}

const togglePreview = () => {
  showPreview.value = !showPreview.value
}
</script>

<style scoped>
.prose h1 {
  @apply text-2xl font-bold mb-4;
}

.prose h2 {
  @apply text-xl font-bold mb-3;
}

.prose h3 {
  @apply text-lg font-bold mb-2;
}

.prose p {
  @apply mb-2;
}

.prose strong {
  @apply font-bold;
}

.prose em {
  @apply italic;
}

.prose a {
  @apply text-blue-600 hover:text-blue-800 underline;
}

.prose img {
  @apply max-w-full h-auto rounded;
}
</style>
