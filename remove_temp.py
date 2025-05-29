import os

# 指定要删除文件的目录
root_dir = r"F:\普中-麒麟F407开发板资料"

# 遍历所有子文件夹和文件
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        # 获取文件扩展名
        ext = os.path.splitext(filename)[1]
        # 如果文件是 .h, .c, .cpp, .py，则删除
        if ext in ['.ini', '.py']:
            file_path = os.path.join(foldername, filename)
            try:
                os.remove(file_path)
                print(f"已删除：{file_path}")
            except Exception as e:
                print(f"删除失败：{file_path}, 错误：{e}")

print("删除完成！")
