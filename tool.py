import os

# 白名单目录：为空表示不过滤（全目录遍历）
WHITELIST_FOLDERS = []  # 示例：["src", "docs"]

# 包含的文件类型
INCLUDED_EXTENSIONS = [".py", ".html",".vue", ".js", ".md", ".txt","cjs",".css"]

# 仅根据目录名排除（不区分路径）
EXCLUDED_FOLDERS = ["venv", ".conda", ".vscode", "__pycache__","node_modules"]

# 根据路径排除（相对于 folder_path）
EXCLUDED_PATHS = []  # 示例：排除 folder_path/a/b 目录

def should_exclude_path(full_path, folder_path):
    # 计算相对路径并标准化（统一使用 /）
    rel_path = os.path.relpath(full_path, folder_path).replace("\\", "/")
    for excluded in EXCLUDED_PATHS:
        if rel_path == excluded or rel_path.startswith(excluded + "/"):
            return True
    return False

def print_tree(folder_path):
    print("📂 项目结构：")
    for root, dirs, files in os.walk(folder_path):
        rel_root = os.path.relpath(root, folder_path).replace("\\", "/")
        if should_exclude_path(root, folder_path):
            dirs[:] = []
            continue
        level = rel_root.count(os.sep)
        indent = '│   ' * level + '├── '
        print(f"{indent}{os.path.basename(root)}/")
        subindent = '│   ' * (level + 1) + '├── '
        for f in files:
            print(f"{subindent}{f}")

def export_content(folder_path, output_file, append=False):
    mode = "a" if append else "w"
    try:
        print(f"开始扫描：{folder_path} 下的所有文件……")
        with open(output_file, mode, encoding="utf-8") as out_file:
            for root, dirs, files in os.walk(folder_path):
                rel_root = os.path.relpath(root, folder_path)
                
                # 白名单控制
                if WHITELIST_FOLDERS:
                    if rel_root == ".":
                        dirs[:] = [d for d in dirs if d in WHITELIST_FOLDERS]
                    else:
                        top_level = rel_root.split(os.sep)[0]
                        if top_level not in WHITELIST_FOLDERS:
                            dirs[:] = []
                            continue

                # 排除目录
                dirs[:] = [
                    d for d in dirs
                    if d not in EXCLUDED_FOLDERS and not should_exclude_path(os.path.join(root, d), folder_path)
                ]

                print(f" 正在进入目录：{root}")
                for file_name in files:
                    lower_name = file_name.lower()
                    if not any(lower_name.endswith(ext) for ext in INCLUDED_EXTENSIONS):
                        continue

                    relative_path = os.path.relpath(
                        os.path.join(root, file_name), folder_path
                    )
                    out_file.write(f"文件路径: {relative_path}\n")
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            out_file.write(f"{content}\n\n")
                    except Exception:
                        out_file.write("无法读取文件内容: 非文本或编码错误\n\n")

        print(f"\n✅ 文件内容已保存到 {output_file}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    folder_path = input("📥 输入文件夹路径: ").strip()
    output_file = os.path.join(os.getcwd(), "output.txt")

    print_tree(folder_path)
    export_content(folder_path, output_file, append=False)

    while True:
        user_input = input("继续添加内容到输出文件？(y/n): ").strip().lower()
        if user_input == "n":
            break
        export_content(folder_path, output_file, append=True)
