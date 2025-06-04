import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException


def upload_files_to_chaoxing(
    username,
    password,
    course_url,
    upload_folder,
    multi_level_folder,
    chromedriver_path="./ChromeDriver/chromedriver.exe"
):
    """
    自动将本地第一层文件上传到学习通多级目录的指定文件夹，倒序上传，确保每个文件真正上传完成后再上传下一个。
    """

    # 🟡 先检测本地是否有文件
    file_list = [os.path.join(upload_folder, f)
                  for f in os.listdir(upload_folder)
                  if os.path.isfile(os.path.join(upload_folder, f))]
    if not file_list:
        print(f"📂 本地文件夹 {upload_folder} 下没有文件，跳过文件上传，但继续进入子文件夹处理。")


    # ✅ 如果有文件，继续后续操作
    file_list = [f.replace("\\", "/") for f in file_list]
    file_list.sort(reverse=True)
    print(f"📂 共找到 {len(file_list)} 个文件待上传（倒序上传）：")
    for f in file_list:
        print(" -", f)

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    try:
        # 登录
        driver.get("https://passport2.chaoxing.com/login")
        print("🔐 自动填充用户名和密码…")
        wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys(username)
        driver.find_element(By.ID, "pwd").send_keys(password)
        driver.find_element(By.ID, "pwd").send_keys(Keys.ENTER)
        time.sleep(5)
        print("✅ 已点击登录按钮")

        # 进入课程资料页面
        driver.get(course_url)
        time.sleep(5)
        print("✅ 已进入课程资料页面")

        # iframe 检测并切换
        try:
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)
            print("🔄 已切换到 iframe")
        except Exception:
            print("⚠️ 页面没有 iframe，直接操作主页面")

        # 依次点击多级目录，支持翻页
        folder_levels = multi_level_folder.replace("\\", "/").split("/")
        for folder_name in folder_levels:
            print(f"➡️ 正在查找并点击：{folder_name}")

            folder_found = False
            while not folder_found:
                try:
                    folder_link = driver.find_element(By.XPATH, f"//a[@title='{folder_name}']")
                    folder_link.click()
                    print(f"✅ 已点击文件夹：{folder_name}")
                    folder_found = True
                    time.sleep(1)
                except Exception:
                    next_btns = driver.find_elements(By.XPATH, "//a[contains(@class,'nextPage')]")
                    if not next_btns:
                        raise Exception(f"⚠️ 页面没有“下一页”按钮，且当前页没找到：{folder_name}")
                    else:
                        next_btn = next_btns[0]
                        class_attr = next_btn.get_attribute("class")
                        if "disabled" in class_attr:
                            raise Exception(f"⚠️ 已到最后一页，仍未找到：{folder_name}")
                        else:
                            next_btn.click()
                            print("🔄 当前页未找到，点击“下一页”…")
                            time.sleep(2)

        # 点击“添加资料”按钮，打开上传弹窗
        add_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(),'添加资料')]")))
        add_btn.click()
        print("✅ 已点击“添加资料”按钮，上传弹窗已打开")
        time.sleep(2)

        # 点击“本地上传”按钮
        try:
            local_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@class='popLocalBnt']")))
            local_btn.click()
            print("✅ 已点击“本地上传”按钮，准备上传第一个文件")
        except TimeoutException:
            print("⚠️ 没有找到“本地上传”按钮，跳过当前目录上传")
            return
        time.sleep(2)

        # 依次上传文件，确保每个文件真正上传完成
        for idx, file_path in enumerate(file_list, start=1):
            print(f"\n🚀 [{idx}/{len(file_list)}] 正在上传：{file_path}")
            try:
                file_input = driver.find_element(By.XPATH, "//input[@type='file']")
                file_input.send_keys(file_path)
                print("⏳ 文件已选中，等待上传完成…")
                time.sleep(2)

                # 检测上传状态
                file_waited = 0
                while file_waited < 300:  # 最多等5分钟
                    uploading_spans = driver.find_elements(By.XPATH,
                        "//span[contains(@class,'colorIn') and (contains(text(),'等待上传') or contains(text(),'处理中') or contains(text(),'已完成'))]")
                    if uploading_spans:
                        print(f"⏳ 文件仍在上传中… {len(uploading_spans)} 项目未完成（包括处理中、等待上传、已完成%）")
                    else:
                        print("✅ 文件上传完成，准备下一个")
                        break
                    time.sleep(2)
                    file_waited += 2
                else:
                    print("⚠️ 单个文件上传超时，跳过…")

            except Exception as e:
                import traceback
                print("❌ 上传出错：", e)
                traceback.print_exc()
                continue

            time.sleep(1)

        # 等待整个上传队列最终确认
        print("\n⏳ 最终确认上传队列已完成…")
        time_waited = 0
        while time_waited < 3600:  # 最多等60分钟
            uploading_spans = driver.find_elements(By.XPATH,
                "//span[contains(@class,'colorIn') and (contains(text(),'等待上传') or contains(text(),'处理中') or contains(text(),'已完成'))]")
            if uploading_spans:
                print(f"⏳ 仍在上传中… {len(uploading_spans)} 项目未完成（包括处理中、等待上传、已完成%）")
            else:
                ready_btn = driver.find_elements(By.XPATH, "//a[contains(text(),'选择本地文件')]")
                if ready_btn:
                    print("✅ 所有文件上传完毕，界面已回到初始状态")
                    break
            time.sleep(5)
            time_waited += 5
        else:
            print("⚠️ 上传超时！强制退出检测…")

        print("\n🎉 全部上传已完成，5秒后自动关闭浏览器。")
        time.sleep(5)

    except Exception as e:
        import traceback
        print("❌ 上传出错：", e)
        traceback.print_exc()


    finally:
        driver.quit()


