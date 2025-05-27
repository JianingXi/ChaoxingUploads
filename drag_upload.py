
import pygetwindow as gw
import pyautogui
import time

# 1️⃣ 获取窗口对象
def find_windows():
    explorer_window = None
    browser_window = None
    for title in gw.getAllTitles():
        if title.strip() == "":
            continue
        if "文件夹" in title or "File Explorer" in title or "资源管理器" in title:
            explorer_window = gw.getWindowsWithTitle(title)[0]
        elif " - Google Chrome" in title or "云盘" in title or "百度云" in title:
            browser_window = gw.getWindowsWithTitle(title)[0]
    return explorer_window, browser_window

# 2️⃣ 窗口并排摆放
def arrange_windows():
    explorer_window, browser_window = find_windows()
    if explorer_window and browser_window:
        screen_width, screen_height = pyautogui.size()
        half_width = screen_width // 2

        # 左侧放资源管理器
        explorer_window.resizeTo(half_width, screen_height)
        explorer_window.moveTo(0, 0)

        # 右侧放浏览器
        browser_window.resizeTo(half_width, screen_height)
        browser_window.moveTo(half_width, 0)
        print("✅ 已并排摆放窗口！")
        return True
    else:
        print("❌ 未找到窗口，请手动确认打开！")
        return False

# 3️⃣ 拖拽文件
def drag_file_to_browser():
    # ⚠️ 下面的坐标请手动测量一次（把鼠标移到那个位置，运行 pyautogui.position() 查看）
    file_x, file_y = 300, 300         # 资源管理器里文件的中心坐标
    target_x, target_y = 1300, 500    # 浏览器上传区域中心坐标

    # 拖拽操作
    pyautogui.moveTo(file_x, file_y, duration=0.5)
    pyautogui.mouseDown()
    time.sleep(0.5)
    pyautogui.moveTo(target_x, target_y, duration=1)
    pyautogui.mouseUp()
    print("✅ 文件拖拽完成！")

if __name__ == "__main__":
    # 步骤：先调整窗口
    success = arrange_windows()
    if success:
        time.sleep(2)  # 等待窗口完全就绪
        # 再执行拖拽
        drag_file_to_browser()
