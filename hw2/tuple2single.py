#!/usr/local/bin/python3.5
import sys
from PIL import Image

infilename = sys.argv[1]
outfilename = sys.argv[2]

inImg = Image.open(infilename)
outImg = Image.new("L", inImg.size)

data_seq = list(inImg.getdata())

out_data = []
for i in range(len(data_seq)):
    if data_seq[i][0] > 127 or data_seq[i][1] > 127 or data_seq[i][2] > 127:
        out_data.append(255)
    else:
        out_data.append(0)

outImg.putdata(out_data)
outImg.save(outfilename, 'bmp')

