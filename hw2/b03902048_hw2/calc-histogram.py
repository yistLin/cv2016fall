#!/usr/bin/python2.7
# to calculate the histogram of lena.bmp

import sys
from PIL import Image
import matplotlib.pyplot as plt

infilename = sys.argv[1]

inImg = Image.open(infilename)

data_seq = list(inImg.getdata())

histogram_lst = [0 for _ in range(255)]

width, height = inImg.size
for x in range(height * width):
    histogram_lst[ data_seq[x] ] += 1

print histogram_lst

# plt.hist(data_seq, bins=50, color='blue')
# plt.plot(histogram_lst)
plt.bar(range(0,255), histogram_lst)
plt.title("Lena Intensity Histogram")
plt.xlabel("Intensity")
plt.ylabel("Count")
plt.show()

