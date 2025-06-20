import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "../stores/auth"

// 页面组件
import Welcome from "../views/Welcome.vue"
import Home from "../views/Home.vue"
import PostDetail from "../views/PostDetail.vue"
import Search from "../views/Search.vue"
import Login from "../views/auth/Login.vue"
import Register from "../views/auth/Register.vue"
import UserProfile from "../views/user/UserProfile.vue"
import CreatePost from "../views/post/CreatePost.vue"
import EditPost from "../views/post/EditPost.vue"
import Admin from "../views/Admin.vue"
import AnonymousChannel from "../views/AnonymousChannel.vue"
import TestFeatures from "../views/TestFeatures.vue"
import TestFollow from "../views/TestFollow.vue"
import Analytics from "../views/Analytics.vue"
import Messages from "../views/Messages.vue"
import Settings from "../views/Settings.vue"
import Activities from "../views/Activities.vue"
import ApiDocs from "../views/ApiDocs.vue"
import Roadmap from "../views/Roadmap.vue"
import FollowTest from "../views/FollowTest.vue"
import DebugFollow from "../views/DebugFollow.vue"
import Help from "../views/Help.vue"
import Guide from "../views/Guide.vue"
import Rules from "../views/Rules.vue"
import Contact from "../views/Contact.vue"
import Feedback from "../views/Feedback.vue"

const routes = [
  {
    path: "/",
    name: "Welcome",
    component: Welcome,
    meta: { title: "欢迎" },
  },
  {
    path: "/posts",
    name: "Home",
    component: Home,
    meta: { title: "文章列表" },
  },
  {
    path: "/posts/:slug",
    name: "PostDetail",
    component: PostDetail,
    meta: { title: "文章详情" },
  },
  {
    path: "/search",
    name: "Search",
    component: Search,
    meta: { title: "搜索结果" },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: { title: "登录", guest: true },
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: { title: "注册", guest: true },
  },
  {
    path: "/user/:id",
    name: "UserProfile",
    component: UserProfile,
    meta: { title: "用户主页" },
  },
  {
    path: "/create-post",
    name: "CreatePost",
    component: CreatePost,
    meta: { title: "发布文章", requiresAuth: true },
  },
  {
    path: "/edit-post/:id",
    name: "EditPost",
    component: EditPost,
    meta: { title: "编辑文章", requiresAuth: true },
  },
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
    meta: { title: "管理后台", requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/anonymous",
    name: "AnonymousChannel",
    component: AnonymousChannel,
    meta: { title: "匿名频道", requiresAuth: true },
  },
  {
    path: "/test",
    name: "TestFeatures",
    component: TestFeatures,
    meta: { title: "功能测试" },
  },
  {
    path: "/test-follow",
    name: "TestFollow",
    component: TestFollow,
    meta: { title: "关注功能测试" },
  },
  {
    path: "/analytics",
    name: "Analytics",
    component: Analytics,
    meta: { title: "数据分析", requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/messages",
    name: "Messages",
    component: Messages,
    meta: { title: "消息中心", requiresAuth: true },
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: { title: "设置", requiresAuth: true },
  },
  {
    path: "/activities",
    name: "Activities",
    component: Activities,
    meta: { title: "社区活动" },
  },
  {
    path: "/api-docs",
    name: "ApiDocs",
    component: ApiDocs,
    meta: { title: "API 文档" },
  },
  {
    path: "/roadmap",
    name: "Roadmap",
    component: Roadmap,
    meta: { title: "产品路线图" },
  },
  {
    path: "/follow-test",
    name: "FollowTest",
    component: FollowTest,
    meta: { title: "关注功能测试" },
  },
  {
    path: "/debug-follow",
    name: "DebugFollow",
    component: DebugFollow,
    meta: { title: "关注功能调试" },
  },
  {
    path: "/help",
    name: "Help",
    component: Help,
    meta: { title: "帮助支持" },
  },
  {
    path: "/guide",
    name: "Guide",
    component: Guide,
    meta: { title: "使用指南" },
  },
  {
    path: "/rules",
    name: "Rules",
    component: Rules,
    meta: { title: "社区规则" },
  },
  {
    path: "/contact",
    name: "Contact",
    component: Contact,
    meta: { title: "联系我们" },
  },
  {
    path: "/feedback",
    name: "Feedback",
    component: Feedback,
    meta: { title: "意见反馈" },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 博客论坛` : "博客论坛"

  // 检查认证状态
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/login")
    return
  }

  // 检查管理员权限
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next("/")
    return
  }

  // 已登录用户访问登录/注册页面
  if (to.meta.guest && authStore.isAuthenticated) {
    next("/")
    return
  }

  next()
})

export default router
