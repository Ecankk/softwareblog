<script setup>
import NavBar from '../components/NavBar.vue'

const articles = [
  {
    title: '如何使用 Vue3 构建现代博客系统？',
    author: '小明',
    date: '2025-06-17',
    summary: '本文介绍如何使用 Vue3 + Vite + Tailwind 打造一个现代化博客平台……',
  },
  {
    title: '前端部署到华为云详细流程',
    author: '小红',
    date: '2025-06-16',
    summary: '华为云部署步骤全解析，从构建打包到 Nginx 配置，手把手教你上线项目……',
  },
  // 你也可以从后端获取数据
]
</script>

<template>
  <NavBar />

  <main class="p-4">
    <div class="grid gap-6 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="(article, i) in articles" :key="i" class="card bg-white shadow hover:shadow-xl transition">
        <div class="card-body">
          <h2 class="card-title">{{ article.title }}</h2>
          <p class="text-sm text-gray-500">{{ article.author }} · {{ article.date }}</p>
          <p class="text-gray-700">{{ article.summary }}</p>
          <div class="card-actions justify-end">
            <button class="btn btn-sm btn-outline">查看详情</button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
