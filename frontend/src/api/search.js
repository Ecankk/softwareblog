import api from "./index"

export const searchAPI = {
  // 获取搜索建议
  getSuggestions: (query) => api.get("/search/suggestions", { params: { q: query } }),

  // 搜索文章
  searchPosts: (query, params) => api.get("/search/posts", { params: { q: query, ...params } }),

  // 搜索用户
  searchUsers: (query, params) => api.get("/search/users", { params: { q: query, ...params } }),

  // 搜索标签
  searchTags: (query, params) => api.get("/search/tags", { params: { q: query, ...params } }),
}
