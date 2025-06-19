/**
 * 应用配置管理
 * 统一管理所有配置项，防止硬编码
 */

// 开发环境配置
const development = {
  API_BASE_URL: 'http://localhost:9000',
  WS_BASE_URL: 'ws://localhost:9000',
  APP_NAME: '博客论坛',
  APP_VERSION: '1.0.0',
  DEBUG: true,
  LOG_LEVEL: 'debug'
}

// 生产环境配置
const production = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || '/api',
  WS_BASE_URL: import.meta.env.VITE_WS_BASE_URL || '/api',
  APP_NAME: '博客论坛',
  APP_VERSION: '1.0.0',
  DEBUG: false,
  LOG_LEVEL: 'error'
}

// 测试环境配置
const test = {
  API_BASE_URL: 'http://localhost:8888',
  WS_BASE_URL: 'ws://localhost:8888',
  APP_NAME: '博客论坛-测试',
  APP_VERSION: '1.0.0-test',
  DEBUG: true,
  LOG_LEVEL: 'info'
}

// 根据环境变量选择配置
const getConfig = () => {
  const env = import.meta.env.MODE || 'development'

  switch (env) {
    case 'production':
      return production
    case 'test':
      return test
    case 'development':
    default:
      return development
  }
}

// 导出配置
export const config = getConfig()

// 导出常用配置项
export const {
  API_BASE_URL,
  WS_BASE_URL,
  APP_NAME,
  APP_VERSION,
  DEBUG,
  LOG_LEVEL
} = config

// 端口检测和自动配置
export const detectApiPort = async () => {
  const commonPorts = [9000, 8000, 8001, 8080, 3000]

  for (const port of commonPorts) {
    try {
      const testUrl = `http://localhost:${port}/health`
      const response = await fetch(testUrl, {
        method: 'GET',
        timeout: 2000
      })

      if (response.ok) {
        console.log(`✅ 检测到API服务运行在端口 ${port}`)
        return `http://localhost:${port}`
      }
    } catch (error) {
      // 端口不可用，继续检测下一个
      continue
    }
  }

  console.warn('⚠️ 未检测到可用的API服务，使用默认配置')
  return API_BASE_URL
}

// 配置验证
export const validateConfig = () => {
  const requiredFields = ['API_BASE_URL', 'APP_NAME']
  const missing = requiredFields.filter(field => !config[field])

  if (missing.length > 0) {
    throw new Error(`配置缺失: ${missing.join(', ')}`)
  }

  console.log('✅ 配置验证通过')
  return true
}

// 动态配置更新
export const updateApiBaseUrl = (newUrl) => {
  config.API_BASE_URL = newUrl
  console.log(`🔄 API基础URL已更新为: ${newUrl}`)
}

// 获取完整的API URL
export const getApiUrl = (endpoint = '') => {
  const baseUrl = config.API_BASE_URL.replace(/\/$/, '')
  const cleanEndpoint = endpoint.replace(/^\//, '')
  return cleanEndpoint ? `${baseUrl}/${cleanEndpoint}` : baseUrl
}

// 获取WebSocket URL
export const getWsUrl = (endpoint = '') => {
  const baseUrl = config.WS_BASE_URL.replace(/\/$/, '')
  const cleanEndpoint = endpoint.replace(/^\//, '')
  return cleanEndpoint ? `${baseUrl}/${cleanEndpoint}` : baseUrl
}

// 开发环境辅助函数
export const isDevelopment = () => config.DEBUG
export const isProduction = () => !config.DEBUG

// 日志函数
export const log = {
  debug: (...args) => {
    if (config.LOG_LEVEL === 'debug') {
      console.log('[DEBUG]', ...args)
    }
  },
  info: (...args) => {
    if (['debug', 'info'].includes(config.LOG_LEVEL)) {
      console.info('[INFO]', ...args)
    }
  },
  warn: (...args) => {
    if (['debug', 'info', 'warn'].includes(config.LOG_LEVEL)) {
      console.warn('[WARN]', ...args)
    }
  },
  error: (...args) => {
    console.error('[ERROR]', ...args)
  }
}

export default config
