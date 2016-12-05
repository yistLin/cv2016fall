#!/usr/local/bin/python3.5
import sys
import getopt
from itertools import product
from statistics import median
from PIL import Image

kernel = [\
    (-1,-2),(0,-2),(1,-2),\
    (-2,-1),(-1,-1),(0,-1),(1,-1),(2,-1),\
    (-2,0),(-1,0),(0,0),(1,0),(2,0),\
    (-2,1),(-1,1),(0,1),(1,1),(2,1),\
    (-1,2),(0,2),(1,2)]

def box_filter3x3(data, hei, wid):
    ret = []
    for y in range(hei):
        for x in range(wid):
            s = 0
            t = 0
            for off_x, off_y in product(range(-1,2), range(-1,2)):
                kx, ky = x + off_x, y + off_y
                if 0 <= kx < wid and 0 <= ky < hei:
                    s += data[ky * wid + kx]
                    t += 1
            ret.append(s / t)
    return ret

def box_filter5x5(data, hei, wid):
    ret = []
    for y in range(hei):
        for x in range(wid):
            s = 0
            t = 0
            for off_x, off_y in product(range(-2,3), range(-2,3)):
                kx, ky = x + off_x, y + off_y
                if 0 <= kx < wid and 0 <= ky < hei:
                    s += data[ky * wid + kx]
                    t += 1
            ret.append(s / t)
    return ret

def median_filter3x3(data, hei, wid):
    ret = []
    for y in range(hei):
        for x in range(wid):
            l = []
            for off_x, off_y in product(range(-1,2), range(-1,2)):
                kx, ky = x + off_x, y + off_y
                if 0 <= kx < wid and 0 <= ky < hei:
                    l.append(data[ky * wid + kx])
            ret.append(median(l))
    return ret

def median_filter5x5(data, hei, wid):
    ret = []
    for y in range(hei):
        for x in range(wid):
            l = []
            for off_x, off_y in product(range(-2,3), range(-2,3)):
                kx, ky = x + off_x, y + off_y
                if 0 <= kx < wid and 0 <= ky < hei:
                    l.append(data[ky * wid + kx])
            ret.append(median(l))
    return ret

def erosion(data, hei, wid):
    global kernel
    result = [0] * len(data)
    for y in range(hei):
        for x in range(wid):
            translated = []
            for x_k, y_k in kernel:
                x_t = x + x_k
                y_t = y + y_k
                if 0 <= x_t < wid and 0 <= y_t < hei:
                    translated.append(data[y_t * wid + x_t])
                else:
                    pass
            result[y * wid + x] = min(translated)
    return result

def dilation(data, hei, wid):
    global kernel
    result = [0] * len(data)
    for y in range(hei):
        for x in range(wid):
            translated = []
            for x_k, y_k in kernel:
                x_t = x + x_k
                y_t = y + y_k
                if 0 <= x_t < wid and 0 <= y_t < hei:
                    translated.append(data[y_t * wid + x_t])
                else:
                    pass
            result[y * wid + x] = max(translated)
    return result

def opening(data, hei, wid):
    return dilation( erosion(data, hei, wid), hei, wid )

def closing(data, hei, wid):
    return erosion( dilation(data, hei, wid), hei, wid )

def main(noise_filter, infilename):
    # get input image
    try:
        img = Image.open(infilename)
        wid, hei = img.size
    except Exception as e:
        print('Error:', str(e))
        sys.exit(1)

    # get 1D image data
    pixellist = list(img.getdata())

    # choose noise filter
    if noise_filter == 'box':
        data = box_filter3x3(pixellist, hei, wid)
        out_img = Image.new('L', img.size)
        out_img.putdata(data)
        out_img.save('box-filter3x3-' + infilename, 'bmp')
        
        data = box_filter5x5(pixellist, hei, wid)
        out_img = Image.new('L', img.size)
        out_img.putdata(data)
        out_img.save('box-filter5x5-' + infilename, 'bmp')

    elif noise_filter == 'median':
        data = median_filter3x3(pixellist, hei, wid)
        out_img = Image.new('L', img.size)
        out_img.putdata(data)
        out_img.save('median-filter3x3-' + infilename, 'bmp')

        data = median_filter5x5(pixellist, hei, wid)
        out_img = Image.new('L', img.size)
        out_img.putdata(data)
        out_img.save('median-filter5x5-' + infilename, 'bmp')

    elif noise_filter == 'opening_closing':
        data = opening(pixellist, hei, wid)
        data = closing(data, hei, wid)
        out_img = Image.new('L', img.size)
        out_img.putdata(data)
        out_img.save('opening-closing-' + infilename, 'bmp')

    elif noise_filter == 'closing_opening':
        data = closing(pixellist, hei, wid)
        data = opening(data, hei, wid)
        out_img = Image.new('L', img.size)
        out_img.putdata(data)
        out_img.save('closing-opening-' + infilename, 'bmp')

    else:
        print('Error: no such noise filter')
        sys.exit(1)

def usage():
    print('usage: ./thinning.py --filter=[filter] [input file]')

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["help", "filter="]);
        infilename = args[0]
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit(1);
            elif opt in ("--filter"):
                noise_filter = arg
    except getopt.GetoptError:
        print("getopt error!")
        usage()
        sys.exit(1);
    except Exception as e:
        print('Error:', str(e))
        usage()
        sys.exit(1)

    main(noise_filter, infilename)
