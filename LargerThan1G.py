
import os

# 设置扫描的根目录
root_folder = r"I:\Alpha\Store历史存档\Y2024_机械臂配套软件"

# 定义文件大小阈值（单位：字节）
size_threshold = int(1.0 * 1024 * 1024 * 1024)  # 1.0 GB

# 存储大文件路径
large_files = []

# 遍历所有子目录和文件
for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        try:
            file_size = os.path.getsize(filepath)
            if file_size > size_threshold:
                large_files.append(os.path.abspath(filepath))
        except Exception as e:
            print(f"⚠️ 无法访问 {filepath}，错误：{e}")

# 输出到文本文件
output_file = "large_files.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for file_path in large_files:
        f.write(file_path + "\n")

print(f"✅ 扫描完毕，共找到 {len(large_files)} 个大于 1.0 GB 的文件。")
print(f"📄 结果已写入：{os.path.abspath(output_file)}")
