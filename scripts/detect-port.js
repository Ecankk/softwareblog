#!/usr/bin/env node

/**
 * 端口检测脚本
 * 自动检测可用的API端口并更新配置
 */

const fs = require('fs')
const path = require('path')
const http = require('http')

// 常用端口列表
const COMMON_PORTS = [9000, 8000, 8001, 8080, 3001, 5000]

// 配置文件路径
const ENV_FILES = [
  path.join(__dirname, '../frontend/.env.development'),
  path.join(__dirname, '../frontend/.env.local'),
  path.join(__dirname, '../frontend/vite.config.js')
]

/**
 * 检测端口是否可用
 */
function checkPort(port) {
  return new Promise((resolve) => {
    const req = http.request({
      hostname: 'localhost',
      port: port,
      path: '/health',
      method: 'GET',
      timeout: 2000
    }, (res) => {
      if (res.statusCode === 200) {
        resolve(true)
      } else {
        resolve(false)
      }
    })

    req.on('error', () => {
      resolve(false)
    })

    req.on('timeout', () => {
      req.destroy()
      resolve(false)
    })

    req.end()
  })
}

/**
 * 检测所有端口
 */
async function detectApiPort() {
  console.log('🔍 正在检测API服务端口...')
  
  for (const port of COMMON_PORTS) {
    console.log(`   检测端口 ${port}...`)
    
    const isAvailable = await checkPort(port)
    if (isAvailable) {
      console.log(`✅ 发现API服务运行在端口 ${port}`)
      return port
    }
  }
  
  console.log('❌ 未发现运行中的API服务')
  return null
}

/**
 * 更新环境变量文件
 */
function updateEnvFile(filePath, port) {
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  文件不存在: ${filePath}`)
    return false
  }

  try {
    let content = fs.readFileSync(filePath, 'utf8')
    const newUrl = `http://localhost:${port}`
    
    if (filePath.endsWith('.env.development') || filePath.endsWith('.env.local')) {
      // 更新 .env 文件
      const regex = /VITE_API_BASE_URL=.*/
      if (regex.test(content)) {
        content = content.replace(regex, `VITE_API_BASE_URL=${newUrl}`)
      } else {
        content += `\nVITE_API_BASE_URL=${newUrl}\n`
      }
    } else if (filePath.endsWith('vite.config.js')) {
      // 更新 vite.config.js 文件
      const regex = /target:\s*["']http:\/\/localhost:\d+["']/
      if (regex.test(content)) {
        content = content.replace(regex, `target: "${newUrl}"`)
      }
    }
    
    fs.writeFileSync(filePath, content, 'utf8')
    console.log(`✅ 已更新: ${filePath}`)
    return true
  } catch (error) {
    console.error(`❌ 更新失败 ${filePath}:`, error.message)
    return false
  }
}

/**
 * 更新前端配置文件
 */
function updateFrontendConfig(port) {
  console.log(`🔄 正在更新前端配置为端口 ${port}...`)
  
  let updateCount = 0
  
  for (const filePath of ENV_FILES) {
    if (updateEnvFile(filePath, port)) {
      updateCount++
    }
  }
  
  if (updateCount > 0) {
    console.log(`✅ 已更新 ${updateCount} 个配置文件`)
    console.log('💡 请重启前端开发服务器以应用新配置')
  } else {
    console.log('❌ 未能更新任何配置文件')
  }
}

/**
 * 生成配置报告
 */
function generateReport(detectedPort) {
  const report = {
    timestamp: new Date().toISOString(),
    detectedPort: detectedPort,
    checkedPorts: COMMON_PORTS,
    configFiles: ENV_FILES.map(file => ({
      path: file,
      exists: fs.existsSync(file)
    }))
  }
  
  const reportPath = path.join(__dirname, '../port-detection-report.json')
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2))
  console.log(`📊 检测报告已保存: ${reportPath}`)
}

/**
 * 主函数
 */
async function main() {
  console.log('🚀 端口检测脚本启动')
  console.log('=' * 50)
  
  try {
    const detectedPort = await detectApiPort()
    
    if (detectedPort) {
      updateFrontendConfig(detectedPort)
      console.log('\n🎉 端口检测和配置更新完成!')
      console.log(`📡 API服务地址: http://localhost:${detectedPort}`)
      console.log(`📋 健康检查: http://localhost:${detectedPort}/health`)
    } else {
      console.log('\n⚠️  未检测到运行中的API服务')
      console.log('请确保后端服务已启动，然后重新运行此脚本')
      console.log('\n启动后端服务的命令:')
      console.log('  cd backend')
      console.log('  python main.py')
    }
    
    generateReport(detectedPort)
    
  } catch (error) {
    console.error('❌ 端口检测失败:', error.message)
    process.exit(1)
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  main()
}

module.exports = {
  detectApiPort,
  updateFrontendConfig,
  checkPort
}
