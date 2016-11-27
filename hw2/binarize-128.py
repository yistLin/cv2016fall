#!/usr/local/bin/python3.5
import sys
from PIL import Image

infilename = sys.argv[1]
outfilename = sys.argv[2]

inImg = Image.open(infilename)
outImg = Image.new(inImg.mode, inImg.size)

data_seq = list(inImg.getdata())

out_data = data_seq[:]

width, height = inImg.size
for x in range(height * width):
    out_data[x] = 255 if data_seq[x] > 127 else 0

outImg.putdata(out_data)
outImg.save(outfilename)

