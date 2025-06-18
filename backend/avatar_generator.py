import random
import hashlib

def generate_avatar_svg(user_id, username="User"):
    """
    根据用户ID生成独特的SVG头像
    """
    # 使用用户ID作为种子，确保同一用户总是得到相同的头像
    random.seed(user_id)
    
    # 颜色调色板
    colors = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9",
        "#F8C471", "#82E0AA", "#F1948A", "#85C1E9", "#D7BDE2"
    ]
    
    # 选择颜色
    bg_color = random.choice(colors)
    
    # 生成用户名首字母
    initial = username[0].upper() if username else "U"
    
    # SVG模板
    svg_content = f'''<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad{user_id}" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
            <stop offset="100%" style="stop-color:{adjust_color_brightness(bg_color, -20)};stop-opacity:1" />
        </linearGradient>
    </defs>
    <circle cx="50" cy="50" r="50" fill="url(#grad{user_id})" />
    <text x="50" y="50" font-family="Arial, sans-serif" font-size="36" font-weight="bold" 
          text-anchor="middle" dominant-baseline="central" fill="white">
        {initial}
    </text>
</svg>'''
    
    return svg_content

def adjust_color_brightness(hex_color, percent):
    """
    调整颜色亮度
    """
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # 调整亮度
    new_rgb = []
    for component in rgb:
        new_component = component + (255 - component) * percent / 100
        new_component = max(0, min(255, int(new_component)))
        new_rgb.append(new_component)
    
    return f"#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}"

def generate_geometric_avatar(user_id):
    """
    生成几何图案头像
    """
    random.seed(user_id)
    
    colors = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#DDA0DD", "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9"
    ]
    
    bg_color = random.choice(colors)
    accent_color = random.choice([c for c in colors if c != bg_color])
    
    # 随机选择图案类型
    patterns = ['circles', 'triangles', 'squares']
    pattern = random.choice(patterns)
    
    if pattern == 'circles':
        svg_content = f'''<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="100" fill="{bg_color}"/>
        <circle cx="25" cy="25" r="15" fill="{accent_color}" opacity="0.7"/>
        <circle cx="75" cy="25" r="10" fill="white" opacity="0.5"/>
        <circle cx="25" cy="75" r="12" fill="white" opacity="0.6"/>
        <circle cx="75" cy="75" r="18" fill="{accent_color}" opacity="0.8"/>
        <circle cx="50" cy="50" r="8" fill="white"/>
    </svg>'''
    elif pattern == 'triangles':
        svg_content = f'''<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="100" fill="{bg_color}"/>
        <polygon points="50,10 90,90 10,90" fill="{accent_color}" opacity="0.7"/>
        <polygon points="20,20 40,20 30,40" fill="white" opacity="0.8"/>
        <polygon points="70,60 90,60 80,80" fill="white" opacity="0.6"/>
    </svg>'''
    else:  # squares
        svg_content = f'''<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="100" fill="{bg_color}"/>
        <rect x="10" y="10" width="30" height="30" fill="{accent_color}" opacity="0.7"/>
        <rect x="60" y="10" width="20" height="20" fill="white" opacity="0.8"/>
        <rect x="10" y="60" width="25" height="25" fill="white" opacity="0.6"/>
        <rect x="65" y="65" width="25" height="25" fill="{accent_color}" opacity="0.8"/>
        <rect x="40" y="40" width="20" height="20" fill="white"/>
    </svg>'''
    
    return svg_content

def get_user_avatar_svg(user_id, username="User", style="initial"):
    """
    获取用户头像SVG
    """
    if style == "geometric":
        return generate_geometric_avatar(user_id)
    else:
        return generate_avatar_svg(user_id, username)