def get_first_level_subfolders(local_folder):
    """
    返回 local_folder 下第一层子文件夹的名字（不递归）
    """
    first_level_folders = []
    with os.scandir(local_folder) as entries:
        for entry in entries:
            if entry.is_dir():
                first_level_folders.append(entry.name)  # 只要文件夹名
    return first_level_folders



def create_online_folders_and_get_mappings(
    upload_folder,
    multi_level_folder,
    course_url,
    username,
    password,
    chromedriver_path="./ChromeDriver/chromedriver.exe"
):
    """
    在学习通中根据本地 upload_folder 下的第一层文件夹，在 multi_level_folder 下新建同名文件夹。
    返回: folder_mappings (dict)，包含每个文件夹的本地路径和线上路径。
    """

    # 🟡 先检测本地是否有子文件夹
    subfolders = get_first_level_subfolders(upload_folder)
    if not subfolders:
        print(f"📂 本地文件夹 {upload_folder} 下没有子文件夹，无需创建线上文件夹，直接退出。")
        return {}

    # ✅ 使用本地 chromedriver
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    folder_mappings = {}

    try:
        # 登录
        driver.get("https://passport2.chaoxing.com/login")
        print("🔐 填充用户名和密码…")
        wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys(username)
        driver.find_element(By.ID, "pwd").send_keys(password)
        driver.find_element(By.ID, "pwd").send_keys(Keys.ENTER)
        time.sleep(5)
        print("✅ 已点击登录按钮")

        # 进入课程资料页面
        driver.get(course_url)
        time.sleep(5)
        print("✅ 已进入课程资料页面")

        # iframe 检测并切换
        try:
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)
            print("🔄 已切换到 iframe")
        except Exception:
            print("⚠️ 页面没有 iframe，直接操作主页面")

        # 依次点击多级目录，支持翻页查找
        folder_levels = multi_level_folder.split("/")
        for folder_name in folder_levels:
            print(f"➡️ 正在查找并点击：{folder_name}")
            folder_found = False

            while not folder_found:
                try:
                    folder_link = driver.find_element(By.XPATH, f"//a[@title='{folder_name}']")
                    folder_link.click()
                    print(f"✅ 已点击文件夹：{folder_name}")
                    folder_found = True
                    time.sleep(1)
                except Exception:
                    next_btns = driver.find_elements(By.XPATH, "//a[contains(@class,'nextPage')]")
                    if not next_btns:
                        raise Exception(f"⚠️ 页面没有“下一页”按钮，且当前页没找到：{folder_name}")
                    else:
                        next_btn = next_btns[0]
                        class_attr = next_btn.get_attribute("class")
                        if "disabled" in class_attr:
                            raise Exception(f"⚠️ 已到最后一页，仍未找到：{folder_name}")
                        else:
                            next_btn.click()
                            print("🔄 当前页未找到，点击“下一页”…")
                            time.sleep(2)

        # 获取本地子文件夹（倒序）
        subfolders.sort(reverse=True)
        print(f"📂 共需新建 {len(subfolders)} 个子文件夹（倒序）：")
        for sf in subfolders:
            print(" -", sf)

        # 依次新建文件夹
        for idx, level in enumerate(subfolders, start=1):
            exists = driver.find_elements(By.XPATH, f"//a[@title='{level}']")
            if exists:
                print(f"✅ 文件夹已存在：{level}")
            else:
                add_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(text(),'新建文件夹')]")))
                add_btn.click()
                time.sleep(1)

                input_box = wait.until(EC.visibility_of_element_located(
                    (By.ID, "nawDirName")))
                input_box.click()
                input_box.clear()
                input_box.send_keys(level)
                time.sleep(0.5)

                confirm_btn = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//a[@onclick='submitFolderPermissionCheck()']")))
                confirm_btn.click()
                print(f"✅ 已新建：{level}")
                time.sleep(1)

            # 记录本地路径 & 线上路径
            local_path = os.path.join(upload_folder, level)
            online_path = f"{multi_level_folder}/{level}".replace("\\", "/")
            folder_mappings[level] = {
                "local_path": local_path,
                "online_path": online_path
            }

            # 检测到最后一个文件夹，启动5秒倒计时后退出
            if idx == len(subfolders):
                print("\n✅ 已完成所有文件夹的创建，5 秒后自动退出…")
                time.sleep(5)

        print("\n🎉 所有文件夹已创建完毕！")
        return folder_mappings

    except Exception as e:
        print("⚠️ 出错：", e)
        return {}

    finally:
        driver.quit()




