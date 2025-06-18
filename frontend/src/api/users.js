import api from "./index"

export const usersAPI = {
  // 获取用户信息
  getUser: (id) => api.get(`/users/${id}`),

  // 获取用户信息（别名）
  getUserById: (id) => api.get(`/users/${id}`),

  // 获取用户详细资料
  getUserProfile: (id) => api.get(`/users/${id}/profile`),

  // 获取推荐作者
  getRecommendedAuthors: () => api.get("/users/recommended"),

  // 关注用户
  followUser: (id) => api.post(`/users/${id}/follow`),

  // 取消关注
  unfollowUser: (id) => api.delete(`/users/${id}/follow`),

  // 获取用户的文章
  getUserPosts: (id, params) => api.get(`/users/${id}/posts`, { params }),

  // 获取用户的收藏
  getUserBookmarks: (id, params) => api.get(`/users/${id}/bookmarks`, { params }),

  // 获取用户浏览历史
  getUserHistory: (id, params) => api.get(`/users/${id}/history`, { params }),

  // 记录浏览历史
  addUserHistory: (userId, postId) => {
    const formData = new FormData()
    formData.append('post_id', postId)
    return api.post(`/users/${userId}/history`, formData)
  },

  // 上传用户头像
  uploadAvatar: (userId, formData) =>
    api.post(`/users/${userId}/avatar`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
}
