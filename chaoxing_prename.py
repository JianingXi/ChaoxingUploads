import os
from ChaoxingPrename.Xuexitong_01_html2pdf import convert_html_files_in_directory
from ChaoxingPrename.Xuexitong_02_ReplaceSymbol import rename_recursively
from ChaoxingPrename.Xuexitong_03_Rename_files_by_Content import rename_files_by_content
from ChaoxingPrename.Xuexitong_04_SplitDirWithin50Files import process_directory
from ChaoxingPrename.Xuexitong_05_FileFormat2RAR import file_format_to_rar, load_blacklist
from ChaoxingPrename.Xuexitong_06_RemoveEmptyDir import remove_empty_dirs
from ChaoxingPrename.Xuexitong_07_LargerThan1G import large_than_1g_files
from ChaoxingPrename.Xuexitong_08_FileExtensionPrint import count_file_extensions
from ChaoxingPrename.File_00_extract_all_archieve import extract_all_archive_dirs
from ChaoxingPrename.File_01_dir_merge_batch import dir_merge_batch

rename_by_content = 0
target_directory = r"G:\2023_学生竞赛"

if not os.path.isdir(target_directory):
    print("错误: 指定的路径不是一个有效的目录!")
    exit(1)

"""
old_string = "大礼包"
new_string = ""
# 去广告
rename_files_in_directory(target_directory, old_string, new_string)



extract_all_archive_dirs(target_directory)
"""

dir_merge_batch(target_directory)


convert_html_files_in_directory(target_directory)
rename_recursively(target_directory)
if rename_by_content:
    rename_files_by_content(target_directory)
process_directory(target_directory)


blacklist_file = r".\ChaoxingPrename\UploadList\blacklist.txt"
target_exts = load_blacklist(blacklist_file)
file_format_to_rar(target_directory, target_exts)
remove_empty_dirs(target_directory)

large_than_1g_files(target_directory, size_threshold_gb=1.0, output_file="large_files.txt")

whitelist_file = r".\ChaoxingPrename\UploadList\whitelist.txt"
output_file = r".\ChaoxingPrename\UploadList\Unknownlist.txt"
count_file_extensions(target_directory, whitelist_file, output_file)
