import os
import subprocess


def file_format_to_rar(root_dir, target_exts, rar_exe_path=r"C:\Program Files\WinRAR\rar.exe"):
    """
    批量压缩指定目录下的目标后缀文件，并删除原文件

    参数：
    - root_dir: 根目录路径
    - target_exts: 需要压缩的文件后缀集合
    - rar_exe_path: WinRAR 可执行文件的完整路径
    """
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

            if not os.path.exists(filepath):
                print(f"⚠️ 文件不存在：{filepath}")
                continue

            rar_name = f"{os.path.splitext(filename)[0]}_{ext_tag}.rar"
            rar_path = os.path.join(foldername, rar_name)

            # 构造 WinRAR 命令
            cmd = f'"{rar_exe_path}" a -ep1 "{rar_path}" "{filepath}"'
            try:
                subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"✅ 已打包：{filepath} -> {rar_path}")
                os.remove(filepath)
                print(f"✅ 已删除：{filepath}")
            except Exception as e:
                print(f"❌ 压缩或删除失败：{filepath}，错误：{e}")

    print("🎉 操作完成！")


# 示例调用
if __name__ == "__main__":
    root_dir = r"I:\STM32"
    target_exts = {'.intlib', '.chm', '.apk', '.tpl', '.dll', '.rtf', '.exe', '.cnt', '.hlp',
                   '.pos', '.fon', '.bin', '.nes', '<无后缀>', '.gif', '.cdl', '.mld', '.tcl', '.example',
                   '.vcproj', '.sln', '.cmd', '.ccxml', '.cproject', '.ccsproject', '.whs',
                   '.prefs', '.inf', '.ptl', '.bpl', '.lrc', '.sms', '.nes', '.shtml', '.onnx',
                   '.action'}

    file_format_to_rar(root_dir, target_exts)
