#!/usr/bin/env python3
"""
博客论坛系统全面功能测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3001"

class BlogTester:
    def __init__(self):
        self.session = requests.Session()
        self.tokens = {}
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        status = "✅ PASS" if success else "❌ FAIL"
        self.test_results.append((test_name, success, message))
        print(f"{status} {test_name}: {message}")
        
    def test_user_registration(self):
        """测试用户注册"""
        print("\n🔐 测试用户认证系统...")
        
        # 测试注册新用户
        test_user = {
            "email": f"testuser_{int(time.time())}@test.com",
            "password": "testpass123"
        }
        
        response = self.session.post(f"{BASE_URL}/auth/register", json=test_user)
        success = response.status_code == 200
        self.log_test("用户注册", success, f"状态码: {response.status_code}")
        
        if success:
            self.test_user = test_user
            return True
        return False
    
    def test_user_login(self):
        """测试用户登录"""
        # 测试管理员登录
        admin_creds = {"email": "admin@blog.com", "password": "123456"}
        response = self.session.post(f"{BASE_URL}/auth/login", json=admin_creds)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            self.tokens['admin'] = data.get('access_token')
            self.log_test("管理员登录", True, "获取到token")
        else:
            self.log_test("管理员登录", False, f"状态码: {response.status_code}")
            
        # 测试普通用户登录
        user_creds = {"email": "test@example.com", "password": "123456"}
        response = self.session.post(f"{BASE_URL}/auth/login", json=user_creds)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            self.tokens['user'] = data.get('access_token')
            self.log_test("普通用户登录", True, "获取到token")
        else:
            self.log_test("普通用户登录", False, f"状态码: {response.status_code}")
            
        return len(self.tokens) > 0
    
    def test_posts_api(self):
        """测试文章相关API"""
        print("\n📝 测试文章系统...")
        
        # 获取文章列表
        response = self.session.get(f"{BASE_URL}/posts")
        success = response.status_code == 200
        self.log_test("获取文章列表", success, f"状态码: {response.status_code}")
        
        if success:
            posts_data = response.json()
            posts = posts_data.get('items', [])
            self.log_test("文章列表内容", len(posts) > 0, f"找到 {len(posts)} 篇文章")
            
            # 测试获取单篇文章
            if posts:
                first_post = posts[0]
                response = self.session.get(f"{BASE_URL}/posts/{first_post['slug']}")
                success = response.status_code == 200
                self.log_test("获取文章详情", success, f"文章: {first_post['title']}")
        
        # 测试创建文章（需要登录）
        if 'user' in self.tokens:
            headers = {"Authorization": f"Bearer {self.tokens['user']}"}
            new_post = {
                "title": f"测试文章 {int(time.time())}",
                "content": "# 测试内容\n\n这是一篇测试文章。",
                "summary": "测试文章摘要",
                "tags": ["测试", "API"],
                "slug": f"test-post-{int(time.time())}"
            }
            
            response = self.session.post(f"{BASE_URL}/posts", json=new_post, headers=headers)
            success = response.status_code == 200
            self.log_test("创建文章", success, f"状态码: {response.status_code}")
            
            if success:
                self.test_post = response.json()
    
    def test_comments_api(self):
        """测试评论系统"""
        print("\n💬 测试评论系统...")
        
        # 获取文章评论
        response = self.session.get(f"{BASE_URL}/posts/1/comments")
        success = response.status_code == 200
        self.log_test("获取文章评论", success, f"状态码: {response.status_code}")
        
        # 测试创建评论（需要登录）
        if 'user' in self.tokens:
            headers = {"Authorization": f"Bearer {self.tokens['user']}"}
            new_comment = {
                "content": f"这是一条测试评论 {int(time.time())}",
                "parentId": None
            }
            
            response = self.session.post(f"{BASE_URL}/posts/1/comments", json=new_comment, headers=headers)
            success = response.status_code == 200
            self.log_test("创建评论", success, f"状态码: {response.status_code}")
    
    def test_user_interactions(self):
        """测试用户交互功能"""
        print("\n👍 测试用户交互...")
        
        if 'user' not in self.tokens:
            self.log_test("用户交互测试", False, "需要用户登录")
            return
            
        headers = {"Authorization": f"Bearer {self.tokens['user']}"}
        
        # 测试点赞文章
        response = self.session.post(f"{BASE_URL}/posts/1/like", headers=headers)
        success = response.status_code in [200, 400]  # 400可能是已经点赞过了
        self.log_test("点赞文章", success, f"状态码: {response.status_code}")
        
        # 测试收藏文章
        response = self.session.post(f"{BASE_URL}/posts/1/bookmark", headers=headers)
        success = response.status_code in [200, 400]  # 400可能是已经收藏过了
        self.log_test("收藏文章", success, f"状态码: {response.status_code}")
    
    def test_search_api(self):
        """测试搜索功能"""
        print("\n🔍 测试搜索功能...")
        
        # 测试文章搜索
        response = self.session.get(f"{BASE_URL}/search", params={"q": "Vue"})
        success = response.status_code == 200
        self.log_test("搜索功能", success, f"状态码: {response.status_code}")
        
        if success:
            results = response.json()
            self.log_test("搜索结果", len(results) > 0, f"找到 {len(results)} 个结果")
    
    def test_admin_api(self):
        """测试管理员功能"""
        print("\n🛠️ 测试管理员功能...")
        
        if 'admin' not in self.tokens:
            self.log_test("管理员功能测试", False, "需要管理员登录")
            return
            
        headers = {"Authorization": f"Bearer {self.tokens['admin']}"}
        
        # 测试获取系统统计
        response = self.session.get(f"{BASE_URL}/admin/stats", headers=headers)
        success = response.status_code == 200
        self.log_test("系统统计", success, f"状态码: {response.status_code}")
        
        # 测试获取用户列表
        response = self.session.get(f"{BASE_URL}/admin/users", headers=headers)
        success = response.status_code == 200
        self.log_test("用户管理", success, f"状态码: {response.status_code}")
    
    def test_frontend_accessibility(self):
        """测试前端页面可访问性"""
        print("\n🌐 测试前端页面...")
        
        pages = [
            ("首页", "/"),
            ("登录页", "/login"),
            ("注册页", "/register"),
            ("文章详情", "/post/vue3-composition-api-guide"),
            ("搜索页", "/search"),
            ("帮助页", "/help")
        ]
        
        for page_name, path in pages:
            try:
                response = requests.get(f"{FRONTEND_URL}{path}", timeout=5)
                success = response.status_code == 200
                self.log_test(f"前端-{page_name}", success, f"状态码: {response.status_code}")
            except Exception as e:
                self.log_test(f"前端-{page_name}", False, f"连接错误: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始全面功能测试...")
        print("=" * 50)
        
        # 运行所有测试
        self.test_user_login()
        self.test_posts_api()
        self.test_comments_api()
        self.test_user_interactions()
        self.test_search_api()
        self.test_admin_api()
        self.test_frontend_accessibility()
        
        # 统计结果
        print("\n" + "=" * 50)
        print("📊 测试结果统计:")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for _, success, _ in self.test_results if success)
        failed_tests = total_tests - passed_tests
        
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ✅")
        print(f"失败: {failed_tests} ❌")
        print(f"成功率: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 失败的测试:")
            for test_name, success, message in self.test_results:
                if not success:
                    print(f"   - {test_name}: {message}")
        
        print("\n🎉 测试完成!")
        return passed_tests, failed_tests

if __name__ == "__main__":
    tester = BlogTester()
    tester.run_all_tests()
