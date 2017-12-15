#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
   本脚本主要基于命令行工具“ffmeg”对音频文件进行切割操作。实现批量将格式统一后的完整录音文件自动且等长分割为若干片段，
并按既定规范(详见："Docs/标注规范.pdf")批量进行标注，最后批量存储到对应目标文件夹中。
exp:ffmpeg -y -i white.wav -codec: copy -ss 0 -t 5 cutWhite.wav
参数：
    srcD ：     指定要进行切割的完整录音的存放源路径；
	split:      判断是否要进行切割操作，默认为“True”；
	splitsize： 指定切割后每个文件的时长，以秒为单位。默认值为5s；
	fileType:   限定要切割的对象类型，使用默认值"wav"，用于判断并筛选出源路径下的WAV文件；
	targetD:    指定数据库的总目录（"MobileData_Zx"），具体某次切割后存放路径“spec_targetD”由targetD和该次切割的参数共同决定；
    prefix:     指定生成的每个录音片段名称的前缀，默认为""；
	workdir:    指定该脚本的工作目录，

使用方法：
   cd MobileData_Zx
   source CutAudioByTime_Second.py [-s srcD] [-d splitsize] [-t targetD] [-j prefix] python
   
生成结果：
    对应的具体存放路径下保存该次切割生成的录音片段集合，每个片段5s，大小约为160KB。
    切割过程中的输出保存在变量“workdir”下的“out.log”文件中。示例见“Docs/CutProcess.log”。
	
其他：
	Created on Mon Jun 19 12:51:38 2017
	@author: Zhang Xue，South China University Of Technology

"""

import string
import os
import time
import re
# import sys
import math
from optparse import OptionParser


def GetFileDuration(srcpath, name):  # 得到每个完整语音文件的时长
    (si, so, se) = os.popen3(
        'cd ' + options.workdir + ';rm -f ffm.txt ; bash -c "(ffmpeg -i ' + srcpath + '/' + name + ' >&  ffm.txt)"; grep Duration ffm.txt')
    t = so.readlines()
    reg = 'Duration\:\s(\d+)\:(\d+)\:([\d\.]+)'
    duration = 0  # second
    for line in t:
        result = re.compile(reg).findall(line)

        for c in result:
            print
            'split file to', options.splitsize, 'seconds, Duration:', c[0], 'h ', c[1], 'min ', c[2], 's '
            duration = int(c[0]) * 3600 + int(c[1]) * 60 + float(c[2])
            return duration


parser = OptionParser()

parser.add_option("-e", "--split", dest="split", action="store_true", help="split to multiple file with size",
                  default=True)
parser.add_option("-d", "--splitsize", dest="splitsize", action="store", help="split to multiple file with size",
                  default="5")  # Seconds
parser.add_option("-j", "--prefix", dest="prefix", action="store", help="target file name prefix", default="")
parser.add_option("-f", "--fileType", dest="fileType", action="store", help="", default="wav")

parser.add_option("-s", "--src", dest="srcD", action="store", help="source dir",
                  default="/media/zzpp220/Entertaminment1/From_Data_Disk/record_live/ku/ch/removed")
parser.add_option("-t", "--target", dest="targetD", action="store", help="target dir",
                  default="/media/zzpp220/Entertaminment1/Mobile_Zx/")
parser.add_option("-w", "--workdir", dest="workdir", action="store", help="work dir",
                  default="/media/zzpp220/Entertaminment1/From_Data_Disk/record_live")

(options, args) = parser.parse_args()

if options.srcD == None or options.srcD[0:1] == '-':
    print
    'srcD Err, quit'
    exit()
if options.targetD == None or options.targetD[0:1] == '-':
    print
    'targetD Err, quit'
    exit()
if options.fileType == None or options.fileType[0:1] == '-':
    print
    'fileType Err, quit'
    exit()
if options.workdir == None or options.workdir[0:1] == '-':
    print
    'workdir Err, quit'
    exit()

for name in os.listdir(options.srcD):
    totname = os.path.join(options.srcD, name)
    # 判断源文件中的当前文件是否为WAV文件，若不是，则输出错误警告并跳过循环体中的所有后续操作，开始判断下个文件，直到满足条件
    if '.' not in name or not name[name.rindex('.') + 1:] == options.fileType:
        print
        'Error！Not a wav-audio file.Would not execute split process'
        continue

    ######################################################################
    newname = name[0: name.rindex('.')]  # 提取完整录音的文件名：mob_langspr : "Apple_Iphone7_CnL"
    brandname = name[0: name.rindex('_')]  # 提取手机标识: "Apple_Iphone7"
    spkr = name[name.rindex('.') - 1]  # 提取录制人员标识："L"
    lang = name[name.rindex('_') + 1:name.rindex('.') - 1]  # 提取语言类型："Cn"
    ###########################################################################
    if os.path.isfile(totname):
        if options.split == True:  # 定义切割文件为小文件,不接受其他参数,进行转换
            duration = GetFileDuration(options.srcD, name)  # 得到每个完整语音文件的时长，单位：秒
            nameLength = int(math.log(int(duration / int(options.splitsize))) / math.log(10)) + 1  # 系列文件名长度
            his = int(duration / int(options.splitsize)) + 1
            for i in range(his):
                tmp = ''
                if duration > int(options.splitsize) * (i + 1):
                    tmp = options.splitsize.decode('utf-8')  # 选项“-t”的参数，表示每个文件时长，单位：秒
                else:
                    tmp = str(duration - int(options.splitsize) * i).decode('utf-8')
                t0 = time.time()
                spec_targetD = os.path.join(options.targetD, brandname, lang, spkr)
            cmd = 'bash -c "' + "cd " + options.workdir + ";(ffmpeg -y -i " + options.srcD + "/" + name + " -codec: copy -ss " + str(
                i * int(
                    options.splitsize)) + " -t " + tmp + "  " + spec_targetD + '/' + options.prefix + newname + '_' + string.replace(
                ('%' + str(nameLength) + 's') % str(i), ' ', '0') + "." + options.fileType + '>> output.log)"'  #
            t1 = time.time()
            print
            cmd
            print
            "total time used for " + name + " : " + str(t1 - t0) + "s"  # 打印一次切割的使用时间，单位：秒
            (si, so, se) = os.popen3(cmd)
            for line in se.readlines():  # 打印输出
                print
                line
            for line in so.readlines():  # 打印输出
                print
                line  # CutAudioIterly(duration,nameLength)
