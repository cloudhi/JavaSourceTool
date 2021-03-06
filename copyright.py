__author__ = 'Yoojia.Chen@gmail.com'
# -*- coding: utf-8 -*-
import os
import sys


# 插入版本信息
def insert_copyright(java_file, my_copyright):
    f = open(java_file, 'r')
    contents = f.readlines()
    f.close()
    contents.insert(0, my_copyright)
    f = open(java_file, 'w')
    contents = ''.join(contents)
    f.write(contents)
    f.close()


# 判断Java文件的版本信息是否匹配
def find_copyright(java_file, my_copyright):
    f = open(java_file)
    cr_buf = []
    # 获取 package 之前的代码
    while True:
        line = f.readline()
        if not line:
            break
        if not line.startswith('package'):
            cr_buf.append(line)
        else:
            break
    f.close()
    content = ''.join(cr_buf)
    copyright_exists = len(cr_buf) != 0
    return (
        # Exists
        copyright_exists,
        # Matched
        copyright_exists and my_copyright in ''.join(cr_buf),
        # Content
        content
    )


# 处理版权信息
def perform_copyright(java_file, my_copyright):
    rs = find_copyright(java_file, my_copyright)
    # Copyright exists and matched
    if rs[1]:
        print "- 此Java源文件已存在版权声明"
        pass
    # Not exists, insert into java file
    elif not rs[0]:
        print '+ 添加版权声明到此Java源文件: %s' % java_file
        insert_copyright(java_file, my_copyright)
    # Exists , but not matched
    else:
        print '> 此Java源文件已存在其它版本信息: %s' % java_file


# 遍历Java源文件目录
def walk(java_path):
    if not os.path.isfile('COPYRIGHT_TEXT.txt'):
        print '- COPYRIGHT_TEXT.txt is Required !'

    cr_f = open('COPYRIGHT_TEXT.txt', 'r')
    my_copyright = ''.join(cr_f.readlines())
    cr_f.close()
    print "---- Using Copyright ----"
    print my_copyright
    print '-------------------------'
    print '> Java Source path: %s' % java_path
    for dir_path, _, names in os.walk(java_path):
        for name in names:
            if not name.endswith('.java'):
                continue
            java_file = dir_path + os.sep + name
            perform_copyright(java_file, my_copyright)


# 主入口
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print """
        Usage:
          $ python copyright.py 'your-java-source-root-patch'
        """
    else:
        walk(sys.argv[1])
