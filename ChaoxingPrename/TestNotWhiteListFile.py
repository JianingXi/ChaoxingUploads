import os

def create_dummy_txt_files(folder, count=100):
    """
    在指定文件夹内批量生成指定数量的.txt文件，内容为“AAA”。
    """
    os.makedirs(folder, exist_ok=True)
    for i in range(count):
        file_path = os.path.join(folder, f"file_{i}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("AAA")
    print(f"已生成 {count} 个内容为'AAA'的txt文件。")

def read_extensions_from_file(file_path):
    """
    从文件中读取后缀列表，每行一个后缀（包括点号 .）。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        extensions = [line.strip() for line in f if line.strip()]
    return extensions

def rename_files_to_extensions(folder, extensions):
    """
    将文件夹内所有.txt文件的后缀改为给定列表的后缀。
    """
    txt_files = [f for f in os.listdir(folder) if f.endswith(".txt")]
    for i, ext in enumerate(extensions):
        if i >= len(txt_files):
            break  # 如果扩展名数大于现有文件数，跳出
        old_file = os.path.join(folder, txt_files[i])
        new_file = os.path.join(folder, os.path.splitext(txt_files[i])[0] + ext)
        os.rename(old_file, new_file)
        print(f"已将 {old_file} 重命名为 {new_file}")

if __name__ == "__main__":
    # 目标文件夹
    target_folder = r".\DummyFiles"

    # 从文件中读取后缀列表
    unknownlist_file = r"..\ChaoxingPrename\UploadList\Unknownlist.txt"
    extensions = read_extensions_from_file(unknownlist_file)

    # 第一步：创建txt文件
    create_dummy_txt_files(target_folder, len(extensions))

    # 第二步：按后缀列表重命名
    rename_files_to_extensions(target_folder, extensions)

    print("✅ 已完成批量创建和重命名操作。")
