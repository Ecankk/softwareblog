import api from "./index"

export const followsAPI = {
  // 关注用户
  followUser: (userId) => api.post(`/users/${userId}/follow`),

  // 取消关注用户
  unfollowUser: (userId) => api.delete(`/users/${userId}/follow`),

  // 检查关注状态
  checkFollowStatus: (userId) => api.get(`/users/${userId}/follow/status`),

  // 获取用户的关注列表
  getUserFollowing: (userId) => api.get(`/users/${userId}/following`),

  // 获取用户的粉丝列表
  getUserFollowers: (userId) => api.get(`/users/${userId}/followers`),
}
