<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="bg-white rounded-lg shadow-sm p-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">社区规则</h1>
      
      <div class="space-y-8">
        <!-- 基本原则 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">基本原则</h2>
          <div class="bg-blue-50 border-l-4 border-blue-500 p-6">
            <p class="text-gray-700 leading-relaxed">
              我们致力于创建一个友好、包容、专业的技术交流社区。每位用户都应该遵守以下基本原则，
              共同维护良好的社区氛围。
            </p>
          </div>
        </section>
        
        <!-- 内容规范 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">内容规范</h2>
          <div class="space-y-4">
            <div class="border border-green-200 bg-green-50 rounded-lg p-4">
              <h3 class="text-lg font-medium text-green-800 mb-2">✅ 鼓励的内容</h3>
              <ul class="text-green-700 space-y-1">
                <li>• 原创技术文章和教程</li>
                <li>• 有价值的学习心得和经验分享</li>
                <li>• 建设性的技术讨论和问答</li>
                <li>• 开源项目介绍和代码分享</li>
                <li>• 行业动态和技术趋势分析</li>
              </ul>
            </div>
            
            <div class="border border-red-200 bg-red-50 rounded-lg p-4">
              <h3 class="text-lg font-medium text-red-800 mb-2">❌ 禁止的内容</h3>
              <ul class="text-red-700 space-y-1">
                <li>• 抄袭、盗用他人作品</li>
                <li>• 发布虚假、误导性信息</li>
                <li>• 恶意攻击、诽谤他人</li>
                <li>• 发布广告、垃圾信息</li>
                <li>• 涉及政治敏感、违法违规内容</li>
                <li>• 色情、暴力、歧视性内容</li>
              </ul>
            </div>
          </div>
        </section>
        
        <!-- 行为规范 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">行为规范</h2>
          <div class="grid md:grid-cols-2 gap-6">
            <div class="space-y-4">
              <h3 class="text-lg font-medium text-gray-900">互动礼仪</h3>
              <ul class="text-gray-600 space-y-2">
                <li>• 保持友善和尊重的态度</li>
                <li>• 使用文明用语，避免恶意言论</li>
                <li>• 理性讨论，避免人身攻击</li>
                <li>• 尊重不同观点和技术选择</li>
              </ul>
            </div>
            
            <div class="space-y-4">
              <h3 class="text-lg font-medium text-gray-900">账号管理</h3>
              <ul class="text-gray-600 space-y-2">
                <li>• 一人一号，禁止恶意注册</li>
                <li>• 保护账号安全，不要共享密码</li>
                <li>• 真实填写个人信息</li>
                <li>• 不得冒充他人身份</li>
              </ul>
            </div>
          </div>
        </section>
        
        <!-- 版权声明 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">版权声明</h2>
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
            <div class="space-y-3 text-gray-700">
              <p>• 用户发布的原创内容版权归作者所有</p>
              <p>• 转载他人内容需注明出处并获得授权</p>
              <p>• 平台有权对违规内容进行处理</p>
              <p>• 尊重知识产权，共同维护创作环境</p>
            </div>
          </div>
        </section>
        
        <!-- 违规处理 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">违规处理</h2>
          <div class="space-y-4">
            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-2">处理流程</h3>
              <ol class="text-gray-600 space-y-1">
                <li>1. 用户举报或系统检测到违规内容</li>
                <li>2. 管理员审核确认违规行为</li>
                <li>3. 根据违规程度采取相应措施</li>
                <li>4. 通知用户处理结果</li>
              </ol>
            </div>
            
            <div class="border border-gray-200 rounded-lg p-4">
              <h3 class="text-lg font-medium text-gray-900 mb-2">处理措施</h3>
              <ul class="text-gray-600 space-y-1">
                <li>• 轻微违规：删除内容，口头警告</li>
                <li>• 一般违规：限制发布权限 1-7 天</li>
                <li>• 严重违规：限制发布权限 7-30 天</li>
                <li>• 恶意违规：永久封禁账号</li>
              </ul>
            </div>
          </div>
        </section>
        
        <!-- 申诉渠道 -->
        <section>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">申诉渠道</h2>
          <div class="bg-gray-50 p-6 rounded-lg">
            <p class="text-gray-700 mb-4">
              如果您认为处理结果有误，可以通过以下方式申诉：
            </p>
            <div class="space-y-2 text-gray-600">
              <p>📧 申诉邮箱：appeal@blog.com</p>
              <p>💬 联系管理员：在线客服</p>
              <p>⏰ 申诉时效：处理决定后 7 天内</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
document.title = '社区规则 - 博客论坛'
</script>
