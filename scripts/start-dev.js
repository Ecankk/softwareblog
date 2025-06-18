#!/usr/bin/env node

/**
 * 开发环境启动脚本
 * 自动检测端口并启动前后端服务
 */

const { spawn } = require('child_process')
const path = require('path')
const fs = require('fs')
const { detectApiPort, checkPort } = require('./detect-port')

// 项目根目录
const ROOT_DIR = path.join(__dirname, '..')
const BACKEND_DIR = path.join(ROOT_DIR, 'backend')
const FRONTEND_DIR = path.join(ROOT_DIR, 'frontend')

// 端口配置
const BACKEND_PORTS = [9000, 8000, 8001, 8080]
const FRONTEND_PORT = 3002

/**
 * 检查目录是否存在
 */
function checkDirectories() {
  const dirs = [
    { name: 'backend', path: BACKEND_DIR },
    { name: 'frontend', path: FRONTEND_DIR }
  ]
  
  for (const dir of dirs) {
    if (!fs.existsSync(dir.path)) {
      console.error(`❌ ${dir.name} 目录不存在: ${dir.path}`)
      return false
    }
  }
  
  return true
}

/**
 * 查找可用端口
 */
async function findAvailablePort(ports) {
  for (const port of ports) {
    const isUsed = await checkPort(port)
    if (!isUsed) {
      return port
    }
  }
  return null
}

/**
 * 启动后端服务
 */
function startBackend(port) {
  return new Promise((resolve, reject) => {
    console.log(`🚀 启动后端服务 (端口 ${port})...`)
    
    const backend = spawn('python', ['main.py'], {
      cwd: BACKEND_DIR,
      stdio: 'pipe',
      env: {
        ...process.env,
        PORT: port.toString()
      }
    })
    
    let started = false
    
    backend.stdout.on('data', (data) => {
      const output = data.toString()
      console.log(`[后端] ${output.trim()}`)
      
      if (output.includes('Uvicorn running') && !started) {
        started = true
        console.log(`✅ 后端服务启动成功: http://localhost:${port}`)
        resolve(backend)
      }
    })
    
    backend.stderr.on('data', (data) => {
      const error = data.toString()
      console.error(`[后端错误] ${error.trim()}`)
      
      if (error.includes('Address already in use') || error.includes('端口被占用')) {
        reject(new Error(`端口 ${port} 被占用`))
      }
    })
    
    backend.on('error', (error) => {
      console.error(`❌ 后端启动失败:`, error.message)
      reject(error)
    })
    
    // 超时检查
    setTimeout(() => {
      if (!started) {
        reject(new Error('后端启动超时'))
      }
    }, 30000)
  })
}

/**
 * 启动前端服务
 */
function startFrontend() {
  return new Promise((resolve, reject) => {
    console.log(`🚀 启动前端服务 (端口 ${FRONTEND_PORT})...`)
    
    const frontend = spawn('npm', ['run', 'dev'], {
      cwd: FRONTEND_DIR,
      stdio: 'pipe'
    })
    
    let started = false
    
    frontend.stdout.on('data', (data) => {
      const output = data.toString()
      console.log(`[前端] ${output.trim()}`)
      
      if (output.includes('Local:') && !started) {
        started = true
        console.log(`✅ 前端服务启动成功: http://localhost:${FRONTEND_PORT}`)
        resolve(frontend)
      }
    })
    
    frontend.stderr.on('data', (data) => {
      const error = data.toString()
      console.error(`[前端错误] ${error.trim()}`)
    })
    
    frontend.on('error', (error) => {
      console.error(`❌ 前端启动失败:`, error.message)
      reject(error)
    })
    
    // 超时检查
    setTimeout(() => {
      if (!started) {
        reject(new Error('前端启动超时'))
      }
    }, 60000)
  })
}

/**
 * 优雅关闭
 */
function setupGracefulShutdown(processes) {
  const shutdown = () => {
    console.log('\n🛑 正在关闭服务...')
    
    processes.forEach((proc, index) => {
      if (proc && !proc.killed) {
        console.log(`   关闭进程 ${index + 1}...`)
        proc.kill('SIGTERM')
      }
    })
    
    setTimeout(() => {
      processes.forEach((proc) => {
        if (proc && !proc.killed) {
          proc.kill('SIGKILL')
        }
      })
      process.exit(0)
    }, 5000)
  }
  
  process.on('SIGINT', shutdown)
  process.on('SIGTERM', shutdown)
  process.on('exit', shutdown)
}

/**
 * 主函数
 */
async function main() {
  console.log('🚀 博客论坛开发环境启动脚本')
  console.log('=' * 50)
  
  try {
    // 检查目录
    if (!checkDirectories()) {
      process.exit(1)
    }
    
    // 检测现有API服务
    console.log('🔍 检测现有API服务...')
    const existingPort = await detectApiPort()
    
    let backendProcess = null
    let backendPort = null
    
    if (existingPort) {
      console.log(`✅ 发现运行中的API服务: http://localhost:${existingPort}`)
      backendPort = existingPort
    } else {
      // 查找可用端口
      console.log('🔍 查找可用端口...')
      backendPort = await findAvailablePort(BACKEND_PORTS)
      
      if (!backendPort) {
        console.error('❌ 没有可用的后端端口')
        process.exit(1)
      }
      
      // 启动后端
      backendProcess = await startBackend(backendPort)
    }
    
    // 更新前端配置
    console.log('🔄 更新前端配置...')
    const { updateFrontendConfig } = require('./detect-port')
    updateFrontendConfig(backendPort)
    
    // 启动前端
    const frontendProcess = await startFrontend()
    
    // 设置优雅关闭
    const processes = [backendProcess, frontendProcess].filter(Boolean)
    setupGracefulShutdown(processes)
    
    // 显示启动信息
    console.log('\n🎉 开发环境启动完成!')
    console.log('=' * 50)
    console.log(`📡 后端API: http://localhost:${backendPort}`)
    console.log(`📋 API文档: http://localhost:${backendPort}/docs`)
    console.log(`🌐 前端应用: http://localhost:${FRONTEND_PORT}`)
    console.log('\n💡 按 Ctrl+C 停止所有服务')
    
    // 保持进程运行
    await new Promise(() => {})
    
  } catch (error) {
    console.error('❌ 启动失败:', error.message)
    process.exit(1)
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  main()
}

module.exports = {
  startBackend,
  startFrontend,
  findAvailablePort
}
