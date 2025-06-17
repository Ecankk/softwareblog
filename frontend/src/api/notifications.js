import api from "./index"

export const notificationsAPI = {
  // 获取通知列表
  getNotifications: (params) => api.get("/notifications", { params }),

  // 标记通知为已读
  markAsRead: (id) => api.put(`/notifications/${id}/read`),

  // 标记所有通知为已读
  markAllAsRead: () => api.put("/notifications/read-all"),

  // 删除通知
  deleteNotification: (id) => api.delete(`/notifications/${id}`),

  // 获取未读通知数量
  getUnreadCount: () => api.get("/notifications/unread-count"),
}
