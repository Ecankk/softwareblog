# 博客论坛系统 - Linux服务器部署指南

## 系统要求

- **操作系统**: Linux (Ubuntu 20.04+ / CentOS 7+ / Debian 10+)
- **Python版本**: Python 3.8+
- **内存**: 最少 1GB RAM (推荐 2GB+)
- **存储**: 最少 10GB 可用空间
- **网络**: 开放端口 8000 (或自定义端口)

## 快速部署步骤

### 1. 环境准备

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y  # Ubuntu/Debian
# 或
sudo yum update -y  # CentOS

# 安装Python和pip
sudo apt install python3 python3-pip python3-venv -y  # Ubuntu/Debian
# 或
sudo yum install python3 python3-pip -y  # CentOS

# 安装Git
sudo apt install git -y  # Ubuntu/Debian
# 或
sudo yum install git -y  # CentOS
```

### 2. 克隆项目

```bash
# 克隆项目到服务器
git clone <your-repository-url>
cd softwareblog/backend
```

### 3. 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

### 4. 安装依赖

```bash
# 安装Python依赖
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. 配置环境变量

```bash
# 创建环境配置文件
cp .env.example .env  # 如果有示例文件
# 或直接创建
nano .env
```

在 `.env` 文件中配置：
```env
# 服务器配置
HOST=0.0.0.0
PORT=8000

# 安全配置
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key

# 数据库配置（如果使用）
DATABASE_URL=sqlite:///./blog.db

# 文件上传配置
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB

# CORS配置
ALLOWED_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

### 6. 初始化数据

```bash
# 如果有初始化脚本
python init_db.py

# 或手动创建必要的目录
mkdir -p uploads/avatars uploads/covers
```

### 7. 启动服务

#### 开发模式
```bash
# 直接启动（开发用）
python main.py
# 或
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 生产模式
```bash
# 使用Gunicorn（推荐生产环境）
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 或使用uvicorn（简单部署）
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 8. 设置系统服务（可选）

创建systemd服务文件：
```bash
sudo nano /etc/systemd/system/blog-backend.service
```

服务文件内容：
```ini
[Unit]
Description=Blog Forum Backend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/softwareblog/backend
Environment=PATH=/path/to/your/softwareblog/backend/venv/bin
ExecStart=/path/to/your/softwareblog/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable blog-backend
sudo systemctl start blog-backend
sudo systemctl status blog-backend
```

## 反向代理配置（Nginx）

### 安装Nginx
```bash
sudo apt install nginx -y  # Ubuntu/Debian
# 或
sudo yum install nginx -y  # CentOS
```

### 配置Nginx
```bash
sudo nano /etc/nginx/sites-available/blog-backend
```

配置内容：
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件服务
    location /uploads/ {
        alias /path/to/your/softwareblog/backend/uploads/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/blog-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL证书配置（Let's Encrypt）

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取SSL证书
sudo certbot --nginx -d yourdomain.com

# 自动续期
sudo crontab -e
# 添加以下行：
0 12 * * * /usr/bin/certbot renew --quiet
```

## 监控和日志

### 查看应用日志
```bash
# 如果使用systemd服务
sudo journalctl -u blog-backend -f

# 如果直接运行
tail -f /path/to/logfile
```

### 性能监控
```bash
# 安装htop监控系统资源
sudo apt install htop -y

# 监控进程
htop
ps aux | grep uvicorn
```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   sudo lsof -i :8000
   sudo kill -9 <PID>
   ```

2. **权限问题**
   ```bash
   sudo chown -R www-data:www-data /path/to/project
   sudo chmod -R 755 /path/to/project
   ```

3. **依赖安装失败**
   ```bash
   # 更新pip
   pip install --upgrade pip
   
   # 清理缓存
   pip cache purge
   
   # 重新安装
   pip install -r requirements.txt --force-reinstall
   ```

4. **数据库连接问题**
   - 检查数据库文件权限
   - 确认数据库路径正确
   - 检查环境变量配置

## 安全建议

1. **防火墙配置**
   ```bash
   sudo ufw enable
   sudo ufw allow ssh
   sudo ufw allow 80
   sudo ufw allow 443
   ```

2. **定期更新**
   ```bash
   # 更新系统
   sudo apt update && sudo apt upgrade -y
   
   # 更新Python依赖
   pip list --outdated
   pip install --upgrade package-name
   ```

3. **备份数据**
   ```bash
   # 备份数据库
   cp db.json db.json.backup.$(date +%Y%m%d)
   
   # 备份上传文件
   tar -czf uploads.backup.$(date +%Y%m%d).tar.gz uploads/
   ```

## 扩展配置

### 使用Docker部署
如果需要使用Docker，可以创建Dockerfile：

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 负载均衡
如果需要多实例部署，可以配置Nginx负载均衡：

```nginx
upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

## 联系支持

如果在部署过程中遇到问题，请检查：
1. 系统日志
2. 应用日志
3. 网络连接
4. 权限设置

部署完成后，访问 `http://yourdomain.com` 即可使用博客论坛系统！
