#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Li Haozheng
# @Time    : 2019/3/22 16:23

from PIL import Image
from urllib.request import urlretrieve
from setting import *

class pic2str():

    def get_img(self):
        # 下载图片
        if PICTURE_PATH[:4] == 'http':
            urlretrieve(PICTURE_PATH, 'cache/cache.jpg')
            self.img_path = 'cache/cache.jpg'
        else:
            self.img_path = PICTURE_PATH
        self.setWidth()
        self.height = HEIGHT

    def get_char(self,r,g,b,alpha=255):
        ascii_char = list(r"@$B%&W%M#*XhkbdpqwmZO0QLCJUYoazcvunxrjft/|()1{}[[-_+~<>i!lI;:,^`'.  ")
        if alpha == 0:
            return ' '
        length = len(ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        unit = (256.0 + 1)/length
        return ascii_char[int(gray/unit)]

    # 黑白模式
    def grayMode(self):
        self.get_img()
        im = Image.open(self.img_path)
        im = im.resize((self.width, self.height), Image.NEAREST)
        txt = 'function grayModeConsoleOut(){console.log("\\n\\\n'
        for i in range(self.height):
            for j in range(self.width):
                txt += self.get_char(*im.getpixel((j, i)))
            txt = txt + '\\n\\\n'
        txt += '");}\
                grayModeConsoleOut();'
        if OUTPUT_PATH:
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                f.write(txt)
        else:
            with open('grayModeConsole.js', 'w', encoding='utf-8') as f:
                f.write(txt)

    # 彩色模式
    def colorMode(self):
        self.get_img()
        im = Image.open(self.img_path)
        im = im.resize((self.width, self.height), Image.NEAREST)# 按给定宽高像素缩小图片
        txt = ColorModeChar
        q_txt = '\\n\\\n'
        css_txt = ''
        char_num = self.height * self.width
        try:
            font_size = 'font-size:' + str(ColorModeFontSize) + 'px;'
        except:
            font_size = ''

        backgroundColor = self.color16toRgb(BackgroundColor)

        for i in range(self.height):
            for j in range(self.width):
                pixel = str(im.getpixel((j, i)))# 获取像素值
                # print(backgroundColor,pixel)
                css_txt += ',"background-color:rgb'+backgroundColor+';'+font_size+'color:rgb'+pixel+'"'
                if self.isEquality(backgroundColor,pixel):# 与背景色相同或者rgb加起来差距在10以内的就用随便什么字符代替，不能占用txt中的字符（因为必须和txt中的文本相同大小，所以就选取了txt[0]）
                    q_txt += "%c"+txt[0]
                else:
                    q_txt += "%c"+txt[0]# 取txt第一个字母
                    txt = txt[1:] + txt[0]# 用完就把第一个字母放在最后, 相当于一个队列
            q_txt = q_txt + '\\n\\\n'
        txt = 'function colorModeConsoleOut(){\
                    console.log("'+q_txt+'"'+css_txt+');\
                    console.log("Make this: https://github.com/Emiyaaaaa/pic2char");\
                }\
                colorModeConsoleOut();'
        if OUTPUT_PATH:
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                f.write(txt)
        else:
            with open('colorModeConsole.js', 'w', encoding='utf-8') as f:
                f.write(txt)

    def color16toRgb(self,color16):
        color16 = color16[1:]
        r = int('0x'+color16[0:2], 16)
        g = int('0x'+color16[2:4], 16)
        b = int('0x'+color16[4:6], 16)
        rgb = '(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'
        return rgb

    def isEquality(self,rgb1,rgb2):
        rgb1sum = self.getRgbSum(rgb1)
        rgb2sum = self.getRgbSum(rgb2)
        if rgb1sum - rgb2sum < 10 and rgb1sum - rgb2sum > -10:
            return True
        else:
            return False

    def getRgbSum(self,rgb):
        rgb = rgb[1:-1].split(',')
        r_num = int(rgb[0])
        g_num = int(rgb[1])
        b_num = int(rgb[2])
        return r_num+g_num+b_num

    def is_all_chinese(self, strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    def setWidth(self):
        try:
            if WIDTH:
                self.width = WIDTH
        except:
            try:# 获取字号
                if ColorModeFontSize < 12:
                    fontSizeCoefficient = 12/ColorModeFontSize
                else:
                    fontSizeCoefficient = 1
            except:
                fontSizeCoefficient = 1
            im = Image.open(self.img_path)
            self.width = int(HEIGHT * im.size[0]/im.size[1]*fontSizeCoefficient*2.2)# 2.2为标准英文宽高比，fontSizeCoefficient 为字号小于12时的调整系数
            if self.is_all_chinese(ColorModeChar):# 中文
                self.width = int(HEIGHT * im.size[0]/im.size[1]*fontSizeCoefficient*1.18)


    def main(self):

        model_dict = {
            'ColorMode':self.colorMode,
            'GrayMode':self.grayMode
        }
        model_dict[MODEL]()

if __name__=='__main__':
    pic2str().main()