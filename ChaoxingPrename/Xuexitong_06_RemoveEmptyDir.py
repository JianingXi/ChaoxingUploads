import os


def remove_empty_dirs(path):
    """
    递归删除指定目录及其子目录中的空文件夹。
    """
    if not os.path.isdir(path):
        return

    # 首先递归遍历子文件夹
    for root, dirs, files in os.walk(path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # 如果是空文件夹，则删除
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"已删除空文件夹: {dir_path}")


# 使用示例
target_path = r"C:\迅雷下载"
remove_empty_dirs(target_path)
