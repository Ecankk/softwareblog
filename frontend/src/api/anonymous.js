/**
 * 匿名消息 API
 */
import api from './index'

export const anonymousAPI = {
  // 获取匿名消息列表
  getMessages: (params = {}) => {
    return api.get('/anonymous/messages', { params })
  },

  // 发送匿名消息
  sendMessage: (content) => {
    return api.post('/anonymous/messages', { content })
  },

  // 管理员删除消息
  deleteMessage: (messageId) => {
    return api.delete(`/anonymous/messages/${messageId}`)
  },

  // 管理员获取所有消息
  getAllMessages: (params = {}) => {
    return api.get('/admin/anonymous/messages', { params })
  }
}
