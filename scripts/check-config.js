#!/usr/bin/env node

/**
 * 配置检查脚本
 * 验证项目配置的完整性和正确性
 */

const fs = require('fs')
const path = require('path')

// 项目根目录
const ROOT_DIR = path.join(__dirname, '..')
const FRONTEND_DIR = path.join(ROOT_DIR, 'frontend')
const BACKEND_DIR = path.join(ROOT_DIR, 'backend')

// 必需的文件列表
const REQUIRED_FILES = [
  // 前端文件
  { path: 'frontend/package.json', type: 'json', required: true },
  { path: 'frontend/vite.config.js', type: 'js', required: true },
  { path: 'frontend/src/config/index.js', type: 'js', required: true },
  { path: 'frontend/.env.example', type: 'env', required: true },
  
  // 后端文件
  { path: 'backend/main.py', type: 'python', required: true },
  { path: 'backend/requirements.txt', type: 'text', required: true },
  
  // 脚本文件
  { path: 'scripts/detect-port.js', type: 'js', required: true },
  { path: 'scripts/start-dev.js', type: 'js', required: true },
  { path: 'package.json', type: 'json', required: true }
]

// 环境变量检查
const ENV_VARS = [
  { name: 'VITE_API_BASE_URL', required: true, pattern: /^https?:\/\/.*/ },
  { name: 'VITE_APP_TITLE', required: false },
  { name: 'VITE_APP_VERSION', required: false }
]

/**
 * 检查文件是否存在
 */
function checkFiles() {
  console.log('📁 检查必需文件...')
  
  let allExists = true
  
  for (const file of REQUIRED_FILES) {
    const fullPath = path.join(ROOT_DIR, file.path)
    const exists = fs.existsSync(fullPath)
    
    if (exists) {
      console.log(`✅ ${file.path}`)
    } else {
      console.log(`❌ ${file.path} - 文件不存在`)
      if (file.required) {
        allExists = false
      }
    }
  }
  
  return allExists
}

/**
 * 检查JSON文件格式
 */
function checkJsonFiles() {
  console.log('\n📋 检查JSON文件格式...')
  
  const jsonFiles = REQUIRED_FILES.filter(f => f.type === 'json')
  let allValid = true
  
  for (const file of jsonFiles) {
    const fullPath = path.join(ROOT_DIR, file.path)
    
    if (!fs.existsSync(fullPath)) continue
    
    try {
      const content = fs.readFileSync(fullPath, 'utf8')
      JSON.parse(content)
      console.log(`✅ ${file.path} - JSON格式正确`)
    } catch (error) {
      console.log(`❌ ${file.path} - JSON格式错误: ${error.message}`)
      allValid = false
    }
  }
  
  return allValid
}

/**
 * 检查环境变量配置
 */
function checkEnvConfig() {
  console.log('\n🔧 检查环境变量配置...')
  
  const envFiles = [
    path.join(FRONTEND_DIR, '.env.development'),
    path.join(FRONTEND_DIR, '.env.local'),
    path.join(FRONTEND_DIR, '.env.example')
  ]
  
  let hasValidEnv = false
  
  for (const envFile of envFiles) {
    if (fs.existsSync(envFile)) {
      console.log(`✅ 找到环境文件: ${path.basename(envFile)}`)
      
      try {
        const content = fs.readFileSync(envFile, 'utf8')
        const lines = content.split('\n')
        
        for (const envVar of ENV_VARS) {
          const found = lines.some(line => line.startsWith(`${envVar.name}=`))
          
          if (found) {
            console.log(`   ✅ ${envVar.name}`)
          } else if (envVar.required) {
            console.log(`   ❌ ${envVar.name} - 必需变量缺失`)
          } else {
            console.log(`   ⚠️  ${envVar.name} - 可选变量缺失`)
          }
        }
        
        hasValidEnv = true
      } catch (error) {
        console.log(`❌ 读取环境文件失败: ${error.message}`)
      }
    }
  }
  
  if (!hasValidEnv) {
    console.log('❌ 未找到有效的环境配置文件')
    console.log('💡 请复制 .env.example 为 .env.development')
  }
  
  return hasValidEnv
}

/**
 * 检查端口配置
 */
