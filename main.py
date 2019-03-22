#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Li Haozheng
# @Time    : 2019/3/22 16:23

from PIL import Image
from urllib.request import urlretrieve
import os
from setting import *

#网络图片
class pic2str():
    def get_img(self):
        if PICTURE_PATH[:4] == 'http':
            urlretrieve(PICTURE_PATH, 'cache/cache.jpg')
            self.img_path = 'cache/cache.jpg'
        else:
            self.img_path = PICTURE_PATH

    def get_char(self,r,g,b,alpha=255):
        ascii_char = list(r"@$B%&W%M#*XhkbdpqwmZO0QLCJUYoazcvunxrjft/|()1{}[[-_+~<>i!lI;:,^`'.  ")
        if alpha == 0:
            return ' '
        length = len(ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

        unit = (256.0 + 1)/length
        return ascii_char[int(gray/unit)]

    def normalMode(self):

        self.get_img()
        im = Image.open(self.img_path)
        # im=im.convert('1')
        # im=im.convert('RGB')
        im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
        txt = ""
        for i in range(HEIGHT):
            for j in range(WIDTH):
                txt += self.get_char(*im.getpixel((j, i)))
            txt = txt + '\\n\\\n'
        print(txt)

    def colorfulMode(self):
        print(1)

    def mixMode(self):
        print(1)

    def main(self):
        model_dict = {
            'ColorfulMode':self.colorfulMode,
            'NormalMode':self.normalMode,
            'MixMode':self.mixMode
        }
        model_dict[MODEL]()


if __name__=='__main__':

    pic2str().main()