# 前端部署指南

## 系统要求

- **Node.js**: 16.0+ (推荐 18.0+)
- **npm**: 8.0+ 或 **yarn**: 1.22+
- **操作系统**: Linux/Windows/macOS

## 快速部署

### 1. 安装依赖

```bash
# 使用npm
npm install

# 或使用yarn
yarn install
```

### 2. 环境配置

创建 `.env.production` 文件：

```env
# API配置
VITE_API_BASE_URL=https://your-api-domain.com

# 其他配置
VITE_APP_TITLE=博客论坛系统
VITE_APP_VERSION=1.0.0
```

### 3. 构建生产版本

```bash
# 构建
npm run build

# 或
yarn build
```

### 4. 部署到服务器

#### 方式1: 静态文件服务器

```bash
# 将dist目录上传到服务器
scp -r dist/* user@server:/var/www/html/

# 或使用rsync
rsync -av dist/ user@server:/var/www/html/
```

#### 方式2: Nginx配置

```nginx
server {
    listen 80;
    server_name your-frontend-domain.com;
    root /var/www/html;
    index index.html;

    # 处理Vue Router的history模式
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### 方式3: 使用PM2 + serve

```bash
# 安装serve
npm install -g serve pm2

# 启动服务
pm2 start "serve -s dist -l 3000" --name "blog-frontend"

# 保存PM2配置
pm2 save
pm2 startup
```

## Docker部署

创建 `Dockerfile`:

```dockerfile
# 构建阶段
FROM node:18-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

创建 `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
```

构建和运行：

```bash
# 构建镜像
docker build -t blog-frontend .

# 运行容器
docker run -d -p 80:80 blog-frontend
```

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `VITE_API_BASE_URL` | 后端API地址 | `http://localhost:8000` |
| `VITE_APP_TITLE` | 应用标题 | `博客论坛` |
| `VITE_APP_VERSION` | 应用版本 | `1.0.0` |

## 性能优化

### 1. 代码分割
项目已配置自动代码分割，无需额外配置。

### 2. 资源压缩
```bash
# 安装压缩插件
npm install --save-dev vite-plugin-compression

# 在vite.config.js中配置
import { compression } from 'vite-plugin-compression'

export default {
  plugins: [
    compression()
  ]
}
```

### 3. CDN配置
在 `index.html` 中使用CDN资源：

```html
<!-- 使用CDN加载Vue等库 -->
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
```

## 监控和分析

### 1. 构建分析
```bash
# 分析构建包大小
npm run build -- --report

# 或使用bundle-analyzer
npm install --save-dev rollup-plugin-visualizer
```

### 2. 性能监控
可以集成Google Analytics或其他分析工具。

## 故障排除

### 常见问题

1. **路由404问题**
   - 确保服务器配置了history模式支持
   - 检查nginx配置中的 `try_files` 指令

2. **API请求失败**
   - 检查 `VITE_API_BASE_URL` 配置
   - 确认后端服务正常运行
   - 检查CORS配置

3. **静态资源加载失败**
   - 检查资源路径配置
   - 确认服务器静态文件权限

4. **构建失败**
   ```bash
   # 清理缓存
   rm -rf node_modules package-lock.json
   npm install
   
   # 或
   yarn cache clean
   yarn install
   ```

## 更新部署

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 安装新依赖
npm install

# 3. 重新构建
npm run build

# 4. 更新服务器文件
rsync -av dist/ user@server:/var/www/html/

# 5. 重启服务（如果使用PM2）
pm2 restart blog-frontend
```

## 安全配置

### 1. HTTPS配置
```bash
# 使用Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

### 2. 安全头配置
在nginx中添加：

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

部署完成后，访问你的域名即可使用前端应用！
