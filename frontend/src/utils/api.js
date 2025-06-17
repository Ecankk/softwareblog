// src/utils/api.js
import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000', // 如果后端跑在别的地址／端口，请调整
})

export const fetchPosts = () => api.get('/posts')
export const fetchPost = slug => api.get(`/posts/${slug}`)
