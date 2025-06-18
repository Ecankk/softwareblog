/**
 * 关注系统 API
 */

import { api } from './index'

export const followAPI = {
  // 关注用户
  async followUser(userId) {
    try {
      const response = await api.post(`/users/${userId}/follow`)
      return response.data
    } catch (error) {
      console.error('关注用户失败:', error)
      throw error
    }
  },

  // 取消关注用户
  async unfollowUser(userId) {
    try {
      const response = await api.delete(`/users/${userId}/follow`)
      return response.data
    } catch (error) {
      console.error('取消关注失败:', error)
      throw error
    }
  },

  // 检查关注状态
  async checkFollowStatus(userId) {
    try {
      const response = await api.get(`/users/${userId}/follow/status`)
      return response.data
    } catch (error) {
      console.error('检查关注状态失败:', error)
      throw error
    }
  },

  // 获取用户的关注列表
  async getUserFollowing(userId) {
    try {
      const response = await api.get(`/users/${userId}/following`)
      return response.data
    } catch (error) {
      console.error('获取关注列表失败:', error)
      throw error
    }
  },

  // 获取用户的粉丝列表
  async getUserFollowers(userId) {
    try {
      const response = await api.get(`/users/${userId}/followers`)
      return response.data
    } catch (error) {
      console.error('获取粉丝列表失败:', error)
      throw error
    }
  }
}
