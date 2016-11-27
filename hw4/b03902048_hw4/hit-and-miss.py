#!/usr/local/bin/python3.5
import sys
from PIL import Image, ImageDraw

infilename = sys.argv[1]
outfilename = sys.argv[2]

in_img = Image.open(infilename)
out_img = Image.new('L', in_img.size)

# define basic settings
width, height = in_img.size
BLACK = 0
WHITE = 255

mask_pos = [\
    (-1,-1),(0,-1),(1,-1),\
    (-1,0),(0,0),(1,0),\
    (-1,1),(0,1),(1,1)]

mask = [\
    0,-1,-1,\
    1,1,-1,\
    0,1,0]

# get 1D image data
data_seq = list(in_img.getdata())
out_img.putdata([0] * len(data_seq))
draw = ImageDraw.Draw(out_img)

for y in range(height):
    for x in range(width):
        if data_seq[y*width+x] == WHITE:
            for i in range(len(mask_pos)):
                p = (x + mask_pos[i][0], y + mask_pos[i][1])
                if 0 <= p[0] < width and 0 <= p[1] < height:
                    if mask[i] == 1 and data_seq[p[1]*width+p[0]] == WHITE:
                        continue
                    elif mask[i] == -1 and data_seq[p[1]*width+p[0]] == BLACK:
                        continue
                    elif mask[i] == 0:
                        continue
                    else:
                        break
            else:
                draw.point((x,y), fill=255)

# save output image
del draw
out_img.save(outfilename, 'bmp')
