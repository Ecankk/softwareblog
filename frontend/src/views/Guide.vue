<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow-sm p-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">使用指南</h1>
      
      <div class="space-y-8">
        <!-- 快速开始 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">快速开始</h2>
          <div class="space-y-6">
            <div class="flex items-start space-x-4">
              <div class="flex-shrink-0 w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">1</div>
              <div>
                <h3 class="text-lg font-medium text-gray-900">注册账号</h3>
                <p class="text-gray-600 mt-1">使用邮箱注册账号，验证邮箱后即可开始使用。</p>
              </div>
            </div>
            
            <div class="flex items-start space-x-4">
              <div class="flex-shrink-0 w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center font-bold">2</div>
              <div>
                <h3 class="text-lg font-medium text-gray-900">完善个人资料</h3>
                <p class="text-gray-600 mt-1">设置用户名、个人简介和头像，让其他用户更好地了解您。</p>
              </div>
            </div>
            
            <div class="flex items-start space-x-4">
              <div class="flex-shrink-0 w-8 h-8 bg-purple-500 text-white rounded-full flex items-center justify-center font-bold">3</div>
              <div>
                <h3 class="text-lg font-medium text-gray-900">发布第一篇文章</h3>
                <p class="text-gray-600 mt-1">点击"写文章"按钮，使用Markdown编辑器创作您的第一篇文章。</p>
              </div>
            </div>
            
            <div class="flex items-start space-x-4">
              <div class="flex-shrink-0 w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center font-bold">4</div>
              <div>
                <h3 class="text-lg font-medium text-gray-900">互动交流</h3>
                <p class="text-gray-600 mt-1">关注感兴趣的用户，评论和点赞优质内容，参与社区讨论。</p>
              </div>
            </div>
          </div>
        </section>
        
        <!-- Markdown 语法指南 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">Markdown 语法指南</h2>
          <div class="bg-gray-50 p-6 rounded-lg">
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <h3 class="font-medium text-gray-900 mb-3">基础语法</h3>
                <div class="space-y-2 text-sm">
                  <div><code class="bg-gray-200 px-2 py-1 rounded"># 一级标题</code></div>
                  <div><code class="bg-gray-200 px-2 py-1 rounded">## 二级标题</code></div>
                  <div><code class="bg-gray-200 px-2 py-1 rounded">**粗体文本**</code></div>
                  <div><code class="bg-gray-200 px-2 py-1 rounded">*斜体文本*</code></div>
                  <div><code class="bg-gray-200 px-2 py-1 rounded">[链接](URL)</code></div>
                </div>
              </div>
              
              <div>
                <h3 class="font-medium text-gray-900 mb-3">高级语法</h3>
                <div class="space-y-2 text-sm">
                  <div><code class="bg-gray-200 px-2 py-1 rounded">```代码块```</code></div>
                  <div><code class="bg-gray-200 px-2 py-1 rounded">- 无序列表</code></div>
                  <div><code class="bg-gray-200 px-2 py-1 rounded">1. 有序列表</code></div>
                  <div><code class="bg-gray-200 px-2 py-1 rounded">> 引用文本</code></div>
                  <div><code class="bg-gray-200 px-2 py-1 rounded">![图片](URL)</code></div>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        <!-- 社区功能 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">社区功能详解</h2>
          <div class="space-y-4">
            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-2">关注系统</h3>
              <p class="text-gray-600">关注您感兴趣的作者，及时获取他们的最新动态和文章更新。</p>
            </div>
            
            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-2">通知中心</h3>
              <p class="text-gray-600">接收关注、评论、点赞等互动通知，不错过任何重要消息。</p>
            </div>
            
            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-2">标签系统</h3>
              <p class="text-gray-600">为文章添加相关标签，帮助其他用户更容易发现您的内容。</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
document.title = '使用指南 - 博客论坛'
</script>
