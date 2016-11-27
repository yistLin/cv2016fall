#!/usr/local/bin/python3.5
import sys
from PIL import Image

infilename = sys.argv[1]
outfilename = sys.argv[2]

in_img = Image.open(infilename)
out_img = Image.new('L', in_img.size)

# define basic settings
width, height = in_img.size
BLACK = 0
WHITE = 255

mask_2d = [\
    (-1,-2),(0,-2),(1,-2),\
    (-2,-1),(-1,-1),(0,-1),(1,-1),(2,-1),\
    (-2,0),(-1,0),(0,0),(1,0),(2,0),\
    (-2,1),(-1,1),(0,1),(1,1),(2,1),\
    (-1,2),(0,2),(1,2)\
]

# get 1D image data
data_seq = list(in_img.getdata())
tmp_data = [0] * len(data_seq)
out_data = [0] * len(data_seq)

for y in range(height):
    for x in range(width):
        if data_seq[y * width + x] == WHITE:
            for m in mask_2d:
                p = (x + m[0], y + m[1])
                if p[0] < 0 or p[0] >= width or p[1] < 0 or p[1] >= height:
                    break
                elif data_seq[p[1] * width + p[0]] != WHITE:
                    break
            else:
                tmp_data[y * width + x] = WHITE

for y in range(height):
    for x in range(width):
        if tmp_data[y * width + x] == WHITE:
            for m in mask_2d:
                p = (x + m[0], y + m[1])
                if 0 <= p[0] < width and 0 <= p[1] < height:
                    out_data[p[1] * width + p[0]] = WHITE

# save output image
out_img.putdata(out_data)
out_img.save(outfilename, 'bmp')
