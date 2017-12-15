#!/bin/bash

## 说明：
## 	本脚本用于自动计算数据库最终存储根路径下各叶子文件夹中的录音文件集的数目。
## 参数：
##    wavdir: 指定数据库存放的根路径
## 输出格式：
##   以手机标识“Apple_Iphone5S-W”、“Apple_Iphone5S-Z”为例
## Apple_Iphone5S-W
##   Cn
##    L : 720
##    Z : 720
##    W : 720
##   Eng
##    L : 720
##    Z : 720
##    W : 720
## Apple_Iphone5S-Z
##   Cn
##    L : 720
##    Z : 720
##    W : 720
##   Eng
##    L : 720
##    Z : 720
##    W : 720
##其他:
##  Created on Sat Jun 24 17:09:44 2017
##	@author: Zhang Xue，South China University Of Technology

brandlist="Apple_Iphone5S-W  Apple_Iphone5S-Z  Apple_Iphone6S  Apple_Iphone7  HuaWei_G7-UL20  HuaWei_KIW-AL10  HuaWei_NT7-TL00 LeShi_L2  MeiZu_M1-Note  MeiZu_M2  MeiZu_M2-Note  MeiZu_MX5  Nobia_NX513J  Nobia_Z11  Vivio_X7  Vivio_Y622  XiaoMi4-C XiaoMi4-W XiaoMi5" #手机标识
langlist="Cn Eng" #语言类型
sprlist="L Z W" #录制人员标识
wavdir="/media/zzpp220/Entertaminment1/MobileData_Zx" #最终存放数据库根路径 "/media/zzpp220/Entertaminment1/Mobile_Zx"
for brand in  $brandlist
do
     echo " "$brand 
     for lang in $langlist
     do
        echo "   "$lang
        for spr in $sprlist
        do
             
            echo "    "$spr \: `find "$wavdir/$brand/$lang/$spr/" -name "*.wav" |wc -l`
        done 
done
done
