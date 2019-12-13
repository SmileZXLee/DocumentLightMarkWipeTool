#coding=utf-8
__author__ = 'zxlee'
__github__ = 'https://github.com/SmileZXLee/DocumentLightMarkWipeTool'

import os
from PIL import Image
import numpy as np
import imghdr
import platform
import sys

#是否是Windows
os_is_windows = platform.system() == 'Windows'

#根据系统获取raw_input中文编码结果
def gbk_encode(str):
	if os_is_windows:
		return str.decode('utf-8').encode('gbk')
	else:
		return str

#main
def main():
    print(u'欢迎使用DocumentLightMarkWipeTool！')
    while True:
        input_dir = getInputPath().strip()
        output_dir = getOutputPath().strip()
        if os.path.exists(input_dir) and os.path.isdir(output_dir):
            break
        else:
            print(u'文件/文件夹不存在或不合法，请重新选择！')
    
    visitDirFiles(input_dir,output_dir,input_dir)
    print(u'完成！所有图片已保存至路径' + output_dir)

#获取输入路径
def getInputPath():
    return raw_input(gbk_encode('请输入或拖动需要处理的文件/文件夹到此处(若为文件夹，将递归文件夹内的所有图片文件)：')).decode(sys.stdin.encoding)

# 获取输出路径
def getOutputPath():
    return raw_input(gbk_encode('请输入导出路径或拖动导出的目标文件夹到此处：')).decode(sys.stdin.encoding)

#递归访问文件/文件夹
def visitDirFiles(org_input_dir,org_output_dir,recursion_dir):
    single_file = False
    if os.path.isdir(recursion_dir):
        dir_list = os.listdir(recursion_dir)
    else:
        dir_list = [recursion_dir]
        single_file = True
    for i in range(0,len(dir_list)):
        path = os.path.join(recursion_dir,dir_list[i])
        if os.path.isdir(path):
            visitDirFiles(org_input_dir,org_output_dir,path)
        else:
            if imghdr.what(path):
                abs_output_dir = org_output_dir + recursion_dir[len(org_input_dir):]
                target_path = os.path.join(abs_output_dir,dir_list[i])
                if single_file:
                    target_path = os.path.join(org_output_dir,os.path.basename(dir_list[i]))
                target_dirname = os.path.dirname(target_path) 
                if not os.path.exists(target_dirname):
                    mkdir(target_dirname)
                img_deal(path,target_path)

#创建文件夹
def mkdir(path):
    path = path.strip().rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        return True
    else:
        return False

#图片处理
def img_deal(img_path,save_path):
    img = Image.open(img_path)
    img = levelsDeal(img,108,164)
    img_res = Image.fromarray(img.astype('uint8'))
    print(u'图片[' + img_path + u']处理完毕')
    img_res.save(save_path)

#色阶处理
def levelsDeal(img, black,white):
    if white > 255:
        white = 255
    if black < 0:
        black = 0
    if black >= white:
        black = white - 2
    img_array = np.array(img, dtype = int)
    cRate = -(white - black) /255.0 * 0.05
    rgb_diff = img_array - black
    rgb_diff = np.maximum(rgb_diff, 0)
    img_array = rgb_diff * cRate
    img_array = np.around(img_array, 0)
    img_array = img_array.astype(int)
    return img_array

if __name__ == '__main__':
    main()

