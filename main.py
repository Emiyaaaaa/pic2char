#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Li Haozheng
# @Time    : 2019/3/22 16:23

from PIL import Image
from urllib.request import urlretrieve
from setting import *

class pic2str():

    def get_img(self):
        if PICTURE_PATH[:4] == 'http':
            urlretrieve(PICTURE_PATH, 'cache/cache.jpg')
            self.img_path = 'cache/cache.jpg'
        else:
            self.img_path = PICTURE_PATH
        try:
            self.width = WIDTH
        except:
            im = Image.open(self.img_path)
            self.width = int(HEIGHT * im.size[0]/im.size[1]*2.14)
        finally:
            self.height = HEIGHT

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
        im = im.resize((self.width, self.height), Image.NEAREST)
        txt = 'function console_out(){console.log("'
        for i in range(self.height):
            for j in range(self.width):
                txt += self.get_char(*im.getpixel((j, i)))
            txt = txt + '\\n\\\n'
        txt += '");}'
        with open('console_out.js', 'w') as f:
            f.write(txt)

    def colorfulMode(self):

        self.get_img()
        im = Image.open(self.img_path)
        im = im.resize((self.width, self.height), Image.NEAREST)
        q_txt = '\\n\\\n'
        css_txt = ''
        try:
            font_size = str(ColorfulModeFontSize) + 'px;'
        except:
            font_size = ''
        for i in range(self.height):
            for j in range(self.width):
                css_txt += ',"background-color:white;'+font_size+'color:rgb'+str(im.getpixel((j, i)))+'"'
                q_txt += "%c"+ColorfulModeChar
            q_txt = q_txt + '\\n\\\n'
        txt = 'function console_out(){console.log('+'"'+q_txt+'"'+css_txt+');}'
        with open('console_out.js', 'w') as f:
            f.write(txt)

    def main(self):

        model_dict = {
            'ColorfulMode':self.colorfulMode,
            'NormalMode':self.normalMode
        }
        model_dict[MODEL]()

if __name__=='__main__':
    pic2str().main()