import os
from ChaoxingPrename.Xuexitong_01_html2pdf import convert_html_files_in_directory
from ChaoxingPrename.Xuexitong_02_ReplaceSymbol import rename_recursively
from ChaoxingPrename.Xuexitong_03_Rename_files_by_Content import rename_files_by_content
from ChaoxingPrename.Xuexitong_04_SplitDirWithin50Files import process_directory
from ChaoxingPrename.Xuexitong_05_FileFormat2RAR import file_format_to_rar
from ChaoxingPrename.Xuexitong_06_LargerThan1G import large_than_1g_files

rename_by_content = 0
target_directory = r"I:\Alpha\StoreLatestYears\Store2023\M02广医事务性工作"

if not os.path.isdir(target_directory):
    print("错误: 指定的路径不是一个有效的目录!")
    exit(1)

convert_html_files_in_directory(target_directory)
rename_recursively(target_directory)
if rename_by_content:
    rename_files_by_content(target_directory)
process_directory(target_directory)


target_exts = {'.intlib', '.chm', '.apk', '.tpl', '.dll', '.rtf', '.exe', '.cnt', '.hlp',
        '.pos', '.fon', '.bin', '.nes', '<无后缀>', '.gif', '.cdl', '.mld', '.tcl', '.example',
        '.vcproj', '.sln', '.cmd', '.ccxml', '.cproject', '.ccsproject', '.whs',
        '.prefs', '.inf', '.ptl', '.bpl', '.lrc', '.sms', '.nes', '.shtml', '.onnx',
        '.action'}

file_format_to_rar(target_directory, target_exts)

large_than_1g_files(target_directory, size_threshold_gb=1.0, output_file="large_files.txt")