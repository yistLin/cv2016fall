#!/usr/local/bin/python3.5
import sys
from PIL import Image

kernel = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]

def binarize(data):
    result = []
    for p in data:
        result.append(1 if p > 127 else 0)
    return result

def downsampling(data, hei, wid):
    result = []
    offset = 8
    for y in range(0, hei, offset):
        for x in range(0, wid, offset):
            result.append(data[y * wid + x])
    return (result, int(hei/offset), int(wid/offset))

def expand(data, hei, wid):
    result = []
    result += [0] * (wid+2)

    offset = 0
    for h in range(hei):
        result += [0] + data[offset : offset+wid] + [0]
        offset += wid
    
    result += [0] * (wid+2)
    return (result, hei+2, wid+2)

def markIB(data, hei, wid):
    result = [0] * len(data)
    for y in range(1, hei-1):
        for x in range(1, wid-1):
            curr = y * wid + x
            count = 0
            if data[curr]:
                count += data[curr-1] + data[curr+1]
                count += data[curr-wid-1] + data[curr-wid] + data[curr-wid+1]
                count += data[curr+wid-1] + data[curr+wid] + data[curr+wid+1]
                if count < 8:
                    result[curr] = 255
                elif count == 8:
                    result[curr] = 2
    return result

def thinning(data, hei, wid):
    # expand the border of image
    exp_data, exp_hei, exp_wid = expand(data, hei, wid)

    # mark border(1) and interior(2)
    marked = markIB(exp_data, exp_hei, exp_wid)

    outimg = Image.new('L', (exp_wid, exp_hei))
    outimg.putdata(marked)
    outimg.save('temp.bmp', 'bmp')

    result = []
    return result

def main():
    # initial setup
    try:
        infilename = sys.argv[1]
        outfilename = sys.argv[2]
    except Exception as e:
        print('usage: ./thinning.py [input file] [output file]')
        print('Error:', str(e))
        exit(1)

    # get input image
    try:
        img = Image.open(infilename)
    except Exception as e:
        print('Error:', str(e))
        exit(1)

    wid, hei = img.size

    # get 1D image data
    pixellist = list(img.getdata())

    # binarize the image
    data = binarize(pixellist)

    # downsampling the image
    data, hei, wid = downsampling(data, hei, wid)

    # thinning the image
    data = thinning(data, hei, wid)

if __name__ == '__main__':
    main()
