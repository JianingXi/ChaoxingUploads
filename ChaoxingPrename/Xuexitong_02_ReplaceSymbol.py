import os
import re

# ⚙️ 要替换的特殊符号列表
SPECIAL_CHARS = r'~!@#$%^&*＋+<>?:"{},\\;\[\]/ '

# ⚙️ 构造正则表达式：匹配上述任意一个字符
pattern = re.compile(f"[{re.escape(SPECIAL_CHARS)}]")

MAX_PATH_LENGTH = 260  # Windows 默认最大路径限制

def clean_name(name):
    """
    将名称中的特殊字符替换为下划线，并合并多个下划线为一个
    🌟 同时将文件夹中的 '.' 替换为 '_' （仅对文件夹做额外处理）
    """
    new_name = pattern.sub("_", name)
    new_name = re.sub(r'_+', '_', new_name)
    return new_name.strip("_")

def clean_dir_name(dirname):
    """
    🌟 额外处理文件夹：将文件夹名中所有 '.' 也替换为 '_'
    """
    name = dirname.replace(".", "_")
    return clean_name(name)

def get_unique_name(directory, new_name):
    """
    检查目录中是否已存在相同名称的文件/文件夹，如果存在，则在结尾加 _数字 直到不冲突
    """
    base, ext = os.path.splitext(new_name)
    candidate = new_name
    counter = 1
    while os.path.exists(os.path.join(directory, candidate)):
        candidate = f"{base}_{counter}{ext}"
        counter += 1
    return candidate

def to_long_path(path):
    """
    解决 Windows 路径过长问题
    """
    if os.name == 'nt':
        path = os.path.abspath(path)
        if not path.startswith("\\\\?\\"):
            return "\\\\?\\" + path
    return path

def move_up_to_shorten_path(path):
    """
    如果路径太长（> MAX_PATH_LENGTH），则尝试将其移动到上一级目录，
    直到路径不再过长，或到达根目录。
    """
    if not os.path.exists(path):
        print(f"⚠️ 文件不存在，跳过：{path}")
        return

    current_path = path
    while len(current_path) > MAX_PATH_LENGTH:
        parent_dir = os.path.dirname(os.path.dirname(current_path))
        if parent_dir == os.path.dirname(parent_dir):
            print(f"⚠️ 已到达根目录，仍无法缩短：{current_path}")
            break
        filename = os.path.basename(current_path)
        new_path = os.path.join(parent_dir, filename)

        # 确保父目录存在
        if not os.path.exists(parent_dir):
            print(f"❌ 父目录不存在，无法移动：{parent_dir}")
            break

        # 避免同名冲突
        if os.path.exists(new_path):
            filename = get_unique_name(parent_dir, filename)
            new_path = os.path.join(parent_dir, filename)

        try:
            os.rename(to_long_path(current_path), to_long_path(new_path))
            print(f"✅ 上移路径: {current_path} -> {new_path}")
            current_path = new_path
        except Exception as e:
            print(f"❌ 上移 {current_path} 时出错: {e}")
            break
    return current_path

def rename_recursively(root_dir):
    """
    递归遍历目录（从最深层开始），对所有文件夹和文件进行重命名
    并在需要时将路径上移到上一级目录
    """
    for current_root, dirs, files in os.walk(root_dir, topdown=False):
        # 先重命名子文件夹
        for dirname in dirs:
            old_dir_path = os.path.join(current_root, dirname)
            if not os.path.exists(old_dir_path):
                print(f"⚠️ 文件夹不存在，跳过：{old_dir_path}")
                continue

            # 🌟 额外处理文件夹名中的 '.' 替换为 '_'
            new_dirname = clean_dir_name(dirname)
            if new_dirname != dirname:
                new_dirname = get_unique_name(current_root, new_dirname)
                new_dir_path = os.path.join(current_root, new_dirname)
                try:
                    os.rename(to_long_path(old_dir_path), to_long_path(new_dir_path))
                    print(f"✅ 重命名文件夹: {old_dir_path} -> {new_dir_path}")
                except Exception as e:
                    print(f"❌ 重命名文件夹 {old_dir_path} 时出错: {e}")
                    continue
                old_dir_path = new_dir_path  # 更新路径
            move_up_to_shorten_path(old_dir_path)

        # 再重命名文件
        for filename in files:
            old_file_path = os.path.join(current_root, filename)
            if not os.path.exists(old_file_path):
                print(f"⚠️ 文件不存在，跳过：{old_file_path}")
                continue

            new_filename = clean_name(filename)
            if new_filename != filename:
                new_filename = get_unique_name(current_root, new_filename)
                new_file_path = os.path.join(current_root, new_filename)
                try:
                    os.rename(to_long_path(old_file_path), to_long_path(new_file_path))
                    print(f"✅ 重命名文件: {old_file_path} -> {new_file_path}")
                except Exception as e:
                    print(f"❌ 重命名文件 {old_file_path} 时出错: {e}")
                    continue
                old_file_path = new_file_path  # 更新路径
            move_up_to_shorten_path(old_file_path)

if __name__ == "__main__":
    target_directory = r"G:\作品\科普组"
    if not os.path.isdir(target_directory):
        print("❌ 错误: 指定的路径不是一个有效的目录!")
        exit(1)
    rename_recursively(target_directory)
    print("🎉 所有处理完成！")
