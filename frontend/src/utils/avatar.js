/**
 * 头像处理工具函数
 */

import { API_BASE_URL } from '../config'

/**
 * 获取用户头像URL
 * @param {Object} user - 用户对象
 * @param {number} size - 头像尺寸（可选）
 * @returns {string} 头像URL
 */
export const getAvatarUrl = (user, size = 40) => {
  if (!user) {
    return `/placeholder.svg?height=${size}&width=${size}`
  }

  // 如果是SVG头像路径（/users/xxx/avatar.svg）
  if (user.avatar && user.avatar.startsWith('/users/')) {
    return `${API_BASE_URL}${user.avatar}`
  }

  // 如果是静态文件路径（/static/avatars/xxx.jpg）
  if (user.avatar && user.avatar.startsWith('/static/')) {
    return `${API_BASE_URL}${user.avatar}`
  }

  // 如果是其他完整URL
  if (user.avatar && (user.avatar.startsWith('http://') || user.avatar.startsWith('https://'))) {
    return user.avatar
  }

  // 如果没有头像或头像路径无效，使用默认SVG头像
  return `${API_BASE_URL}/users/${user.id}/avatar.svg`
}

/**
 * 处理头像加载错误
 * @param {Event} event - 错误事件
 * @param {Object} user - 用户对象
 * @param {number} size - 头像尺寸（可选）
 */
export const handleAvatarError = (event, user, size = 40) => {
  if (user?.id) {
    // 尝试使用SVG生成头像
    event.target.src = `${API_BASE_URL}/users/${user.id}/avatar.svg`
  } else {
    // 使用占位符
    event.target.src = `/placeholder.svg?height=${size}&width=${size}`
  }
}

/**
 * 创建头像错误处理函数
 * @param {Object} user - 用户对象
 * @param {number} size - 头像尺寸（可选）
 * @returns {Function} 错误处理函数
 */
export const createAvatarErrorHandler = (user, size = 40) => {
  return (event) => handleAvatarError(event, user, size)
}