def upload_all_dirs_recursive(local_folder, remote_folder, course_url, username, password, chromedriver_path):
    """
    递归上传 local_folder 下的所有文件和文件夹到学习通，保持目录结构一致。
    1️⃣ 始终用 Selenium 建立线上文件夹映射
    2️⃣ 上传当前目录的文件（如有）
    3️⃣ 用 Selenium 返回的线上映射继续递归，保证线上目录完整
    4️⃣ 如果 Selenium 出错，放弃该层递归，防止线上缺目录
    """
    local_folder = local_folder.replace("\\", "/")
    remote_folder = remote_folder.replace("\\", "/")

    print(f"\n🚀 开始处理目录：{local_folder} → {remote_folder}")

    # 1️⃣ 建立线上文件夹映射
    mappings = create_online_folders_and_get_mappings(
        upload_folder=local_folder,
        multi_level_folder=remote_folder,
        course_url=course_url,
        username=username,
        password=password,
        chromedriver_path=chromedriver_path
    )

    if mappings is None:
        print(f"⚠️ Selenium 出错，放弃该层递归：{local_folder}")
        return

    # 2️⃣ 上传当前目录的第一层文件
    upload_files_to_chaoxing(
        username=username,
        password=password,
        course_url=course_url,
        upload_folder=local_folder,
        multi_level_folder=remote_folder,
        chromedriver_path=chromedriver_path
    )

    # 3️⃣ 递归进入子文件夹（只用 Selenium 返回的映射，确保线上已建好）
    if mappings and isinstance(mappings, dict):
        for folder_name, mapping in sorted(mappings.items(), reverse=True):
            local_subfolder = mapping["local_path"]
            remote_subfolder = mapping["online_path"]
            print(f"\n🔁 递归进入：{local_subfolder} → {remote_subfolder}")
            upload_all_dirs_recursive(
                local_folder=local_subfolder,
                remote_folder=remote_subfolder,
                course_url=course_url,
                username=username,
                password=password,
                chromedriver_path=chromedriver_path
            )



# =========== 🟡 主入口调用 🟡 =============
if __name__ == "__main__":
    upload_all_dirs_recursive(
        local_folder=r"D:\aaa\bbb",
        remote_folder="ffff/aaa/bbb",
        course_url="https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/tch?courseid=224806989&clazzid=96513826&cpi=244937480&enc=e64ca0b26d9f168b4facb6a4a5137fda&t=1748252130471&pageHeader=3&v=2&hideHead=0",
        username="Phone Number",
        password="Password****",
        chromedriver_path="./ChromeDriver/chromedriver.exe"
    )

