import api from "./index"

export const commentsAPI = {
  // 获取文章评论
  getPostComments: (postId) => api.get(`/posts/${postId}/comments`),

  // 创建评论
  createComment: (postId, commentData) => api.post(`/posts/${postId}/comments`, commentData),

  // 删除评论
  deleteComment: (commentId) => api.delete(`/comments/${commentId}`),

  // 点赞评论
  likeComment: (commentId) => api.post(`/comments/${commentId}/like`),

  // 获取用户的评论
  getUserComments: (userId, params) => api.get(`/users/${userId}/comments`, { params }),
}
