#!/usr/bin/python2.7
# to do Histogram Equalization on lena.bmp

import sys
from PIL import Image
import math

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


class HSVEqualization:
    def __init__(self, data, img_size):
        self.data = data
        self.img_size = img_size
        self.h_seq = []
        self.s_seq = []
        self.v_seq = []
        self.hsv_data = self.convert_hsv()
        self.s_hist = self.s_histogram()
        self.v_hist = self.v_histogram()
        self.s_cdf = self.calc_s_cdf()
        self.v_cdf = self.calc_v_cdf()

    def convert_hsv(self):
        for x in range(self.img_size):
            r, g, b = self.data[x]
            h, s, v = rgb2hsv(r, g, b)
            self.h_seq.append(h)
            self.s_seq.append(int(s * 100))
            self.v_seq.append(int(v * 100))

    def s_histogram(self):
        lst = [0] * 101
        for x in range(self.img_size):
            lst[ self.s_seq[x] ] += 1
        return lst

    def v_histogram(self):
        lst = [0] * 101
        for x in range(self.img_size):
            lst[ self.v_seq[x] ] += 1
        return lst

    def calc_s_cdf(self):
        lst = [0] * 101
        for x in range(1,101):
            lst[x] = lst[x-1] + self.s_hist[x]
        return lst

    def calc_v_cdf(self):
        lst = [0] * 101
        for x in range(1,101):
            lst[x] = lst[x-1] + self.v_hist[x]
        return lst

    def equalized(self):
        cdf_min = 0
        lst = []
        new_lightness = [0] * 101
        new_saturate = [0] * 101

        for x in range(101):
            new_lightness[x] = int(round( (float(self.v_cdf[x] - 1) / float(self.img_size - 1)) * 99 ))
            new_saturate[x] = int(round( (float(self.s_cdf[x] - 1) / float(self.img_size - 1)) * 99 ))

        for x in range(self.img_size):
            h, s, v = 0, 0, 0
            h = self.h_seq[x]
            s = new_saturate[ self.s_seq[x] ]
            v = new_lightness[ self.v_seq[x] ]
            r, g, b = hsv2rgb(h, float(s/100.0), float(v/100.0))
            lst.append((r,g,b))

        return lst

# read input image
infilename = sys.argv[1]
origin_img = Image.open(infilename)
data_seq = list(origin_img.getdata())

width, height = origin_img.size
img_size = width * height

# prepare output image
outfilename = sys.argv[2]
output_img = Image.new('RGB', origin_img.size)

he = HSVEqualization(data_seq, img_size)

equalized_data = he.equalized()
output_img.putdata( equalized_data )
output_img.save(outfilename, 'bmp')
