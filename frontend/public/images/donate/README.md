# 打赏收款码图片目录

## 📁 目录说明
这个目录用于存放打赏功能的收款码图片。

## 📋 文件要求

### 主要收款码
- **文件名**: `alipay-qr.jpg` 或 `alipay-qr.png`
- **尺寸**: 建议 400x400 像素或更大
- **格式**: JPG 或 PNG
- **内容**: 支付宝收款码

### 可选收款码
- **微信收款码**: `wechat-qr.jpg` 或 `wechat-qr.png`
- **其他收款码**: 可以根据需要添加

## 🎯 使用方式

1. **准备收款码图片**
   - 打开支付宝，进入"收钱"功能
   - 保存收款码图片到本地
   - 重命名为 `alipay-qr.jpg`

2. **放置图片**
   ```
   frontend/public/images/donate/alipay-qr.jpg
   ```

3. **访问路径**
   - 图片将通过以下URL访问：
   - `http://localhost:3002/images/donate/alipay-qr.jpg`

## 🔧 自定义配置

### 多用户收款码
如果需要为不同用户设置不同的收款码，可以：

1. **按用户ID命名**
   ```
   alipay-qr-user1.jpg
   alipay-qr-user2.jpg
   ```

2. **修改组件代码**
   在 `DonateModal.vue` 中修改 `qrCodeUrl` 计算属性：
   ```javascript
   const qrCodeUrl = computed(() => {
     return `/images/donate/alipay-qr-user${props.authorId}.jpg`
   })
   ```

### 支持多种支付方式
可以添加多个收款码图片：
```
alipay-qr.jpg     # 支付宝
wechat-qr.jpg     # 微信
paypal-qr.jpg     # PayPal
```

## 📝 注意事项

1. **图片大小**: 建议控制在 500KB 以内
2. **图片质量**: 确保二维码清晰可扫描
3. **安全性**: 不要在代码仓库中提交真实的收款码
4. **备份**: 建议保留收款码的备份

## 🎨 推荐尺寸

- **最小尺寸**: 200x200 像素
- **推荐尺寸**: 400x400 像素
- **最大尺寸**: 800x800 像素

## 🔄 更新收款码

要更新收款码，只需：
1. 替换对应的图片文件
2. 保持文件名不变
3. 刷新页面即可看到新的收款码
