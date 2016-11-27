#!/usr/local/bin/python3.5
import sys
from PIL import Image, ImageOps

infilename = sys.argv[1]
outfilename = sys.argv[2]

in_img = Image.open(infilename)
out_img = ImageOps.grayscale(in_img).convert('L')

out_img.save(outfilename, 'bmp')

