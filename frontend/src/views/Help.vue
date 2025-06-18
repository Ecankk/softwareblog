<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow-sm p-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">帮助支持</h1>
      
      <div class="space-y-8">
        <!-- 常见问题 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">常见问题</h2>
          <div class="space-y-4">
            <div class="border-l-4 border-blue-500 pl-4">
              <h3 class="text-lg font-medium text-gray-900">如何发布文章？</h3>
              <p class="text-gray-600 mt-2">
                登录后点击右上角的"写文章"按钮，使用Markdown编辑器编写内容，添加标签后点击发布即可。
              </p>
            </div>
            
            <div class="border-l-4 border-green-500 pl-4">
              <h3 class="text-lg font-medium text-gray-900">如何关注其他用户？</h3>
              <p class="text-gray-600 mt-2">
                访问用户主页，点击"关注"按钮即可关注该用户，关注后可以在通知中心收到相关动态。
              </p>
            </div>
            
            <div class="border-l-4 border-purple-500 pl-4">
              <h3 class="text-lg font-medium text-gray-900">如何修改个人信息？</h3>
              <p class="text-gray-600 mt-2">
                点击右上角头像进入个人中心，在个人资料页面可以修改用户名、个人简介和头像。
              </p>
            </div>
            
            <div class="border-l-4 border-red-500 pl-4">
              <h3 class="text-lg font-medium text-gray-900">忘记密码怎么办？</h3>
              <p class="text-gray-600 mt-2">
                请联系管理员重置密码，或发送邮件到 admin@blog.com 申请密码重置。
              </p>
            </div>
          </div>
        </section>
        
        <!-- 功能介绍 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">功能介绍</h2>
          <div class="grid md:grid-cols-2 gap-6">
            <div class="bg-gray-50 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-900 mb-3">文章编辑</h3>
              <ul class="text-gray-600 space-y-2">
                <li>• 支持Markdown语法</li>
                <li>• 实时预览功能</li>
                <li>• 代码高亮显示</li>
                <li>• 图片上传支持</li>
              </ul>
            </div>
            
            <div class="bg-gray-50 p-6 rounded-lg">
              <h3 class="text-lg font-medium text-gray-900 mb-3">社交功能</h3>
              <ul class="text-gray-600 space-y-2">
                <li>• 用户关注系统</li>
                <li>• 评论和回复</li>
                <li>• 实时通知</li>
                <li>• 个性化头像</li>
              </ul>
            </div>
          </div>
        </section>
        
        <!-- 联系方式 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">需要帮助？</h2>
          <div class="bg-blue-50 p-6 rounded-lg">
            <p class="text-gray-700 mb-4">
              如果您遇到任何问题或有建议，请通过以下方式联系我们：
            </p>
            <div class="space-y-2 text-gray-600">
              <p>📧 邮箱：admin@blog.com</p>
              <p>💬 在线客服：工作日 9:00-18:00</p>
              <p>📱 QQ群：123456789</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
// 设置页面标题
document.title = '帮助支持 - 博客论坛'
</script>
