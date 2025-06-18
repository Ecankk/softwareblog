import os, json, secrets
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import Response
from pydantic import BaseModel
import bcrypt as bcrypt_lib
from typing import Optional
from avatar_generator import get_user_avatar_svg

# —— 数据路径准备 ——
DB_PATH = "db.json"
UPLOAD_DIR = "uploads"
for sub in ("avatars", "covers"):
    os.makedirs(f"{UPLOAD_DIR}/{sub}", exist_ok=True)

# —— 认证配置 ——
security = HTTPBearer()
# 简单的token存储（生产环境应使用JWT）
active_tokens = {}

# —— 读写 JSON ——  
def read_db():
    with open(DB_PATH, encoding="utf-8") as f:
        return json.load(f)

def write_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# —— 认证辅助函数 ——
def generate_token():
    return secrets.token_urlsafe(32)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in active_tokens:
        raise HTTPException(401, "无效的token")
    user_id = active_tokens[token]
    db = read_db()
    for user in db["users"]:
        if user["id"] == user_id:
            return {
                "id": user["id"],
                "email": user["email"],
                "avatar": user["avatar"],
                "username": user.get("username", user["email"]),
                "bio": user.get("bio", ""),
                "role": user.get("role", "user")
            }
    raise HTTPException(401, "用户不存在")

def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(403, "需要管理员权限")
    return current_user

def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    """可选的用户认证，如果没有token也不会报错"""
    if not credentials:
        return None

    token = credentials.credentials
    if token not in active_tokens:
        return None

    user_id = active_tokens[token]
    db = read_db()
    for user in db["users"]:
        if user["id"] == user_id:
            return {
                "id": user["id"],
                "email": user["email"],
                "avatar": user["avatar"],
                "username": user.get("username", user["email"]),
                "bio": user.get("bio", ""),
                "role": user.get("role", "user")
            }
    return None

# —— 请求模型 ——  
class UserIn(BaseModel):
    email: str
    password: str


class PostIn(BaseModel):
    slug: str
    title: str
    content: str
    summary: Optional[str] = ""
    tags: Optional[list] = []

class CommentIn(BaseModel):
    content: str
    parentId: Optional[int] = None

class TagIn(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = "#666666"

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None

class NotificationIn(BaseModel):
    type: str
    title: str
    content: str
    relatedId: Optional[int] = None
    relatedType: Optional[str] = None

# —— 启动 FastAPI ——  
app = FastAPI()

# —— 添加 CORS 中间件 ——  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# —— 挂载静态资源 ——  
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# ✅ 用户注册 ——  
@app.post("/auth/register")
def register(user: UserIn):
    db = read_db()
    if any(u["email"] == user.email for u in db["users"]):
        raise HTTPException(400, "邮箱已存在")
    uid = max((u["id"] for u in db["users"]), default=0) + 1
    hashed = bcrypt_lib.hashpw(user.password.encode('utf-8'), bcrypt_lib.gensalt()).decode('utf-8')
    new_user = {"id": uid, "email": user.email, "password": hashed, "avatar": None}
    db["users"].append(new_user)
    write_db(db)
    return {"id": uid, "email": user.email}

# ✅ 用户登录 ——
@app.post("/auth/login")
def login(user: UserIn):
    db = read_db()
    for u in db["users"]:
        if u["email"] == user.email and bcrypt_lib.checkpw(user.password.encode('utf-8'), u["password"].encode('utf-8')):
            # 生成token
            token = generate_token()
            active_tokens[token] = u["id"]

            user_info = {"id": u["id"], "email": u["email"], "avatar": u["avatar"]}
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": user_info
            }
    raise HTTPException(401, "邮箱或密码错误")

