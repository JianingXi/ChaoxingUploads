import os
import subprocess

root_dir = r"F:\普中-麒麟F407开发板资料"
target_exts = {'.intlib', '.chm', '.apk', '.tpl', '.dll', '.rtf', '.exe', '.cnt', '.hlp',
                '.pos', '.fon', '.bin', '.nes', '<无后缀>', '.gif', '.cdl', '.mld', '.tcl', '.example',
                '.vcproj', '.sln', '.cmd', '.ccxml', '.cproject', '.ccsproject', '.whs',
                '.prefs', '.inf', '.ptl', '.bpl', '.lrc', '.sms', '.nes', '.shtml'}

for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        filepath = os.path.join(foldername, filename)
        ext = os.path.splitext(filename)[1].lower()
        if not ext:
            if '<无后缀>' not in target_exts:
                continue
            ext_tag = 'noext'
        else:
            if ext not in target_exts:
                continue
            ext_tag = ext.lstrip('.')

        # 确认文件是否存在
        if not os.path.exists(filepath):
            print(f"⚠️ 文件不存在：{filepath}")
            continue

        # 压缩包名
        rar_name = f"{os.path.splitext(filename)[0]}_{ext_tag}.rar"
        rar_path = os.path.join(foldername, rar_name)

        # shell=True 兼容中文和空格
        RAR_PATH = r"C:\Program Files\WinRAR\rar.exe"
        cmd = f'"{RAR_PATH}" a -ep1 "{rar_path}" "{filepath}"'
        try:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"✅ 已打包：{filepath} -> {rar_path}")
            os.remove(filepath)
            print(f"✅ 已删除：{filepath}")
        except Exception as e:
            print(f"❌ 压缩或删除失败：{filepath}，错误：{e}")

print("🎉 操作完成！")
