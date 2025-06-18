import api from "./index"

export const postsAPI = {
  // 获取文章列表
  getPosts: (params) => api.get("/posts", { params }),

  // 获取文章详情（通过slug）
  getPost: (slug) => api.get(`/posts/${slug}`),

  // 获取文章详情（通过ID，用于编辑）
  getPostById: (id) => api.get(`/posts/id/${id}`),

  // 创建文章
  createPost: (postData) => api.post("/posts", postData),

  // 更新文章
  updatePost: (id, postData) => api.put(`/posts/${id}`, postData),

  // 删除文章
  deletePost: (id) => api.delete(`/posts/${id}`),

  // 点赞文章
  likePost: (id) => api.post(`/posts/${id}/like`),

  // 取消点赞
  unlikePost: (id) => api.delete(`/posts/${id}/like`),

  // 转发文章
  sharePost: (id, shareData) => api.post(`/posts/${id}/share`, shareData),

  // 举报文章
  reportPost: (id, reportData) => api.post(`/posts/${id}/report`, reportData),

  // 收藏文章
  bookmarkPost: (id) => api.post(`/posts/${id}/bookmark`),

  // 取消收藏
  unbookmarkPost: (id) => api.delete(`/posts/${id}/bookmark`),

  // 上传封面图
  uploadCover: (formData) =>
    api.post("/posts/upload-cover", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }),

  // 搜索文章
  searchPosts: (query, params) =>
    api.get("/posts/search", {
      params: { q: query, ...params },
    }),
}
