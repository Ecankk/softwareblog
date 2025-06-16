// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import PostDetail from '../pages/PostDetail.vue'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Editor from '../pages/Editor.vue'

const routes = [
    { path: '/', component: Home },
    { path: '/posts/:slug', component: PostDetail },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/editor', component: Editor },
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})
