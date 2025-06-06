from ChaoxingUpload.chaoxing_upload_dir import upload_all_dirs_recursive

folders = [
    (r"G:\2022_学生竞赛",
     "课程PBL项目/历年比赛作品归档/2022"),
]

for local_folder, remote_folder in folders:
    print(f"\n➡️ 开始上传：{local_folder} -> {remote_folder}")
    upload_all_dirs_recursive(
        local_folder=local_folder,
        remote_folder=remote_folder,
        course_url="https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/tch?courseid=224806989&clazzid=96513826&cpi=244937480&enc=e64ca0b26d9f168b4facb6a4a5137fda&t=1748252130471&pageHeader=3&v=2&hideHead=0",
        username="X",
        password="X",
        chromedriver_path="./ChromeDriver/chromedriver.exe"
    )
