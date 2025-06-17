import api from "./index"

export const tagsAPI = {
  // 获取所有标签
  getTags: () => api.get("/tags"),

  // 获取热门标签
  getPopularTags: () => api.get("/tags/popular"),

  // 创建标签
  createTag: (tagData) => api.post("/tags", tagData),

  // 删除标签
  deleteTag: (id) => api.delete(`/tags/${id}`),
}
