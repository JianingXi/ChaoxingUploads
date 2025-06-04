import os
import shutil

def merge_single_subfolder_or_file(root_dir):
    """
    对于每个文件夹：
    - 如果内部只有一个子文件夹且无其他文件，保留较长的名字，合并子文件夹内容。
    - 如果内部只有一个文件且无其他子文件夹，保留较长的名字，移出来，删掉空文件夹。
    返回值: 本轮是否有合并操作
    """
    merged = False  # 记录是否有合并操作

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        current_folder = os.path.basename(dirpath)
        parent_path = os.path.dirname(dirpath)

        # Case 1: 只有一个子文件夹且无其他文件
        if len(dirnames) == 1 and len(filenames) == 0:
            only_subdir = dirnames[0]
            only_subdir_path = os.path.join(dirpath, only_subdir)

            # 比较名字长度
            longer_name = max(current_folder, only_subdir, key=len)

            # 把子文件夹内容移出来
            for item in os.listdir(only_subdir_path):
                shutil.move(os.path.join(only_subdir_path, item), dirpath)

            # 删除空的子文件夹
            os.rmdir(only_subdir_path)

            # 如果名字不同，重命名
            if current_folder != longer_name:
                new_path = os.path.join(parent_path, longer_name)
                os.rename(dirpath, new_path)
                print(f"✅ 合并文件夹并重命名: {dirpath} -> {new_path}")
            else:
                print(f"✅ 合并文件夹: {dirpath}")

            merged = True

        # Case 2: 只有一个文件且无其他子文件夹
        elif len(dirnames) == 0 and len(filenames) == 1:
            only_file = filenames[0]
            only_file_path = os.path.join(dirpath, only_file)

            # 比较名字长度
            longer_name = max(current_folder, os.path.splitext(only_file)[0], key=len)
            new_file_ext = os.path.splitext(only_file)[1]

            # 新的文件名
            new_file_name = f"{longer_name}{new_file_ext}"
            new_file_path = os.path.join(parent_path, new_file_name)

            # 移动文件
            shutil.move(only_file_path, new_file_path)

            # 删除空文件夹
            os.rmdir(dirpath)
            print(f"✅ 文件移出并重命名: {only_file_path} -> {new_file_path}")

            merged = True

    return merged

if __name__ == "__main__":
    root_folder = r"G:\2022_学生竞赛"  # 替换为你的根目录

    # 反复循环，直到没有新的合并
    while True:
        changed = merge_single_subfolder_or_file(root_folder)
        if not changed:
            break
        print("🔄 本轮有合并操作，继续下一轮检测...")

    print("🎉 所有合并操作已完成，文件夹已规整！")
