import os, json
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# —— 准备目录和 DB 路径 ——  
DB_PATH = "db.json"
UPLOAD_DIR = "uploads"
# 确保上传目录存在
for sub in ("avatars", "covers"):
    os.makedirs(f"{UPLOAD_DIR}/{sub}", exist_ok=True)

# —— 读写 JSON 的辅助函数 ——  
def read_db():
    with open(DB_PATH, encoding="utf-8") as f:
        return json.load(f)

def write_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# —— 定义请求模型 ——  
class UserIn(BaseModel):
    username: str

class PostIn(BaseModel):
    slug: str
    title: str
    content: str  # Markdown 或 HTML

# —— 启动 FastAPI ——  
app = FastAPI()
# 挂载静态文件目录，前端可通过 /static/avatars/... 或 /static/covers/... 访问
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# —— 用户注册（简化版） ——  
@app.post("/auth/register")
def register(user: UserIn):
    db = read_db()
    if any(u["username"] == user.username for u in db["users"]):
        raise HTTPException(400, "用户名已存在")
    uid = max((u["id"] for u in db["users"]), default=0) + 1
    new = {"id": uid, "username": user.username, "avatar": None}
    db["users"].append(new)
    write_db(db)
    return new

# —— 列出文章 ——  
@app.get("/posts")
def list_posts():
    return read_db()["posts"]

# —— 发布文章 ——  
@app.post("/posts")
def create_post(post: PostIn):
    db = read_db()
    if any(p["slug"] == post.slug for p in db["posts"]):
        raise HTTPException(400, "slug 已存在")
    pid = max((p["id"] for p in db["posts"]), default=0) + 1
    entry = {
        "id": pid,
        "slug": post.slug,
        "title": post.title,
        "content": post.content,
        "cover": None,
        "authorId": 1  # 演示用，固定用户 ID
    }
    db["posts"].append(entry)
    write_db(db)
    return entry

# —— 获取文章详情 ——  
@app.get("/posts/{slug}")
def get_post(slug: str):
    db = read_db()
    for p in db["posts"]:
        if p["slug"] == slug:
            return p
    raise HTTPException(404, "文章不存在")

# —— 上传用户头像 ——  
@app.post("/upload/avatar")
async def upload_avatar(user_id: int, file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    path = f"{UPLOAD_DIR}/avatars/{user_id}{ext}"
    with open(path, "wb") as f:
        f.write(await file.read())
    # 更新 db.json 中该用户的 avatar 字段
    db = read_db()
    for u in db["users"]:
        if u["id"] == user_id:
            u["avatar"] = path
            break
    write_db(db)
    return {"avatar": path}

# —— 上传文章封面 ——  
@app.post("/upload/cover")
async def upload_cover(slug: str, file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    path = f"{UPLOAD_DIR}/covers/{slug}{ext}"
    with open(path, "wb") as f:
        f.write(await file.read())
    # 更新 db.json 中该文章的 cover 字段
    db = read_db()
    for p in db["posts"]:
        if p["slug"] == slug:
            p["cover"] = path
            break
    write_db(db)
    return {"cover": path}
