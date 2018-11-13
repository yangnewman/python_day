#!C:/Python27
#coding=utf-8
 
# from pytesser import *
from PIL import Image,ImageEnhance,ImageFilter
import os
import fnmatch
import re,time
 
import urllib, random

#import hashlib  
 
def getGray(image_file):
   tmpls=[]
   for h in range(0,  image_file.size[1]):#h
      for w in range(0, image_file.size[0]):#w
         tmpls.append( image_file.getpixel((w,h))  )
          
   return tmpls
 
def getAvg(ls):#获取平均灰度值
   return sum(ls)/len(ls)
 
def getMH(a,b):#比较100个字符有几个字符相同
   dist = 0
   for i in range(0,len(a)):
      if a[i]==b[i]:
         dist=dist+1
   return dist
 
def getImgHash(fne):
   image_file = Image.open(fne) # 打开
   image_file = image_file.resize((12, 12))#重置图片大小我12px X 12px
   image_file = image_file.convert("L")#转256灰度图
   Grayls = getGray(image_file)#灰度集合
   avg = getAvg(Grayls)#灰度平均值
   bitls = ''#接收获取0或1
   #除去变宽1px遍历像素
   for h in range(1,  image_file.size[1]-1):#h
      for w in range(1, image_file.size[0]-1):#w
         if image_file.getpixel((w,h))>=avg:#像素的值比较平均值 大于记为1 小于记为0
            bitls=bitls+'1'
         else:
            bitls=bitls+'0'
   return bitls
'''         
   m2 = hashlib.md5()   
   m2.update(bitls)
   print m2.hexdigest(),bitls
   return m2.hexdigest()
'''

def get_compare(filename1, filename2):

   a=getImgHash(filename1)#图片地址自行替换

   b=getImgHash(filename2)

   compare=getMH(a,b)
   return compare


def get_compare_loop():
    path = 'D:\\workcodes\\Crawler\\day06\\cut_image'
    list_pic = []
    for file in os.listdir(path):
        # print(file)
        pic = {}
        file01=getImgHash('./cut_image/{}'.format(file))
        pic[file] = file01
        list_pic.append(pic)
    return list_pic


def comp_pic():
   count = 0
   pics = get_compare_loop()
   print(len(pics))
   for pic1 in pics:
       if not pic1:
           pics.remove(pic1)
           continue
       flag = 0
       a = list(pic1.values())[0]
       print(pic1)
       for pic2 in pics:
           if not pic2:
               pics.remove(pic2)
               continue
           b = list(pic2.values())[0]
           compare = getMH(a, b)
           # print(pic2)
           key = list(pic2.keys())[0]
           if 88 <= compare and compare < 100:
                os.remove('./cut_image/{}'.format(key))
                pic2.clear()
                count += 1
                continue
           if compare == 100:
               flag += 1
               if flag >= 2:
                    os.remove('./cut_image/{}'.format(list(pic2.keys())[0]))
                    pic2.clear()
                    count += 1
       print(count)
   return count

# def get_filename():
#    path = 'D:\\workcodes\\Crawler\\day06\\cut_image'
#    for file in os.listdir(path):
#       print(file)

if __name__ == '__main__':
   count = comp_pic()
   print('删除了{}个文件'.format(count))
   # filename1 = './cut_image/image0108_6.png'
   # filename2 = './cut_image/image0107_3.png'
   # compare = get_compare(filename1, filename2)
   # print(compare)
   # os.remove('./cut_image/{}'.format('231.png'))
