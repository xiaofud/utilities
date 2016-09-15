#!/usr/bin/python3
# coding = utf-8
"""
统计代码行数
"""

import os

def get_path():
    """
    输入源文件路径
    """
    path = input("enter the root path(default current work dir):\n")
    if path.strip() == "":
        path = "."
    assert os.path.exists(path), "the path does't exist"
    assert os.path.isdir(path), "the path must be a dir"
    return path

def get_suffix():
    """
    输入源码文件的后缀, 输入以空行结尾
    """
    suffix_list = list()
    while True:
        suffix = input("input the suffix like cpp(end input by empty line)\n")
        suffix = suffix.strip()
        if suffix == "":
            break
        suffix_list.append(suffix)
    return suffix_list
        
def get_line_count(root_path, suffix_list):
    """
    得到 root_path 下， 拥有 suffix_list 里面后缀名的源码文件的代码行数量
    默认不统计空行
    """
    #assert len(suffix_list) > 0, "there must be some suffix"
    line_count = 0
    empty_line_count = 0
    for root, dirs, files in os.walk(root_path):
        for file in files:
            # print(os.path.abspath(file))
            # 匹配后缀名
            file_suffix = os.path.splitext(file)[1]
            file_suffix = file_suffix.strip('.')
            if file_suffix in suffix_list:
                # 读取该文件
                with open(os.path.join(root, file)) as f:
                    for line in f:
                        if line.strip() == "":
                            empty_line_count += 1
                        line_count += 1
    return line_count, empty_line_count

if __name__ == "__main__":
    lines, empty = get_line_count(get_path(), get_suffix())
    print("{}(with empty lines)\n{}(without)\n{}(empty)".format(lines, lines - empty, empty))
    
    
