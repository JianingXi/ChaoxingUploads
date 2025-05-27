import os
from Xuexitong_01_html2pdf import convert_html_files_in_directory
from Xuexitong_02_ReplaceSymbol import rename_recursively
from Xuexitong_03_Rename_files_by_Content import rename_files_by_content
from Xuexitong_04_SplitDirWithin50Files import process_directory

rename_by_content = 0
target_directory = r"G:\作品\科普组"

if not os.path.isdir(target_directory):
    print("错误: 指定的路径不是一个有效的目录!")
    exit(1)

convert_html_files_in_directory(target_directory)
rename_recursively(target_directory)
if rename_by_content:
    rename_files_by_content(target_directory)
process_directory(target_directory)

