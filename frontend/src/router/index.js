import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "../stores/auth"

// 页面组件
import Home from "../views/Home.vue"
import PostDetail from "../views/PostDetail.vue"
import Search from "../views/Search.vue"
import Login from "../views/auth/Login.vue"
import Register from "../views/auth/Register.vue"
import UserProfile from "../views/user/UserProfile.vue"
import CreatePost from "../views/post/CreatePost.vue"
import EditPost from "../views/post/EditPost.vue"
import AdminDashboard from "../views/admin/AdminDashboard.vue"
import AnonymousChannel from "../views/AnonymousChannel.vue"

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: { title: "首页" },
  },
  {
    path: "/post/:slug",
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
    meta: { title: "个人中心", requiresAuth: true },
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
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { title: "管理后台", requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/anonymous",
    name: "AnonymousChannel",
    component: AnonymousChannel,
    meta: { title: "匿名频道", requiresAuth: true },
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
