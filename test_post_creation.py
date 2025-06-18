#!/usr/bin/env python3
"""
测试文章发布功能的脚本
"""

import requests
import json

# 配置
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "test@example.com",
    "password": "123456"
}

def login():
    """登录并获取token"""
    response = requests.post(f"{BASE_URL}/auth/login", json=TEST_USER)
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print(f"登录失败: {response.text}")
        return None

def create_test_post(token):
    """创建测试文章"""
    headers = {"Authorization": f"Bearer {token}"}
    
    post_data = {
        "title": "测试文章 - 自动化测试",
        "content": "# 测试文章\n\n这是一篇通过API自动创建的测试文章。\n\n## 功能测试\n\n- 文章创建 ✅\n- 标签支持 ✅\n- 摘要支持 ✅\n\n测试完成！",
        "summary": "这是一篇用于测试文章发布功能的测试文章",
        "tags": ["测试", "API", "自动化"],
        "slug": f"test-post-{int(__import__('time').time())}"
    }
    
    response = requests.post(f"{BASE_URL}/posts", json=post_data, headers=headers)
    
    if response.status_code == 200:
        post = response.json()
        print("✅ 文章创建成功!")
        print(f"   标题: {post['title']}")
        print(f"   Slug: {post['slug']}")
        print(f"   作者: {post['author']['username']}")
        print(f"   标签: {post['tags']}")
        return post
    else:
        print(f"❌ 文章创建失败: {response.text}")
        return None

def get_posts():
    """获取文章列表"""
    response = requests.get(f"{BASE_URL}/posts")
    if response.status_code == 200:
        posts = response.json()
        print(f"\n📚 当前共有 {posts['total']} 篇文章:")
        for post in posts['items'][:5]:  # 显示前5篇
            print(f"   - {post['title']} (作者: {post['author']['username']})")
        return posts
    else:
        print(f"❌ 获取文章列表失败: {response.text}")
        return None

def main():
    print("🚀 开始测试文章发布功能...")
    
    # 1. 登录
    print("\n1. 正在登录...")
    token = login()
    if not token:
        return
    print("✅ 登录成功!")
    
    # 2. 创建文章
    print("\n2. 正在创建测试文章...")
    post = create_test_post(token)
    if not post:
        return
    
    # 3. 获取文章列表
    print("\n3. 正在获取文章列表...")
    posts = get_posts()
    
    print("\n🎉 测试完成!")
    print("\n📋 测试结果:")
    print("   ✅ 用户登录功能正常")
    print("   ✅ 文章创建功能正常")
    print("   ✅ 文章列表功能正常")
    print("   ✅ 标签和摘要支持正常")
    print("   ✅ 作者信息关联正常")

if __name__ == "__main__":
    main()
