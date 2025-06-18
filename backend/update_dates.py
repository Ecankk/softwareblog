#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新数据库中文章时间到2025年
"""

import json
import random
from datetime import datetime, timedelta

def generate_2025_dates():
    """生成2025年的随机日期"""
    # 2025年1月1日到现在（6月18日）的日期范围
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 6, 18)
    
    # 计算日期范围
    date_range = (end_date - start_date).days
    
    dates = []
    for i in range(10):  # 生成10个不同的日期
        random_days = random.randint(0, date_range)
        random_date = start_date + timedelta(days=random_days)
        
        # 添加随机的小时和分钟
        random_hour = random.randint(8, 22)  # 8点到22点
        random_minute = random.randint(0, 59)
        
        random_date = random_date.replace(hour=random_hour, minute=random_minute)
        dates.append(random_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    
    return sorted(dates, reverse=True)  # 按时间倒序排列

def update_article_dates():
    """更新文章日期"""
    print("🕒 开始更新文章时间到2025年...")

    # 获取脚本所在目录
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'db.json')

    # 读取数据库
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    # 生成新的日期
    new_dates = generate_2025_dates()
    
    print(f"📝 找到 {len(db['posts'])} 篇文章需要更新")
    
    # 更新每篇文章的时间
    for i, post in enumerate(db['posts']):
        # 使用循环分配日期，确保每篇文章都有合理的时间
        date_index = i % len(new_dates)
        new_date = new_dates[date_index]
        
        old_created = post.get('created_at', '未设置')
        old_updated = post.get('updated_at', '未设置')
        
        # 更新时间
        post['created_at'] = new_date
        post['updated_at'] = new_date
        
        print(f"  ✅ 文章 {i+1}: {post['title'][:30]}...")
        print(f"     旧时间: {old_created}")
        print(f"     新时间: {new_date}")
        print()
    
    # 同时更新其他相关数据的时间
    print("🔄 更新其他数据的时间...")
    
    # 更新评论时间
    comment_dates = generate_2025_dates()
    for i, comment in enumerate(db['comments']):
        date_index = i % len(comment_dates)
        comment['created_at'] = comment_dates[date_index]
    
    # 更新点赞时间
    like_dates = generate_2025_dates()
    for i, like in enumerate(db['likes']):
        date_index = i % len(like_dates)
        like['created_at'] = like_dates[date_index]
    
    # 更新收藏时间
    bookmark_dates = generate_2025_dates()
    for i, bookmark in enumerate(db['bookmarks']):
        date_index = i % len(bookmark_dates)
        bookmark['created_at'] = bookmark_dates[date_index]
    
    # 更新关注时间
    follow_dates = generate_2025_dates()
    for i, follow in enumerate(db['follows']):
        date_index = i % len(follow_dates)
        follow['created_at'] = follow_dates[date_index]
    
    # 更新通知时间
    notification_dates = generate_2025_dates()
    for i, notification in enumerate(db['notifications']):
        date_index = i % len(notification_dates)
        notification['created_at'] = notification_dates[date_index]
    
    # 更新浏览历史时间
    if 'history' in db:
        history_dates = generate_2025_dates()
        for i, history in enumerate(db['history']):
            date_index = i % len(history_dates)
            history['visited_at'] = history_dates[date_index]
    
    # 保存更新后的数据库
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print("✅ 数据库时间更新完成！")
    print(f"📊 更新统计:")
    print(f"   - 文章: {len(db['posts'])} 篇")
    print(f"   - 评论: {len(db['comments'])} 条")
    print(f"   - 点赞: {len(db['likes'])} 个")
    print(f"   - 收藏: {len(db['bookmarks'])} 个")
    print(f"   - 关注: {len(db['follows'])} 个")
    print(f"   - 通知: {len(db['notifications'])} 条")
    if 'history' in db:
        print(f"   - 浏览历史: {len(db['history'])} 条")

if __name__ == "__main__":
    update_article_dates()