# ✅ 获取当前用户信息 ——
@app.get("/auth/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user

# ✅ 更新用户资料 ——
@app.put("/auth/profile")
def update_profile(profile_data: UserProfileUpdate, current_user: dict = Depends(get_current_user)):
    db = read_db()

    for u in db["users"]:
        if u["id"] == current_user["id"]:
            # 更新用户信息
            if profile_data.username is not None:
                u["username"] = profile_data.username
            if profile_data.bio is not None:
                u["bio"] = profile_data.bio
            if profile_data.email is not None:
                # 检查邮箱是否已被其他用户使用
                if any(user["email"] == profile_data.email and user["id"] != current_user["id"] for user in db["users"]):
                    raise HTTPException(400, "邮箱已被使用")
                u["email"] = profile_data.email

            write_db(db)

            # 返回更新后的用户信息
            return {
                "id": u["id"],
                "email": u["email"],
                "username": u.get("username", u["email"]),
                "bio": u.get("bio", ""),
                "avatar": u["avatar"]
            }

    raise HTTPException(404, "用户不存在")

# ✅ 获取用户信息 ——
@app.get("/users/{user_id}")
def get_user(user_id: int):
    db = read_db()

    # 查找用户
    user = None
    for u in db["users"]:
        if u["id"] == user_id:
            user = u
            break

    if not user:
        raise HTTPException(404, "用户不存在")

    # 统计用户文章数
    post_count = len([p for p in db["posts"] if p["authorId"] == user_id])

    return {
        "id": user["id"],
        "email": user["email"],
        "username": user.get("username", user["email"]),
        "bio": user.get("bio", ""),
        "avatar": user["avatar"],
        "followers_count": user.get("followers_count", 0),
        "following_count": user.get("following_count", 0),
        "posts_count": post_count,
        "created_at": user.get("created_at")
    }

# ✅ 获取用户文章列表 ——
@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int, page: int = 1, limit: int = 10):
    db = read_db()

    # 检查用户是否存在
    user_exists = any(u["id"] == user_id for u in db["users"])
    if not user_exists:
        raise HTTPException(404, "用户不存在")

    # 获取用户的文章
    user_posts = [p for p in db["posts"] if p["authorId"] == user_id]

    # 按创建时间排序
    user_posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    # 分页
    start = (page - 1) * limit
    end = start + limit
    paginated_posts = user_posts[start:end]

    return {
        "items": paginated_posts,
        "has_more": end < len(user_posts),
        "total": len(user_posts),
        "page": page,
        "limit": limit
    }

