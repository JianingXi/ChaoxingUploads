import os
import time
import subprocess
import pyautogui
import pygetwindow as gw
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ========== 配置信息 ==========
USERNAME = "PhoneNumber"
PASSWORD = "Password*****"
CHROMEDRIVER_PATH = "./ChromeDriver/chromedriver.exe"
UPLOAD_FOLDER_PATH = r"D:\Alpha\StoreLatestYears\Store2024\B教学_教学与人才培养_B80_课程录像\信号与系统_习佳宁\Vedio\新建文件夹\D20240426_14"
FOLDER_PATH_ONLINE = "电脑上传文件/abc"
# ============================

def open_browser_and_login():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 20)

    # 1️⃣ 登录
    driver.get("https://passport2.chaoxing.com/login")
    wait.until(EC.presence_of_element_located((By.ID, "phone"))).send_keys(USERNAME)
    driver.find_element(By.ID, "pwd").send_keys(PASSWORD)
    driver.find_element(By.ID, "pwd").send_keys(Keys.ENTER)
    time.sleep(5)
    print("✅ 登录成功")

    # 2️⃣ 进入云盘首页
    driver.get("https://pan-yz.cldisk.com/pcuserpan/index")
    time.sleep(5)
    print("✅ 已进入云盘首页")

    # 3️⃣ 依次进入多层文件夹
    for folder_name in FOLDER_PATH_ONLINE.split("/"):
        folder_xpath = f"//span[@class='name-hover' and @title='{folder_name}']"
        folder_span = wait.until(EC.element_to_be_clickable((By.XPATH, folder_xpath)))
        driver.execute_script("arguments[0].scrollIntoView(true);", folder_span)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", folder_span)
        time.sleep(2)
        print(f"✅ 进入文件夹：{folder_name}")

    # 4️⃣ 点击“上传文件”按钮
    upload_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='上传文件']")))
    driver.execute_script("arguments[0].click();", upload_btn)
    time.sleep(2)
    print("✅ 点击【上传文件】按钮，上传窗口已出现！")

    return driver

def open_explorer_and_arrange():
    # 启动资源管理器
    subprocess.Popen(f'explorer "{UPLOAD_FOLDER_PATH}"')
    time.sleep(2)
    print("✅ 已打开资源管理器窗口")

    # 获取窗口
    explorer_window = None
    browser_window = None
    for w in gw.getAllTitles():
        if "文件夹" in w or "File Explorer" in w or "资源管理器" in w:
            explorer_window = gw.getWindowsWithTitle(w)[0]
        elif " - Google Chrome" in w or "云盘" in w:
            browser_window = gw.getWindowsWithTitle(w)[0]

    if explorer_window and browser_window:
        # 调整窗口位置：左右并排
        screen_width, screen_height = pyautogui.size()
        half_width = screen_width // 2
        explorer_window.resizeTo(half_width, screen_height)
        browser_window.resizeTo(half_width, screen_height)
        explorer_window.moveTo(0, 0)
        browser_window.moveTo(half_width, 0)
        print("✅ 窗口已自动并排摆放")
    else:
        print("❌ 找不到窗口，手动调整吧")

def drag_all_files_to_browser():
    time.sleep(3)  # 确保窗口调整完毕
    # 聚焦资源管理器窗口
    pyautogui.click(100, 100)
    time.sleep(1)

    pyautogui.click(600, 300)
    time.sleep(1)

    # Ctrl+A 全选
    pyautogui.hotkey("ctrl", "a")
    time.sleep(1)

    # 文件起始位置（示例值，确保拖到上传区域）
    start_x, start_y = 300, 300
    target_x, target_y = 1300, 500  # 浏览器上传区域坐标

    # 拖拽
    pyautogui.moveTo(start_x, start_y, duration=0.5)
    pyautogui.mouseDown()
    time.sleep(0.5)
    pyautogui.moveTo(target_x, target_y, duration=1)
    pyautogui.mouseUp()
    print("✅ 已全选文件并拖拽到上传区域！")

if __name__ == "__main__":
    driver = open_browser_and_login()
    open_explorer_and_arrange()
    drag_all_files_to_browser()
    input("🎉 文件上传已模拟，确认上传无误后按回车关闭浏览器…")
    driver.quit()
