import os
import zipfile
import rarfile
import logging

# 初始化日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
failure_log = "failures.txt"
failure_count = {}  # 记录每个压缩包的失败解压次数
MAX_FAILURES = 3    # 最大失败次数，超过则跳过

def extract_archive(archive_path):
    ext = os.path.splitext(archive_path)[1].lower()
    extract_dir = os.path.dirname(archive_path)

    try:
        if ext == ".zip":
            try:
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    namelist = zf.namelist()
                    if len(namelist) == 1 and not namelist[0].endswith('/'):
                        # 只有一个文件，修正中文乱码
                        filename = namelist[0]
                        try:
                            filename = filename.encode('cp437').decode('gbk')
                        except:
                            pass
                        target_path = os.path.join(extract_dir, filename)
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        with open(target_path, 'wb') as f_out, zf.open(namelist[0]) as f_in:
                            f_out.write(f_in.read())
                        logging.info(f"✅ 单文件ZIP解压: {archive_path} -> {target_path}")
                    else:
                        subdir = os.path.splitext(os.path.basename(archive_path))[0]
                        final_dir = os.path.join(extract_dir, subdir)
                        os.makedirs(final_dir, exist_ok=True)
                        for info in zf.infolist():
                            filename = info.filename
                            try:
                                filename = filename.encode('cp437').decode('gbk')
                            except:
                                pass
                            target_path = os.path.join(final_dir, filename)
                            if info.is_dir():
                                os.makedirs(target_path, exist_ok=True)
                            else:
                                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                                with open(target_path, 'wb') as f_out, zf.open(info) as f_in:
                                    f_out.write(f_in.read())
                        logging.info(f"✅ 多文件ZIP解压到: {final_dir}")
                # 解压成功，删除文件
                os.remove(archive_path)
                logging.info(f"🗑️ 已删除压缩包: {archive_path}")

                # 成功解压，清空该文件的失败次数
                failure_count.pop(archive_path, None)

                # 修正解压出来的文件名中文乱码
                fix_chinese_filenames(extract_dir)

            except zipfile.BadZipFile:
                raise Exception("文件不是有效的ZIP文件")

        elif ext == ".rar":
            try:
                with rarfile.RarFile(archive_path) as rf:
                    namelist = rf.namelist()
                    if len(namelist) == 1 and not rf.getinfo(namelist[0]).is_dir():
                        rf.extract(namelist[0], extract_dir)
                        logging.info(f"✅ 单文件RAR解压: {archive_path} -> {extract_dir}")
                    else:
                        subdir = os.path.splitext(os.path.basename(archive_path))[0]
                        final_dir = os.path.join(extract_dir, subdir)
                        os.makedirs(final_dir, exist_ok=True)
                        rf.extractall(final_dir)
                        logging.info(f"✅ 多文件RAR解压到: {final_dir}")
                # 解压成功，删除文件
                os.remove(archive_path)
                logging.info(f"🗑️ 已删除压缩包: {archive_path}")

                # 成功解压，清空该文件的失败次数
                failure_count.pop(archive_path, None)

                # 修正解压出来的文件名中文乱码
                fix_chinese_filenames(extract_dir)

            except rarfile.BadRarFile:
                raise Exception("文件不是有效的RAR文件")
            except rarfile.NeedFirstVolume:
                raise Exception("分卷RAR文件缺少第一卷，无法解压")

        else:
            logging.warning(f"⚠️ 不支持的文件类型: {archive_path}")
            with open(failure_log, "a", encoding="utf-8", newline="\n") as f:
                f.write(f"不支持: {archive_path}\n")
            return

    except Exception as e:
        logging.error(f"❌ 解压失败: {archive_path}，错误: {str(e)}")

        # 记录失败次数
        failure_count[archive_path] = failure_count.get(archive_path, 0) + 1

        if failure_count[archive_path] >= MAX_FAILURES:
            logging.warning(f"⚠️ 文件 {archive_path} 已累计失败 {MAX_FAILURES} 次，跳过后续解压。")
            with open(failure_log, "a", encoding="utf-8", newline="\n") as f:
                f.write(f"超过失败次数跳过: {archive_path}，错误: {str(e)}\n")
        else:
            with open(failure_log, "a", encoding="utf-8", newline="\n") as f:
                f.write(f"解压失败: {archive_path}，错误: {str(e)}\n")

def fix_chinese_filenames(root_dir):
    """
    尝试修正解压出来的文件/文件夹名称中的中文乱码
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in dirnames + filenames:
            try:
                new_name = name.encode('cp437').decode('gbk')
                if new_name != name:
                    old_path = os.path.join(dirpath, name)
                    new_path = os.path.join(dirpath, new_name)
                    os.rename(old_path, new_path)
                    logging.info(f"🔤 修正文件名: {old_path} -> {new_path}")
            except:
                pass

def extract_all_archives(root_path):
    # 如果有历史的失败日志，先删除
    if os.path.exists(failure_log):
        os.remove(failure_log)

    # 多轮循环解压，直到没有压缩包
    while True:
        found_archives = False
        for dirpath, _, filenames in os.walk(root_path):
            for filename in filenames:
                if filename.lower().endswith(('.zip', '.rar')):
                    file_path = os.path.join(dirpath, filename)

                    # 如果该文件已失败超过最大次数，跳过
                    if failure_count.get(file_path, 0) >= MAX_FAILURES:
                        logging.info(f"🔕 文件 {file_path} 失败超过 {MAX_FAILURES} 次，已跳过。")
                        continue

                    found_archives = True
                    extract_archive(file_path)

        if not found_archives:
            # 没有更多压缩包，退出
            break
        else:
            logging.info("🔄 发现新解压文件中的压缩包，继续下一轮...")

def extract_all_archive_dirs(root_dir: str, rarfile_location = r"C:\Program Files\WinRAR\UnRAR.exe"):
    # root_dir = r"G:\竞赛"
    rarfile.UNRAR_TOOL = rarfile_location
    extract_all_archives(root_dir)
    logging.info("🎉 所有压缩包及嵌套压缩包解压完毕！查看failures.txt排查失败文件。")
