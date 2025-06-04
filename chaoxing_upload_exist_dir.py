from ChaoxingUpload.chaoxing_upload_dir import upload_files_to_chaoxing

import os

# 根目录（你可以改成任意盘符路径）
root_dir = r"G:\2022_学生竞赛"

# 自动获取盘符根目录 (如 F:\)
drive, _ = os.path.splitdrive(root_dir)
drive_root = drive + "\\"  # 保证有反斜杠

folders = []

for foldername, subfolders, filenames in os.walk(root_dir):
    if filenames:
        abs_path = os.path.abspath(foldername)
        # 相对于盘符根目录的路径
        rel_path = os.path.relpath(abs_path, drive_root).replace("\\", "/")
        upload_path = f"课程PBL项目/历年比赛作品归档/2022/{rel_path}"
        folders.append((abs_path, upload_path))

print(f"🎉 Done! 共 {len(folders)} 个包含文件的文件夹。")


for local_folder, remote_folder in folders:
    print(f"\n➡️ 开始上传：{local_folder} -> {remote_folder}")
    upload_files_to_chaoxing(
        username="X",
        password="X",
        course_url="https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/tch?courseid=224806989&clazzid=96513826&cpi=244937480&enc=e64ca0b26d9f168b4facb6a4a5137fda&t=1748252130471&pageHeader=3&v=2&hideHead=0",
        upload_folder=local_folder,
        multi_level_folder=remote_folder,
        chromedriver_path="./ChromeDriver/chromedriver.exe"
    )
