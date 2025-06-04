import os
import shutil

import os
import shutil

def merge_single_subfolder_or_file(root_dir):
    merged = False
    all_dirs = list(os.walk(root_dir, topdown=False))  # 缓存结构

    for dirpath, dirnames, filenames in all_dirs:
        if not os.path.exists(dirpath):  # 🚨 防止路径失效
            continue

        current_folder = os.path.basename(dirpath)
        parent_path = os.path.dirname(dirpath)

        # Case 1: 只有一个子文件夹且无文件
        if len(dirnames) == 1 and len(filenames) == 0:
            only_subdir = dirnames[0]
            only_subdir_path = os.path.join(dirpath, only_subdir)

            if not os.path.exists(only_subdir_path):  # 🚨 子文件夹可能已被移动或删除
                continue

            longer_name = max(current_folder, only_subdir, key=len)

            for item in os.listdir(only_subdir_path):
                shutil.move(os.path.join(only_subdir_path, item), dirpath)

            os.rmdir(only_subdir_path)

            if current_folder != longer_name:
                new_path = os.path.join(parent_path, longer_name)
                if not os.path.exists(new_path):  # 防止重名冲突
                    os.rename(dirpath, new_path)
                    print(f"✅ 合并文件夹并重命名: {dirpath} -> {new_path}")
                else:
                    print(f"⚠️ 跳过重命名，目标已存在: {new_path}")
            else:
                print(f"✅ 合并文件夹: {dirpath}")

            merged = True

        # Case 2: 只有一个文件且无子文件夹
        elif len(dirnames) == 0 and len(filenames) == 1:
            only_file = filenames[0]
            only_file_path = os.path.join(dirpath, only_file)

            if not os.path.exists(only_file_path):
                continue

            longer_name = max(current_folder, os.path.splitext(only_file)[0], key=len)
            new_file_ext = os.path.splitext(only_file)[1]
            new_file_name = f"{longer_name}{new_file_ext}"
            new_file_path = os.path.join(parent_path, new_file_name)

            # 若目标文件存在则避免覆盖
            if not os.path.exists(new_file_path):
                shutil.move(only_file_path, new_file_path)
                os.rmdir(dirpath)
                print(f"✅ 文件移出并重命名: {only_file_path} -> {new_file_path}")
                merged = True
            else:
                print(f"⚠️ 跳过移动，目标文件已存在: {new_file_path}")

    return merged

def dir_merge_batch(root_folder: str):
    while True:
        changed = merge_single_subfolder_or_file(root_folder)
        if not changed:
            break
        print("🔄 本轮有合并操作，继续下一轮检测...")

    print("🎉 所有合并操作已完成，文件夹已规整")
