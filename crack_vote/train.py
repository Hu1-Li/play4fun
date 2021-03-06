#!/usr/bin/envpython
#-*-coding:UTF-8-*-
#图像二值处理
import os
from PIL import Image
j=1
dir="./pic/"
path="./font/"
for f in os.listdir(dir):
    if f.endswith(".jpg"):
        img=Image.open(dir+f)
        img=img.convert("RGBA")
        pixdata=img.load()
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x,y][0]<90:
                    pixdata[x,y]=(0,0,0,255)
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x,y][1]<136:
                    pixdata[x,y]=(0,0,0,255)
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if pixdata[x,y][2]>0:
                    pixdata[x,y]=(255,255,255,255)
        img.save(path+f,"JPEG")
