from ChaoxingUpload.chaoxing_upload_dir import upload_all_dirs_recursive

folders = [
    (r"I:\Alpha\Store历史存档\Y2024_机械臂配套软件", "最近上传"),
]

for local_folder, remote_folder in folders:
    print(f"\n➡️ 开始上传：{local_folder} -> {remote_folder}")
    upload_all_dirs_recursive(
        local_folder=local_folder,
        remote_folder=remote_folder,
        course_url="https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/tch?courseid=224806989&clazzid=96513826&cpi=244937480&enc=e64ca0b26d9f168b4facb6a4a5137fda&t=1748252130471&pageHeader=3&v=2&hideHead=0",
        username="pn",
        password="ps",
        chromedriver_path="./ChromeDriver/chromedriver.exe"
    )
