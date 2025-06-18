import api from "./index"

export const adminAPI = {
  // 获取系统统计信息
  getStats: () => api.get("/admin/stats"),

  // 用户管理
  getAllUsers: (params) => api.get("/admin/users", { params }),
  deleteUser: (userId) => api.delete(`/admin/users/${userId}`),

  // 文章管理
  getAllPosts: (params) => api.get("/admin/posts", { params }),
  deletePost: (postId) => api.delete(`/admin/posts/${postId}`),

  // 评论管理
  getAllComments: (params) => api.get("/admin/comments", { params }),
  deleteComment: (commentId) => api.delete(`/admin/comments/${commentId}`),
}
