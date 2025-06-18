#!/usr/bin/env python3
"""
部署环境检查脚本
用于验证Linux服务器环境是否满足部署要求
"""

import sys
import subprocess
import os
import platform
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - 版本符合要求")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - 需要Python 3.8+")
        return False

def check_pip():
    """检查pip是否可用"""
    print("\n📦 检查pip...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pip可用: {result.stdout.strip()}")
            return True
        else:
            print("❌ pip不可用")
            return False
    except Exception as e:
        print(f"❌ pip检查失败: {e}")
        return False

def check_requirements():
    """检查requirements.txt文件"""
    print("\n📋 检查requirements.txt...")
    # 检查当前目录和上级目录
    req_file = Path("requirements.txt")
    if not req_file.exists():
        req_file = Path("backend/requirements.txt")
    if not req_file.exists():
        req_file = Path("../requirements.txt")

    if req_file.exists():
        print("✅ requirements.txt文件存在")
        
        # 读取并验证文件内容
        with open(req_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        packages = [line.strip() for line in lines 
                   if line.strip() and not line.strip().startswith('#')]
        
        print(f"✅ 找到 {len(packages)} 个依赖包")
        
        # 检查是否有版本号
        has_versions = any('==' in pkg or '>=' in pkg or '<=' in pkg for pkg in packages)
        if not has_versions:
            print("✅ 无版本号限制，适合Linux部署")
        else:
            print("⚠️  包含版本号限制，可能在某些环境中出现兼容性问题")
        
        return True
    else:
        print("❌ requirements.txt文件不存在")
        return False

def check_system_info():
    """检查系统信息"""
    print("\n💻 系统信息...")
    print(f"✅ 操作系统: {platform.system()} {platform.release()}")
    print(f"✅ 架构: {platform.machine()}")
    print(f"✅ Python路径: {sys.executable}")

def check_network():
    """检查网络连接"""
    print("\n🌐 检查网络连接...")
    try:
        import urllib.request
        urllib.request.urlopen('https://pypi.org', timeout=5)
        print("✅ 网络连接正常，可以访问PyPI")
        return True
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
        return False

def check_ports():
    """检查端口可用性"""
    print("\n🔌 检查端口...")
    import socket
    
    def check_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            sock.close()
            return True
        except OSError:
            return False
    
    ports_to_check = [8000, 8001, 8002]
    available_ports = []
    
    for port in ports_to_check:
        if check_port(port):
            available_ports.append(port)
    
    if available_ports:
        print(f"✅ 可用端口: {', '.join(map(str, available_ports))}")
        return True
    else:
        print("❌ 常用端口都被占用")
        return False

def check_permissions():
    """检查文件权限"""
    print("\n🔐 检查权限...")
    current_dir = Path.cwd()
    
    if os.access(current_dir, os.R_OK | os.W_OK):
        print("✅ 当前目录可读写")
        return True
    else:
        print("❌ 当前目录权限不足")
        return False

def simulate_install():
    """模拟安装依赖"""
    print("\n🧪 模拟依赖安装...")
    try:
        # 只检查几个核心包是否可以找到
        core_packages = ['fastapi', 'uvicorn', 'pydantic']
        
        for package in core_packages:
            result = subprocess.run([sys.executable, '-m', 'pip', 'show', package], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {package} - 已安装")
            else:
                print(f"○ {package} - 未安装但可通过pip安装")
        
        return True
    except Exception as e:
        print(f"❌ 依赖检查失败: {e}")
        return False

def main():
    """主检查函数"""
    print("🚀 博客论坛系统 - Linux部署环境检查")
    print("=" * 50)
    
    checks = [
        ("Python版本", check_python_version),
        ("pip工具", check_pip),
        ("requirements文件", check_requirements),
        ("系统信息", check_system_info),
        ("网络连接", check_network),
        ("端口可用性", check_ports),
        ("文件权限", check_permissions),
        ("依赖包", simulate_install),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name}检查出错: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 检查结果: {passed}/{total} 项通过")
    
    if passed == total:
        print("🎉 环境检查全部通过！可以开始部署。")
        print("\n📝 下一步:")
        print("1. pip install -r requirements.txt")
        print("2. python main.py")
        print("3. 访问 http://localhost:8000")
    elif passed >= total - 2:
        print("⚠️  大部分检查通过，可以尝试部署。")
        print("请注意解决失败的检查项。")
    else:
        print("❌ 环境不满足部署要求，请解决问题后重试。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