function checkPortConfig() {
  console.log('\n🔌 检查端口配置...')
  
  const configFiles = [
    { path: path.join(FRONTEND_DIR, 'vite.config.js'), type: 'vite' },
    { path: path.join(FRONTEND_DIR, 'src/config/index.js'), type: 'app' }
  ]
  
  let allValid = true
  
  for (const config of configFiles) {
    if (!fs.existsSync(config.path)) {
      console.log(`❌ ${path.basename(config.path)} - 文件不存在`)
      allValid = false
      continue
    }
    
    try {
      const content = fs.readFileSync(config.path, 'utf8')
      
      if (config.type === 'vite') {
        // 检查 vite.config.js 中的代理配置
        if (content.includes('proxy') && content.includes('target')) {
          console.log(`✅ ${path.basename(config.path)} - 代理配置存在`)
        } else {
          console.log(`⚠️  ${path.basename(config.path)} - 代理配置可能缺失`)
        }
      } else if (config.type === 'app') {
        // 检查应用配置
        if (content.includes('API_BASE_URL')) {
          console.log(`✅ ${path.basename(config.path)} - API配置存在`)
        } else {
          console.log(`❌ ${path.basename(config.path)} - API配置缺失`)
          allValid = false
        }
      }
    } catch (error) {
      console.log(`❌ 读取配置文件失败: ${error.message}`)
      allValid = false
    }
  }
  
  return allValid
}

/**
 * 检查依赖安装
 */
function checkDependencies() {
  console.log('\n📦 检查依赖安装...')
  
  // 检查前端依赖
  const frontendNodeModules = path.join(FRONTEND_DIR, 'node_modules')
  if (fs.existsSync(frontendNodeModules)) {
    console.log('✅ 前端依赖已安装')
  } else {
    console.log('❌ 前端依赖未安装')
    console.log('💡 运行: cd frontend && npm install')
  }
  
  // 检查后端依赖（简单检查）
  const backendVenv = path.join(BACKEND_DIR, 'venv')
  if (fs.existsSync(backendVenv)) {
    console.log('✅ 后端虚拟环境存在')
  } else {
    console.log('⚠️  后端虚拟环境不存在')
    console.log('💡 运行: cd backend && python -m venv venv')
  }
}

/**
 * 生成配置报告
 */
function generateReport(results) {
  const report = {
    timestamp: new Date().toISOString(),
    results: results,
    recommendations: []
  }
  
  // 添加建议
  if (!results.files) {
    report.recommendations.push('请确保所有必需文件存在')
  }
  
  if (!results.env) {
    report.recommendations.push('请配置环境变量文件')
  }
  
  if (!results.ports) {
    report.recommendations.push('请检查端口配置')
  }
  
  const reportPath = path.join(ROOT_DIR, 'config-check-report.json')
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2))
  console.log(`\n📊 配置检查报告已保存: ${reportPath}`)
}

/**
 * 主函数
 */
function main() {
  console.log('🔍 博客论坛系统配置检查')
  console.log('=' * 50)
  
  const results = {
    files: checkFiles(),
    json: checkJsonFiles(),
    env: checkEnvConfig(),
    ports: checkPortConfig()
  }
  
  checkDependencies()
  
  console.log('\n📊 检查结果汇总:')
  console.log('=' * 30)
  console.log(`文件检查: ${results.files ? '✅ 通过' : '❌ 失败'}`)
  console.log(`JSON格式: ${results.json ? '✅ 通过' : '❌ 失败'}`)
  console.log(`环境配置: ${results.env ? '✅ 通过' : '❌ 失败'}`)
  console.log(`端口配置: ${results.ports ? '✅ 通过' : '❌ 失败'}`)
  
  const allPassed = Object.values(results).every(Boolean)
  
  if (allPassed) {
    console.log('\n🎉 所有检查通过！系统配置正确。')
  } else {
    console.log('\n⚠️  发现配置问题，请根据上述提示进行修复。')
  }
  
  generateReport(results)
  
  return allPassed
}

// 如果直接运行此脚本
if (require.main === module) {
  const success = main()
  process.exit(success ? 0 : 1)
}

module.exports = {
  checkFiles,
  checkJsonFiles,
  checkEnvConfig,
  checkPortConfig
}