# ✅ 上传用户头像 ——  
@app.post("/upload/avatar")
async def upload_avatar(user_id: int = Form(...), file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    path = f"{UPLOAD_DIR}/avatars/{user_id}{ext}"
    with open(path, "wb") as f:
        f.write(await file.read())
    db = read_db()
    for u in db["users"]:
        if u["id"] == user_id:
            u["avatar"] = path
            break
    write_db(db)
    return {"avatar": path}

# ✅ 创建文章 ——
@app.post("/posts")
def create_post(post: PostIn, current_user: dict = Depends(get_current_user)):
    db = read_db()
    if any(p["slug"] == post.slug for p in db["posts"]):
        raise HTTPException(400, "slug 已存在")
    pid = max((p["id"] for p in db["posts"]), default=0) + 1
    new_post = {
        "id": pid,
        "slug": post.slug,
        "title": post.title,
        "content": post.content,
        "summary": getattr(post, 'summary', ''),
        "cover": None,
        "authorId": current_user["id"],
        "likes_count": 0,
        "views_count": 0,
        "comments_count": 0,
        "bookmarks_count": 0,
        "tags": getattr(post, 'tags', []),
        "status": "published",
        "created_at": "2024-06-18T00:00:00Z",
        "updated_at": "2024-06-18T00:00:00Z"
    }
    db["posts"].append(new_post)
    write_db(db)

    # 返回包含作者信息的文章
    new_post["author"] = {
        "id": current_user["id"],
        "username": current_user.get("username", current_user["email"]),
        "email": current_user["email"],
        "avatar": current_user["avatar"]
    }

    return new_post

# ✅ 获取文章列表 ——
@app.get("/posts")
def list_posts(page: int = 1, limit: int = 10, sort: str = "created_at", tag: str = "", type: str = "latest", current_user: dict = Depends(get_current_user_optional)):
    db = read_db()
    posts = db["posts"].copy()

    # 标签筛选
    if tag:
        posts = [p for p in posts if tag in p.get("tags", [])]

    # 排序
    if sort == "created_at":
        posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    elif sort == "likes_count":
        posts.sort(key=lambda x: x.get("likes_count", 0), reverse=True)
    elif sort == "comments_count":
        posts.sort(key=lambda x: x.get("comments_count", 0), reverse=True)
    elif sort == "views_count":
        posts.sort(key=lambda x: x.get("views_count", 0), reverse=True)

    # 添加作者信息和用户交互状态
    for post in posts:
        # 添加作者信息
        for user in db["users"]:
            if user["id"] == post["authorId"]:
                post["author"] = {
                    "id": user["id"],
                    "username": user.get("username", user["email"]),
                    "email": user["email"],
                    "avatar": user["avatar"]
                }
                break

        # 添加用户交互状态（如果用户已登录）
        if current_user:
            # 检查是否点赞
            post["is_liked"] = any(
                like["userId"] == current_user["id"] and like["postId"] == post["id"]
                for like in db["likes"]
            )

            # 检查是否收藏
            post["is_bookmarked"] = any(
                bookmark["userId"] == current_user["id"] and bookmark["postId"] == post["id"]
                for bookmark in db["bookmarks"]
            )
        else:
            post["is_liked"] = False
            post["is_bookmarked"] = False

    # 分页
    start = (page - 1) * limit
    end = start + limit
    paginated_posts = posts[start:end]

    return {
        "items": paginated_posts,
        "has_more": end < len(posts),
        "total": len(posts),
        "page": page,
        "limit": limit
    }

# ✅ 获取文章详情 ——
@app.get("/posts/{slug}")
def get_post(slug: str, current_user: dict = Depends(get_current_user_optional)):
    db = read_db()
    for p in db["posts"]:
        if p["slug"] == slug:
            # 添加作者信息
            for user in db["users"]:
                if user["id"] == p["authorId"]:
                    p["author"] = {
                        "id": user["id"],
                        "username": user.get("username", user["email"]),
                        "email": user["email"],
                        "avatar": user["avatar"]
                    }
                    break

            # 添加用户交互状态（如果用户已登录）
            if current_user:
                # 检查是否点赞
                p["is_liked"] = any(
                    like["userId"] == current_user["id"] and like["postId"] == p["id"]
                    for like in db["likes"]
                )

                # 检查是否收藏
                p["is_bookmarked"] = any(
                    bookmark["userId"] == current_user["id"] and bookmark["postId"] == p["id"]
                    for bookmark in db["bookmarks"]
                )
            else:
                p["is_liked"] = False
                p["is_bookmarked"] = False

            return p
    raise HTTPException(404, "文章不存在")

# ✅ 上传文章封面 ——  
@app.post("/upload/cover")
async def upload_cover(slug: str = Form(...), file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    path = f"{UPLOAD_DIR}/covers/{slug}{ext}"
    with open(path, "wb") as f:
        f.write(await file.read())
    db = read_db()
    for p in db["posts"]:
        if p["slug"] == slug:
            p["cover"] = path
            break
    write_db(db)
    return {"cover": path}

# ✅ 文章搜索 ——  
@app.get("/posts/search")
def search_posts(q: str = ""):
    db = read_db()
    return [p for p in db["posts"] if q.lower() in p["title"].lower()]

# ✅ 点赞文章 ——  
@app.post("/posts/{post_id}/like")
def like_post(post_id: int):
    db = read_db()
    for p in db["posts"]:
        if p["id"] == post_id:
            p["likes"] = p.get("likes", 0) + 1
            write_db(db)
            return {"likes": p["likes"]}
    raise HTTPException(404, "文章不存在")

# ✅ 获取用户的文章 ——
@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int):
    db = read_db()
    return [p for p in db["posts"] if p["authorId"] == user_id]

# ✅ 评论系统 API ——

# 获取文章的评论
@app.get("/posts/{post_id}/comments")
def get_post_comments(post_id: int):
    db = read_db()
    comments = [c for c in db["comments"] if c["postId"] == post_id]

    # 获取评论作者信息
    for comment in comments:
        for user in db["users"]:
            if user["id"] == comment["authorId"]:
                comment["author"] = {
                    "id": user["id"],
                    "username": user.get("username", user["email"]),
                    "avatar": user["avatar"]
                }
                break

    return comments

# 创建评论
@app.post("/posts/{post_id}/comments")
def create_comment(post_id: int, comment: CommentIn, current_user: dict = Depends(get_current_user)):
    db = read_db()

    # 检查文章是否存在
    post_exists = any(p["id"] == post_id for p in db["posts"])
    if not post_exists:
        raise HTTPException(404, "文章不存在")

    # 如果是回复评论，检查父评论是否存在
    if comment.parentId:
        parent_exists = any(c["id"] == comment.parentId and c["postId"] == post_id for c in db["comments"])
        if not parent_exists:
            raise HTTPException(404, "父评论不存在")

    comment_id = max((c["id"] for c in db["comments"]), default=0) + 1
    new_comment = {
        "id": comment_id,
        "postId": post_id,
        "authorId": current_user["id"],
        "content": comment.content,
        "parentId": comment.parentId,
        "likes": 0,
        "created_at": "2024-06-17T00:00:00Z",  # 实际应用中使用 datetime.utcnow()
        "updated_at": "2024-06-17T00:00:00Z"
    }

    db["comments"].append(new_comment)

    # 更新文章评论数
    for post in db["posts"]:
        if post["id"] == post_id:
            # 重新计算评论数
            comment_count = len([c for c in db["comments"] if c["postId"] == post["id"]])
            post["comments_count"] = comment_count
            break

    write_db(db)

    # 返回包含作者信息的评论
    new_comment["author"] = {
        "id": current_user["id"],
        "username": current_user.get("username", current_user["email"]),
        "avatar": current_user["avatar"]
    }

    return new_comment

# 删除评论
@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    comment_index = None
    for i, comment in enumerate(db["comments"]):
        if comment["id"] == comment_id:
            # 只有评论作者或管理员可以删除评论
            if comment["authorId"] != current_user["id"] and current_user.get("role") != "admin":
                raise HTTPException(403, "无权限删除此评论")
            comment_index = i
            break

    if comment_index is None:
        raise HTTPException(404, "评论不存在")

    deleted_comment = db["comments"].pop(comment_index)

    # 更新文章评论数
    for post in db["posts"]:
        if post["id"] == deleted_comment["postId"]:
            # 重新计算评论数
            comment_count = len([c for c in db["comments"] if c["postId"] == post["id"]])
            post["comments_count"] = comment_count
            break

    write_db(db)
    return {"message": "评论已删除"}

# 点赞评论
@app.post("/comments/{comment_id}/like")
def like_comment(comment_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    for comment in db["comments"]:
        if comment["id"] == comment_id:
            comment["likes"] = comment.get("likes", 0) + 1
            write_db(db)
            return {"likes": comment["likes"]}

    raise HTTPException(404, "评论不存在")

# ✅ 标签系统 API ——

# 获取所有标签
@app.get("/tags")
def get_tags():
    db = read_db()
    return db["tags"]

# 创建标签
@app.post("/tags")
def create_tag(tag: TagIn, current_user: dict = Depends(get_current_user)):
    db = read_db()

    # 检查标签是否已存在
    if any(t["name"] == tag.name for t in db["tags"]):
        raise HTTPException(400, "标签已存在")

    tag_id = max((t["id"] for t in db["tags"]), default=0) + 1
    new_tag = {
        "id": tag_id,
        "name": tag.name,
        "description": tag.description or "",
        "color": tag.color,
        "post_count": 0
    }

    db["tags"].append(new_tag)
    write_db(db)
    return new_tag

# 根据标签获取文章
@app.get("/tags/{tag_name}/posts")
def get_posts_by_tag(tag_name: str):
    db = read_db()
    posts = [p for p in db["posts"] if tag_name in p.get("tags", [])]
    return posts

# ✅ 文件上传增强 ——

# 上传用户头像（增强版）
@app.post("/users/{user_id}/avatar")
async def upload_user_avatar(user_id: int, file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    # 检查权限：只能上传自己的头像或管理员
    if current_user["id"] != user_id and current_user.get("role") != "admin":
        raise HTTPException(403, "无权限上传此用户头像")

    # 检查文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "只能上传图片文件")

    ext = os.path.splitext(file.filename)[1]
    path = f"{UPLOAD_DIR}/avatars/{user_id}{ext}"

    with open(path, "wb") as f:
        f.write(await file.read())

    db = read_db()
    avatar_url = f"/static/avatars/{user_id}{ext}"
    for u in db["users"]:
        if u["id"] == user_id:
            u["avatar"] = avatar_url
            break
    write_db(db)

    return {"avatar": avatar_url, "url": avatar_url}

# 获取用户信息（增强版）
@app.get("/users/{user_id}/profile")
def get_user_profile(user_id: int):
    db = read_db()
    for u in db["users"]:
        if u["id"] == user_id:
            # 计算用户的文章数
            post_count = len([p for p in db["posts"] if p["authorId"] == user_id])

            return {
                "id": u["id"],
                "username": u.get("username", u["email"]),
                "email": u["email"],
                "bio": u.get("bio", ""),
                "avatar": u["avatar"],
                "created_at": u.get("created_at"),
                "followers_count": u.get("followers_count", 0),
                "following_count": u.get("following_count", 0),
                "post_count": post_count
            }
    raise HTTPException(404, "用户不存在")

# ✅ SVG头像生成 ——
@app.get("/users/{user_id}/avatar.svg")
def get_user_avatar_svg_endpoint(user_id: int, style: str = "initial"):
    db = read_db()

    # 查找用户
    user = None
    for u in db["users"]:
        if u["id"] == user_id:
            user = u
            break

    if not user:
        raise HTTPException(404, "用户不存在")

    username = user.get("username", user["email"])
    svg_content = get_user_avatar_svg(user_id, username, style)

    return Response(content=svg_content, media_type="image/svg+xml")

# ✅ 关注系统 API ——

# 关注用户
@app.post("/users/{user_id}/follow")
def follow_user(user_id: int, current_user: dict = Depends(get_current_user)):
    if current_user["id"] == user_id:
        raise HTTPException(400, "不能关注自己")

    db = read_db()

    # 检查目标用户是否存在
    target_user = None
    for u in db["users"]:
        if u["id"] == user_id:
            target_user = u
            break

    if not target_user:
        raise HTTPException(404, "用户不存在")

    # 检查是否已经关注
    existing_follow = any(
        f["followerId"] == current_user["id"] and f["followingId"] == user_id
        for f in db["follows"]
    )

    if existing_follow:
        raise HTTPException(400, "已经关注了该用户")

    # 创建关注关系
    follow_id = max((f["id"] for f in db["follows"]), default=0) + 1
    new_follow = {
        "id": follow_id,
        "followerId": current_user["id"],
        "followingId": user_id,
        "created_at": "2024-06-17T00:00:00Z"
    }

    db["follows"].append(new_follow)

    # 更新用户关注数
    for u in db["users"]:
        if u["id"] == current_user["id"]:
            u["following_count"] = u.get("following_count", 0) + 1
        elif u["id"] == user_id:
            u["followers_count"] = u.get("followers_count", 0) + 1

    # 创建通知
    notification_id = max((n["id"] for n in db["notifications"]), default=0) + 1
    notification = {
        "id": notification_id,
        "userId": user_id,
        "type": "follow",
        "title": "新的关注者",
        "content": f"{current_user.get('username', current_user['email'])} 关注了你",
        "relatedId": current_user["id"],
        "relatedType": "user",
        "isRead": False,
        "created_at": "2024-06-17T00:00:00Z"
    }

    db["notifications"].append(notification)
    write_db(db)

    return {"message": "关注成功"}

# 取消关注
@app.delete("/users/{user_id}/follow")
def unfollow_user(user_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    # 查找关注关系
    follow_index = None
    for i, follow in enumerate(db["follows"]):
        if follow["followerId"] == current_user["id"] and follow["followingId"] == user_id:
            follow_index = i
            break

    if follow_index is None:
        raise HTTPException(400, "未关注该用户")

    # 删除关注关系
    db["follows"].pop(follow_index)

    # 更新用户关注数
    for u in db["users"]:
        if u["id"] == current_user["id"]:
            u["following_count"] = max(0, u.get("following_count", 0) - 1)
        elif u["id"] == user_id:
            u["followers_count"] = max(0, u.get("followers_count", 0) - 1)

    write_db(db)
    return {"message": "取消关注成功"}

# 获取用户的关注列表
@app.get("/users/{user_id}/following")
def get_user_following(user_id: int):
    db = read_db()

    following_ids = [f["followingId"] for f in db["follows"] if f["followerId"] == user_id]
    following_users = []

    for u in db["users"]:
        if u["id"] in following_ids:
            following_users.append({
                "id": u["id"],
                "username": u.get("username", u["email"]),
                "email": u["email"],
                "avatar": u["avatar"],
                "bio": u.get("bio", ""),
                "followers_count": u.get("followers_count", 0)
            })

    return following_users

# 获取用户的粉丝列表
@app.get("/users/{user_id}/followers")
def get_user_followers(user_id: int):
    db = read_db()

    follower_ids = [f["followerId"] for f in db["follows"] if f["followingId"] == user_id]
    followers = []

    for u in db["users"]:
        if u["id"] in follower_ids:
            followers.append({
                "id": u["id"],
                "username": u.get("username", u["email"]),
                "email": u["email"],
                "avatar": u["avatar"],
                "bio": u.get("bio", ""),
                "followers_count": u.get("followers_count", 0)
            })

    return followers

# 检查是否关注某用户
@app.get("/users/{user_id}/follow/status")
def check_follow_status(user_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    is_following = any(
        f["followerId"] == current_user["id"] and f["followingId"] == user_id
        for f in db["follows"]
    )

    return {"isFollowing": is_following}

# ✅ 通知系统 API ——

# 获取用户通知
@app.get("/notifications")
def get_notifications(current_user: dict = Depends(get_current_user), page: int = 1, limit: int = 20):
    db = read_db()

    user_notifications = [n for n in db["notifications"] if n["userId"] == current_user["id"]]
    user_notifications.sort(key=lambda x: x["created_at"], reverse=True)

    # 分页
    start = (page - 1) * limit
    end = start + limit
    paginated_notifications = user_notifications[start:end]

    return {
        "items": paginated_notifications,
        "has_more": end < len(user_notifications),
        "total": len(user_notifications),
        "unread_count": len([n for n in user_notifications if not n["isRead"]])
    }

# 标记通知为已读
@app.put("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    for notification in db["notifications"]:
        if notification["id"] == notification_id and notification["userId"] == current_user["id"]:
            notification["isRead"] = True
            write_db(db)
            return {"message": "通知已标记为已读"}

    raise HTTPException(404, "通知不存在")

# 标记所有通知为已读
@app.put("/notifications/read-all")
def mark_all_notifications_read(current_user: dict = Depends(get_current_user)):
    db = read_db()

    count = 0
    for notification in db["notifications"]:
        if notification["userId"] == current_user["id"] and not notification["isRead"]:
            notification["isRead"] = True
            count += 1

    write_db(db)
    return {"message": f"已标记 {count} 条通知为已读"}

# 删除通知
@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    notification_index = None
    for i, notification in enumerate(db["notifications"]):
        if notification["id"] == notification_id and notification["userId"] == current_user["id"]:
            notification_index = i
            break

    if notification_index is None:
        raise HTTPException(404, "通知不存在")

    db["notifications"].pop(notification_index)
    write_db(db)
    return {"message": "通知已删除"}

# 获取未读通知数量
@app.get("/notifications/unread-count")
def get_unread_count(current_user: dict = Depends(get_current_user)):
    db = read_db()

    unread_count = len([
        n for n in db["notifications"]
        if n["userId"] == current_user["id"] and not n["isRead"]
    ])

    return {"count": unread_count}

# ✅ 点赞系统 API ——

# 点赞文章
@app.post("/posts/{post_id}/like")
def like_post(post_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    # 检查文章是否存在
    post = None
    for p in db["posts"]:
        if p["id"] == post_id:
            post = p
            break

    if not post:
        raise HTTPException(404, "文章不存在")

    # 检查是否已经点赞
    existing_like = any(
        like["userId"] == current_user["id"] and like["postId"] == post_id
        for like in db["likes"]
    )

    if existing_like:
        raise HTTPException(400, "已经点赞过了")

    # 创建点赞记录
    like_id = max((like["id"] for like in db["likes"]), default=0) + 1
    new_like = {
        "id": like_id,
        "userId": current_user["id"],
        "postId": post_id,
        "created_at": "2024-06-17T00:00:00Z"
    }

    db["likes"].append(new_like)

    # 更新文章点赞数
    post["likes_count"] = post.get("likes_count", 0) + 1

    write_db(db)
    return {"message": "点赞成功"}

# 取消点赞
@app.delete("/posts/{post_id}/like")
def unlike_post(post_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    # 查找点赞记录
    like_index = None
    for i, like in enumerate(db["likes"]):
        if like["userId"] == current_user["id"] and like["postId"] == post_id:
            like_index = i
            break

    if like_index is None:
        raise HTTPException(400, "未点赞该文章")

    # 删除点赞记录
    db["likes"].pop(like_index)

    # 更新文章点赞数
    for post in db["posts"]:
        if post["id"] == post_id:
            post["likes_count"] = max(0, post.get("likes_count", 0) - 1)
            break

    write_db(db)
    return {"message": "取消点赞成功"}

# ✅ 收藏系统 API ——

# 收藏文章
@app.post("/posts/{post_id}/bookmark")
def bookmark_post(post_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    # 检查文章是否存在
    post = None
    for p in db["posts"]:
        if p["id"] == post_id:
            post = p
            break

    if not post:
        raise HTTPException(404, "文章不存在")

    # 检查是否已经收藏
    existing_bookmark = any(
        bookmark["userId"] == current_user["id"] and bookmark["postId"] == post_id
        for bookmark in db["bookmarks"]
    )

    if existing_bookmark:
        raise HTTPException(400, "已经收藏过了")

    # 创建收藏记录
    bookmark_id = max((bookmark["id"] for bookmark in db["bookmarks"]), default=0) + 1
    new_bookmark = {
        "id": bookmark_id,
        "userId": current_user["id"],
        "postId": post_id,
        "created_at": "2024-06-17T00:00:00Z"
    }

    db["bookmarks"].append(new_bookmark)

    # 更新文章收藏数
    post["bookmarks_count"] = post.get("bookmarks_count", 0) + 1

    write_db(db)
    return {"message": "收藏成功"}

# 取消收藏
@app.delete("/posts/{post_id}/bookmark")
def unbookmark_post(post_id: int, current_user: dict = Depends(get_current_user)):
    db = read_db()

    # 查找收藏记录
    bookmark_index = None
    for i, bookmark in enumerate(db["bookmarks"]):
        if bookmark["userId"] == current_user["id"] and bookmark["postId"] == post_id:
            bookmark_index = i
            break

    if bookmark_index is None:
        raise HTTPException(400, "未收藏该文章")

    # 删除收藏记录
    db["bookmarks"].pop(bookmark_index)

    # 更新文章收藏数
    for post in db["posts"]:
        if post["id"] == post_id:
            post["bookmarks_count"] = max(0, post.get("bookmarks_count", 0) - 1)
            break

    write_db(db)
    return {"message": "取消收藏成功"}

# ✅ 管理后台 API ——

# 获取系统统计信息
@app.get("/admin/stats")
def get_admin_stats(admin_user: dict = Depends(get_admin_user)):
    db = read_db()

    stats = {
        "users_count": len(db["users"]),
        "posts_count": len(db["posts"]),
        "comments_count": len(db["comments"]),
        "tags_count": len(db["tags"]),
        "follows_count": len(db["follows"]),
        "notifications_count": len(db["notifications"])
    }

    return stats

# 获取所有用户（管理员）
@app.get("/admin/users")
def get_all_users(admin_user: dict = Depends(get_admin_user), page: int = 1, limit: int = 20):
    db = read_db()

    users = []
    for u in db["users"]:
        post_count = len([p for p in db["posts"] if p["authorId"] == u["id"]])
        comment_count = len([c for c in db["comments"] if c["authorId"] == u["id"]])

        users.append({
            "id": u["id"],
            "email": u["email"],
            "username": u.get("username", u["email"]),
            "role": u.get("role", "user"),
            "avatar": u["avatar"],
            "created_at": u.get("created_at"),
            "followers_count": u.get("followers_count", 0),
            "following_count": u.get("following_count", 0),
            "post_count": post_count,
            "comment_count": comment_count
        })

    # 分页
    start = (page - 1) * limit
    end = start + limit
    paginated_users = users[start:end]

    return {
        "items": paginated_users,
        "has_more": end < len(users),
        "total": len(users)
    }

# 删除用户（管理员）
@app.delete("/admin/users/{user_id}")
def delete_user_admin(user_id: int, admin_user: dict = Depends(get_admin_user)):
    if user_id == admin_user["id"]:
        raise HTTPException(400, "不能删除自己")

    db = read_db()

    # 删除用户
    user_index = None
    for i, u in enumerate(db["users"]):
        if u["id"] == user_id:
            user_index = i
            break

    if user_index is None:
        raise HTTPException(404, "用户不存在")

    db["users"].pop(user_index)

    # 删除用户相关数据
    db["posts"] = [p for p in db["posts"] if p["authorId"] != user_id]
    db["comments"] = [c for c in db["comments"] if c["authorId"] != user_id]
    db["follows"] = [f for f in db["follows"] if f["followerId"] != user_id and f["followingId"] != user_id]
    db["notifications"] = [n for n in db["notifications"] if n["userId"] != user_id]

    write_db(db)
    return {"message": "用户已删除"}

# 获取所有文章（管理员）
@app.get("/admin/posts")
def get_all_posts_admin(admin_user: dict = Depends(get_admin_user), page: int = 1, limit: int = 20):
    db = read_db()

    posts = []
    for p in db["posts"]:
        # 获取作者信息
        author = None
        for u in db["users"]:
            if u["id"] == p["authorId"]:
                author = {
                    "id": u["id"],
                    "username": u.get("username", u["email"]),
                    "email": u["email"]
                }
                break

        comment_count = len([c for c in db["comments"] if c["postId"] == p["id"]])

        posts.append({
            **p,
            "author": author,
            "comment_count": comment_count
        })

    # 按创建时间排序
    posts.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    # 分页
    start = (page - 1) * limit
    end = start + limit
    paginated_posts = posts[start:end]

    return {
        "items": paginated_posts,
        "has_more": end < len(posts),
        "total": len(posts)
    }

# 删除文章（管理员）
@app.delete("/admin/posts/{post_id}")
def delete_post_admin(post_id: int, admin_user: dict = Depends(get_admin_user)):
    db = read_db()

    # 删除文章
    post_index = None
    for i, p in enumerate(db["posts"]):
        if p["id"] == post_id:
            post_index = i
            break

    if post_index is None:
        raise HTTPException(404, "文章不存在")

    db["posts"].pop(post_index)

    # 删除相关评论
    db["comments"] = [c for c in db["comments"] if c["postId"] != post_id]

    write_db(db)
    return {"message": "文章已删除"}

# 获取所有评论（管理员）
@app.get("/admin/comments")
def get_all_comments_admin(admin_user: dict = Depends(get_admin_user), page: int = 1, limit: int = 20):
    db = read_db()

    comments = []
    for c in db["comments"]:
        # 获取作者信息
        author = None
        for u in db["users"]:
            if u["id"] == c["authorId"]:
                author = {
                    "id": u["id"],
                    "username": u.get("username", u["email"]),
                    "email": u["email"]
                }
                break

        # 获取文章信息
        post = None
        for p in db["posts"]:
            if p["id"] == c["postId"]:
                post = {
                    "id": p["id"],
                    "title": p["title"],
                    "slug": p["slug"]
                }
                break

        comments.append({
            **c,
            "author": author,
            "post": post
        })

    # 按创建时间排序
    comments.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    # 分页
    start = (page - 1) * limit
    end = start + limit
    paginated_comments = comments[start:end]

    return {
        "items": paginated_comments,
        "has_more": end < len(comments),
        "total": len(comments)
    }
