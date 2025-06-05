import os
import shutil
import math

MAX_PATH_LENGTH = 260  # Windows 路径长度限制


def shorten_path_if_needed(file_path):
    """
    如果文件路径过长，逐步将文件移动到上一级目录，直到路径足够短。
    """
    while len(file_path) >= MAX_PATH_LENGTH:
        parent_dir = os.path.dirname(file_path)
        grandparent_dir = os.path.dirname(parent_dir)

        # 如果已经到根目录，则无法再上移
        if parent_dir == grandparent_dir:
            print(f"⚠️ 文件仍然过长，且已无法上移：{file_path}")
            break

        file_name = os.path.basename(file_path)
        new_path = os.path.join(grandparent_dir, file_name)

        try:
            shutil.move(file_path, new_path)
            print(f"✅ 路径过长，已将文件上移：\n {file_path} -> {new_path}")
            file_path = new_path  # 更新路径，继续检查
        except Exception as e:
            print(f"❌ 移动失败：{file_path}，错误：{e}")
            break


def check_and_shorten_all_files(root_dir):
    """
    递归遍历所有文件，检查路径长度，必要时执行 shorten_path_if_needed。
    """
    for foldername, subfolders, filenames in os.walk(root_dir, topdown=False):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            shorten_path_if_needed(file_path)


def split_folder_if_needed(folder, max_files=50):
    """
    检查指定文件夹下的文件数量（不含子文件夹），如果超过 max_files，则拆分为多个子文件夹，
    拆分后的子文件夹名称为原文件夹名称 + 下划线 + 编号。
    """
    # 获取当前目录下所有文件（不包括子目录）
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    num_files = len(files)

    if num_files > max_files:
        # 获取当前文件夹名称
        original_folder_name = os.path.basename(folder)
        # 计算需要拆分的子文件夹数量
        num_splits = math.ceil(num_files / max_files)
        print(f"📂 目录 {folder} 中有 {num_files} 个文件，需要拆分为 {num_splits} 个子文件夹。")

        # 创建拆分用的子文件夹
        split_folders = []
        for i in range(1, num_splits + 1):
            new_folder = os.path.join(folder, f"{original_folder_name}_{i}")
            os.makedirs(new_folder, exist_ok=True)
            split_folders.append(new_folder)

        # 将文件依次分配到各个拆分子文件夹中
        for index, filename in enumerate(files):
            src = os.path.join(folder, filename)
            target_index = index // max_files
            dst = os.path.join(split_folders[target_index], filename)
            shutil.move(src, dst)
            print(f"✅ 移动文件 {src} -> {dst}")


def process_directory_50files(root_dir, max_files=50):
    """
    递归遍历目录：
    1️⃣ 先将路径过长的文件上移，直到不再过长
    2️⃣ 对每个目录调用 split_folder_if_needed 进行拆分
    """
    print("🔍 正在检查并上移路径过长的文件...")
    check_and_shorten_all_files(root_dir)

    print("🔍 正在拆分文件过多的文件夹...")
    for current_dir, subdirs, files in os.walk(root_dir, topdown=False):
        split_folder_if_needed(current_dir, max_files=max_files)

    print("🎉 所有操作已完成！")


if __name__ == "__main__":
    # 修改成你需要操作的目标目录
    target_directory = r"G:\作品\科普组"

    # 调用主函数
    process_directory_50files(target_directory, max_files=50)
