# 端口管理指南

## 🎯 **解决端口变化问题的完整方案**

本文档介绍如何防止和解决端口变化导致的配置问题。

## 📋 **问题背景**

在开发过程中，端口变化会导致以下问题：
- 前端无法连接到后端API
- 头像和静态资源加载失败
- 开发环境配置不一致
- 部署时端口冲突

## 🔧 **解决方案架构**

### **1. 统一配置管理**
```
frontend/src/config/index.js  # 统一配置文件
├── 开发环境配置
├── 生产环境配置
├── 测试环境配置
└── 动态端口检测
```

### **2. 自动化脚本**
```
scripts/
├── detect-port.js     # 端口检测脚本
├── start-dev.js       # 开发环境启动脚本
└── check-config.js    # 配置检查脚本
```

### **3. 健康检查机制**
```
后端API: /health       # 健康检查端点
前端配置: 自动检测      # 动态端口发现
```

## 🚀 **使用方法**

### **快速启动（推荐）**
```bash
# 自动检测端口并启动前后端服务
npm run dev
```

### **手动端口检测**
```bash
# 检测当前运行的API端口
npm run detect-port
```

### **配置检查**
```bash
# 检查项目配置完整性
node scripts/check-config.js
```

### **分别启动服务**
```bash
# 启动后端
npm run start:backend

# 启动前端
npm run start:frontend
```

## 📁 **配置文件说明**

### **环境变量配置**
```env
# frontend/.env.development
VITE_API_BASE_URL=http://localhost:9000
VITE_WS_BASE_URL=ws://localhost:9000
VITE_APP_TITLE=博客论坛
VITE_APP_VERSION=1.0.0
```

### **应用配置**
```javascript
// frontend/src/config/index.js
export const config = {
  API_BASE_URL: 'http://localhost:9000',
  WS_BASE_URL: 'ws://localhost:9000',
  // ... 其他配置
}
```

### **代理配置**
```javascript
// frontend/vite.config.js
server: {
  proxy: {
    "/api": {
      target: "http://localhost:9000",
      changeOrigin: true,
    },
  },
}
```

## 🔍 **端口检测机制**

### **自动检测流程**
1. 检查常用端口：9000, 8000, 8001, 8080
2. 调用健康检查端点：`/health`
3. 更新前端配置文件
4. 重启开发服务器

### **健康检查端点**
```json
GET /health
{
  "status": "healthy",
  "service": "博客论坛 API",
  "version": "1.0.0",
  "timestamp": "2025-06-18T16:41:17.959653",
  "port": 9000
}
```

## 🛠️ **故障排除**

### **端口被占用**
```bash
# 查看端口占用
netstat -ano | findstr :9000

# 杀死占用进程
taskkill /PID <进程ID> /F

# 或使用脚本自动检测可用端口
npm run detect-port
```

### **配置不一致**
```bash
# 检查配置完整性
node scripts/check-config.js

# 重新生成配置
npm run detect-port
```

### **前端连接失败**
```bash
# 1. 确认后端服务运行
curl http://localhost:9000/health

# 2. 检查前端配置
cat frontend/.env.development

# 3. 重启前端服务
cd frontend && npm run dev
```

## 📊 **监控和日志**

### **配置检查报告**
运行配置检查后会生成报告：
```json
// config-check-report.json
{
  "timestamp": "2025-06-18T16:41:17.959Z",
  "results": {
    "files": true,
    "json": true,
    "env": true,
    "ports": true
  },
  "recommendations": []
}
```

### **端口检测报告**
运行端口检测后会生成报告：
```json
// port-detection-report.json
{
  "timestamp": "2025-06-18T16:41:17.959Z",
  "detectedPort": 9000,
  "checkedPorts": [9000, 8000, 8001, 8080],
  "configFiles": [...]
}
```

## 🎯 **最佳实践**

### **开发环境**
1. 使用 `npm run dev` 启动项目
2. 定期运行 `node scripts/check-config.js` 检查配置
3. 遇到端口问题时运行 `npm run detect-port`

### **生产环境**
1. 使用环境变量配置端口
2. 设置健康检查监控
3. 使用反向代理（Nginx）

### **团队协作**
1. 提交 `.env.example` 文件
2. 不提交 `.env.development` 文件
3. 使用统一的启动脚本

## 🔄 **自动化流程**

### **开发启动流程**
```
npm run dev
├── 检测现有API服务
├── 查找可用端口
├── 启动后端服务（如需要）
├── 更新前端配置
├── 启动前端服务
└── 显示服务地址
```

### **配置更新流程**
```
npm run detect-port
├── 检测API端口
├── 更新 .env.development
├── 更新 vite.config.js
├── 生成检测报告
└── 提示重启服务
```

## 📝 **常用命令**

```bash
# 项目启动
npm run dev                    # 自动启动前后端
npm run start:backend          # 只启动后端
npm run start:frontend         # 只启动前端

# 配置管理
npm run detect-port            # 检测并更新端口配置
node scripts/check-config.js   # 检查配置完整性

# 依赖安装
npm run install:all            # 安装前后端依赖

# 项目构建
npm run build                  # 构建前端项目
```

## 🎉 **优势总结**

✅ **自动化**：无需手动修改配置文件
✅ **智能检测**：自动发现可用端口
✅ **统一管理**：所有配置集中管理
✅ **错误预防**：配置检查和验证
✅ **团队友好**：标准化的启动流程
✅ **生产就绪**：支持多环境配置

通过这套端口管理方案，可以彻底解决端口变化导致的配置问题！
