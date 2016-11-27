import os, sys
from PIL import Image

# get input image name
infilename = sys.argv[1]
outfilename = sys.argv[2]

# create input and output image objects
inImg = Image.open(infilename)
outImg = Image.new(inImg.mode, inImg.size)

# get data sequence from input image
data_seq = list(inImg.getdata())

# copy data sequence into output sequence
res_data = data_seq[:]

width, height = inImg.size
for y in range(height):
    for x in range(width):
        res_data[y * width + x] = data_seq[(height-y-1) * width + x]

# put result data sequence input output image and save
outImg.putdata(res_data)
outImg.save(outfilename)

