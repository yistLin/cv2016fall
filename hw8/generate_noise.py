#!/usr/local/bin/python3.5
import sys
import random
from PIL import Image

def additive_white(data, amplitude):
    ret = []
    for pix in data:
        ret.append(pix + amplitude * random.gauss(0, 1))
    return ret

def salt_and_pepper(data, threshold):
    ret = []
    threshold = threshold / 2
    for pix in data:
        uni = random.uniform(0, 1)
        if uni < threshold:
            ret.append(0)
        elif uni > (1 - threshold):
            ret.append(255)
        else:
            ret.append(pix)
    return ret

def main():
    # initial setup
    try:
        infilename = sys.argv[1]
    except Exception as e:
        print('usage: ./thinning.py [input file]')
        print('Error:', str(e))
        exit(1)

    # get input image
    try:
        img = Image.open(infilename)
        wid, hei = img.size
    except Exception as e:
        print('Error:', str(e))
        exit(1)

    # get 1D image data
    pixellist = list(img.getdata())

    # generate additive white guassian noise with amplitude = 10
    data = additive_white(pixellist, 10)
    o_img = Image.new('L', img.size)
    o_img.putdata(data)
    o_img.save('additive-white-10-' + infilename, 'bmp')

    # generate additive white guassian noise with amplitude = 30
    data = additive_white(pixellist, 30)
    o_img = Image.new('L', img.size)
    o_img.putdata(data)
    o_img.save('additive-white-30-' + infilename, 'bmp')

    # generate salt-and-pepper noise with threshold = 0.05
    data = salt_and_pepper(pixellist, 0.05)
    o_img = Image.new('L', img.size)
    o_img.putdata(data)
    o_img.save('salt-and-pepper-0.05-' + infilename, 'bmp')

    # generate salt-and-pepper noise with threshold = 0.05
    data = salt_and_pepper(pixellist, 0.1)
    o_img = Image.new('L', img.size)
    o_img.putdata(data)
    o_img.save('salt-and-pepper-0.1-' + infilename, 'bmp')

if __name__ == '__main__':
    main()
