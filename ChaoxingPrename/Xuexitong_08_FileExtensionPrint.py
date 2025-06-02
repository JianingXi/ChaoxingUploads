import os
from collections import defaultdict

def load_whitelist(file_path):
    """
    从文本文件中加载白名单后缀，生成 set。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return {line.strip().lower() for line in f if line.strip()}

def count_file_extensions(path, whitelist_file, output_file):
    """
    递归统计指定目录及其子目录中所有文件的后缀名。
    只保存不在白名单中的后缀，不保存数量，且第一行无提示语。
    """
    # 加载白名单
    whitelist_exts = load_whitelist(whitelist_file)

    extension_counts = defaultdict(int)

    for root, dirs, files in os.walk(path):
        for file in files:
            _, ext = os.path.splitext(file)
            ext = ext.lower()  # 统一转小写，避免重复
            if ext:
                extension_counts[ext] += 1

    # 只保存不在白名单中的后缀（无数量）
    unknown_extensions = [ext for ext in extension_counts.keys() if ext not in whitelist_exts]

    # 写入文件（首行无任何提示语）
    with open(output_file, 'w', encoding='utf-8') as f:
        for ext in unknown_extensions:
            f.write(f"{ext}\n")

    # 同时在控制台打印
    print("⚠️ 不在白名单中的后缀：")
    for ext in unknown_extensions:
        print(ext)

if __name__ == "__main__":
    target_path = r"C:\迅雷下载\互联网加_挑战杯_大创等合集"
    whitelist_file = r"C:\MyPython\ChaoxingUploads\ChaoxingPrename\UploadList\whitelist.txt"
    output_file = r"C:\MyPython\ChaoxingUploads\ChaoxingPrename\UploadList\Unknownlist.txt"
    count_file_extensions(target_path, whitelist_file, output_file)
