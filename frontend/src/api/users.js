import api from "./index"

export const usersAPI = {
  // 获取用户信息
  getUser: (id) => api.get(`/users/${id}`),

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
}
