# 博客论坛前端

基于 Vue 3 + Vite + Tailwind CSS 构建的现代化博客论坛系统。

## 🚀 快速开始

### 安装依赖
\`\`\`bash
npm install
\`\`\`

### 启动开发服务器
\`\`\`bash
npm run dev
\`\`\`

### 构建生产版本
\`\`\`bash
npm run build
\`\`\`

### 预览生产版本
\`\`\`bash
npm run preview
\`\`\`

## 📦 技术栈

- **Vue 3** - 渐进式JavaScript框架
- **Vite** - 下一代前端构建工具
- **Vue Router** - 官方路由管理器
- **Pinia** - Vue 状态管理库
- **Tailwind CSS** - 实用优先的CSS框架
- **Axios** - HTTP客户端
- **Lucide Vue** - 美观的图标库

## 🏗️ 项目结构

\`\`\`
src/
├── api/              # API接口封装
├── components/       # 可复用组件
│   ├── common/      # 通用组件
│   ├── editor/      # 编辑器组件
│   ├── layout/      # 布局组件
│   └── post/        # 文章相关组件
├── stores/          # Pinia状态管理
├── views/           # 页面组件
├── router/          # 路由配置
├── utils/           # 工具函数
└── style.css        # 全局样式
\`\`\`

## ✨ 主要功能

### 访客功能
- 📖 浏览文章列表（排序、分页、标签筛选）
- 🔍 全局搜索功能
- 👀 查看文章详情
- 📝 用户注册和登录

### 注册用户功能
- ✍️ 发布和编辑文章（Markdown编辑器）
- 👍 点赞、收藏、分享文章
- 💬 发表评论
- 👤 个人中心管理
- 🔔 通知中心

### 管理员功能
- 🛠️ 管理后台
- 👥 用户管理
- 📋 内容管理

## 🎨 设计特色

- 📱 响应式设计，完美适配移动端
- 🎯 现代化UI设计
- ♿ 无障碍设计支持
- 🌙 支持深色模式（可扩展）
- ⚡ 优秀的性能表现

## 🔧 开发指南

### 环境变量配置

创建 `.env.local` 文件：

\`\`\`env
VITE_API_BASE_URL=http://localhost:8000/api
\`\`\`

### 代码规范

\`\`\`bash
# 代码检查
npm run lint

# 代码格式化
npm run format
\`\`\`

### 测试

\`\`\`bash
# 运行单元测试
npm run test
\`\`\`

## 📝 API接口

项目已预配置了完整的API接口封装，包括：

- 用户认证 (`/api/auth`)
- 文章管理 (`/api/posts`)
- 用户管理 (`/api/users`)
- 搜索功能 (`/api/search`)
- 标签管理 (`/api/tags`)
- 通知系统 (`/api/notifications`)

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
