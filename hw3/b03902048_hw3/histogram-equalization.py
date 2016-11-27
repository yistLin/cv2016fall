#!/usr/bin/python2.7
# to do Histogram Equalization on lena.bmp

import sys
from PIL import Image
import matplotlib.pyplot as plt

class HistEqualization:
    def __init__(self, data, img_size):
        self.data = data
        self.img_size = img_size
        self.hist_lst = self.calc_histogram(data)
        self.cdf_lst = self.calc_cdf(self.hist_lst)

    # accumulate intensity to get histogram
    def calc_histogram(self, data):
        lst = [0] * 256
        for x in range(self.img_size):
            lst[ data[x] ] += 1
        return lst

    # from hist_lst, calculate CDF
    def calc_cdf(self, hist_lst):
        lst = [0] * 256
        for x in range(1,256):
            lst[x] = lst[x-1] + hist_lst[x]
        return lst
    
    def equalized(self):
        cdf_min = 0
        lst = [0] * self.img_size
        intensity = [0] * 256
        
        for x in range(256):
            if self.cdf_lst[x] > 0:
                cdf_min = self.cdf_lst[x]
                break
        
        for x in range(256):
            if self.cdf_lst[x] < cdf_min:
                intensity[x] = 0
            else:
                intensity[x] = int(round( (float(self.cdf_lst[x] - cdf_min) / float(self.img_size - cdf_min)) * 255.0 ))
        
        for x in range(self.img_size):
            lst[x] = intensity[ self.data[x] ]

        return lst

# read input image
infilename = sys.argv[1]
origin_img = Image.open(infilename)
data_seq = list(origin_img.getdata())

width, height = origin_img.size
img_size = width * height

# prepare output image
outfilename = sys.argv[2]
output_img = Image.new(origin_img.mode, origin_img.size)

he = HistEqualization(data_seq, img_size)

equalized_data = he.equalized()
output_img.putdata( equalized_data )
output_img.save(outfilename, 'bmp')

histogram_lst = [0] * 256
for i in range(img_size):
    histogram_lst[ equalized_data[i] ] += 1

plt.bar(range(0,256), histogram_lst)
plt.title("Lena Intensity Histogram (Equalized)")
plt.xlabel("Intensity")
plt.ylabel("Count")
plt.show()

