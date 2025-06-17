import api from "./index"

export const authAPI = {
  // 登录
  login: (credentials) => api.post("/auth/login", credentials),

  // 注册
  register: (userData) => api.post("/auth/register", userData),

  // 获取用户信息
  getProfile: () => api.get("/auth/profile"),

  // 更新用户信息
  updateProfile: (profileData) => api.put("/auth/profile", profileData),

  // 上传头像
  uploadAvatar: (formData) =>
    api.post("/auth/upload-avatar", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }),

  // 修改密码
  changePassword: (passwordData) => api.put("/auth/change-password", passwordData),
}
