import os

def large_than_1g_files(root_folder, size_threshold_gb=1.0, output_file="large_files.txt"):
    """
    扫描指定目录及子目录，找出所有大于 size_threshold_gb 的文件，并写入 output_file

    参数：
    - root_folder: 根目录路径
    - size_threshold_gb: 文件大小阈值（单位 GB，默认为 1.0GB）
    - output_file: 输出结果文件名
    """
    size_threshold = int(size_threshold_gb * 1024 * 1024 * 1024)  # 转换为字节
    large_files = []

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_size = os.path.getsize(filepath)
                if file_size > size_threshold:
                    large_files.append(os.path.abspath(filepath))
            except Exception as e:
                print(f"⚠️ 无法访问 {filepath}，错误：{e}")

    with open(output_file, "w", encoding="utf-8") as f:
        for file_path in large_files:
            f.write(file_path + "\n")

    print(f"✅ 扫描完毕，共找到 {len(large_files)} 个大于 {size_threshold_gb} GB 的文件。")
    print(f"📄 结果已写入：{os.path.abspath(output_file)}")
    return large_files

# 示例调用
if __name__ == "__main__":
    root_dir = r"I:\STM32"
    large_than_1g_files(root_dir, size_threshold_gb=1.0, output_file="../large_files.txt")
