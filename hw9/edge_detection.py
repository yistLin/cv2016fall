#!/usr/local/bin/python3.5
import sys
import getopt
from math import sqrt
from PIL import Image

def flip(p, boundary):
    if p < 0:
        return -p -1
    elif p >= boundary:
        return 2 * boundary - p - 1
    else:
        return p

def roberts_operator(data, hei, wid):
    r1 = [\
        ( 0, 0,-1),( 1, 0, 0),\
        ( 0, 1, 0),( 1, 1, 1)]
    r2 = [\
        ( 0, 0, 0),( 1, 0,-1),\
        ( 0, 1, 1),( 1, 1, 0)]
    ret = []
    for y in range(hei):
        for x in range(wid):
            r1val = 0
            for rx, ry, val in r1:
                px = flip(x + rx, wid)
                py = flip(y + ry, hei)
                r1val += data[py * wid + px] * val
            r2val = 0
            for rx, ry, val in r2:
                px = flip(x + rx, wid)
                py = flip(y + ry, hei)
                r2val += data[py * wid + px] * val
            val = sqrt(r1val ** 2 + r2val ** 2)
            ret.append(0 if val >= 12 else 255)
    return ret

def prewitt_operator(data, hei, wid):
    p1 = [\
        (-1,-1,-1),( 0,-1,-1),( 1,-1,-1),\
        (-1, 0, 0),( 0, 0, 0),( 1, 0, 0),\
        (-1, 1, 1),( 0, 1, 1),( 1, 1, 1)]
    p2 = [\
        (-1,-1,-1),( 0,-1, 0),( 1,-1, 1),\
        (-1, 0,-1),( 0, 0, 0),( 1, 0, 1),\
        (-1, 1,-1),( 0, 1, 0),( 1, 1, 1)]
    ret = []
    for y in range(hei):
        for x in range(wid):
            p1val = 0
            for rx, ry, val in p1:
                px = flip(x + rx, wid)
                py = flip(y + ry, hei)
                p1val += data[py * wid + px] * val
            p2val = 0
            for rx, ry, val in p2:
                px = flip(x + rx, wid)
                py = flip(y + ry, hei)
                p2val += data[py * wid + px] * val
            val = sqrt(p1val ** 2 + p2val ** 2)
            ret.append(0 if val >= 24 else 255)
    return ret

def sobel_operator(data, hei, wid):
    s1 = [\
        (-1,-1,-1),( 0,-1,-2),( 1,-1,-1),\
        (-1, 0, 0),( 0, 0, 0),( 1, 0, 0),\
        (-1, 1, 1),( 0, 1, 2),( 1, 1, 1)]
    s2 = [\
        (-1,-1,-1),( 0,-1, 0),( 1,-1, 1),\
        (-1, 0,-2),( 0, 0, 0),( 1, 0, 2),\
        (-1, 1,-1),( 0, 1, 0),( 1, 1, 1)]
    ret = []
    for y in range(hei):
        for x in range(wid):
            s1val = 0
            for rx, ry, val in s1:
                px = flip(x + rx, wid)
                py = flip(y + ry, hei)
                s1val += data[py * wid + px] * val
            s2val = 0
            for rx, ry, val in s2:
                px = flip(x + rx, wid)
                py = flip(y + ry, hei)
                s2val += data[py * wid + px] * val
            val = sqrt(s1val ** 2 + s2val ** 2)
            ret.append(0 if val >= 38 else 255)
    return ret

def frei_and_chen_operator(data, hei, wid):
    f1 = [\
        (-1,-1,-1),( 0,-1,-sqrt(2)),( 1,-1,-1),\
        (-1, 0, 0),( 0, 0,       0),( 1, 0, 0),\
        (-1, 1, 1),( 0, 1, sqrt(2)),( 1, 1, 1)]
    f2 = [\
        (-1,-1,      -1),( 0,-1, 0),( 1,-1,       1),\
        (-1, 0,-sqrt(2)),( 0, 0, 0),( 1, 0, sqrt(2)),\
        (-1, 1,      -1),( 0, 1, 0),( 1, 1,       1)]
    ret = []
    for y in range(hei):
        for x in range(wid):
            f1val = 0
            for rx, ry, val in f1:
                px = flip(x + rx, wid)
                py = flip(y + ry, hei)
                f1val += data[py * wid + px] * val
            f2val = 0
            for rx, ry, val in f2:
                px = flip(x + rx, wid)
                py = flip(y + ry, hei)
                f2val += data[py * wid + px] * val
            val = sqrt(f1val ** 2 + f2val ** 2)
            ret.append(0 if val >= 30 else 255)
    return ret

def kirsch_operator(data, hei, wid):
    k = [
        [\
        (-1,-1,-3),( 0,-1,-3),( 1,-1, 5),\
        (-1, 0,-3),( 0, 0, 0),( 1, 0, 5),\
        (-1, 1,-3),( 0, 1,-3),( 1, 1, 5)],\
        [\
        (-1,-1,-3),( 0,-1, 5),( 1,-1, 5),\
        (-1, 0,-3),( 0, 0, 0),( 1, 0, 5),\
        (-1, 1,-3),( 0, 1,-3),( 1, 1,-3)],\
        [\
        (-1,-1, 5),( 0,-1, 5),( 1,-1, 5),\
        (-1, 0,-3),( 0, 0, 0),( 1, 0,-3),\
        (-1, 1,-3),( 0, 1,-3),( 1, 1,-3)],\
        [\
        (-1,-1, 5),( 0,-1, 5),( 1,-1,-3),\
        (-1, 0, 5),( 0, 0, 0),( 1, 0,-3),\
        (-1, 1,-3),( 0, 1,-3),( 1, 1,-3)],\
        [\
        (-1,-1, 5),( 0,-1,-3),( 1,-1,-3),\
        (-1, 0, 5),( 0, 0, 0),( 1, 0,-3),\
        (-1, 1, 5),( 0, 1,-3),( 1, 1,-3)],\
        [\
        (-1,-1,-3),( 0,-1,-3),( 1,-1,-3),\
        (-1, 0, 5),( 0, 0, 0),( 1, 0,-3),\
        (-1, 1, 5),( 0, 1, 5),( 1, 1,-3)],\
        [\
        (-1,-1,-3),( 0,-1,-3),( 1,-1,-3),\
        (-1, 0,-3),( 0, 0, 0),( 1, 0,-3),\
        (-1, 1, 5),( 0, 1, 5),( 1, 1, 5)],\
        [\
        (-1,-1,-3),( 0,-1,-3),( 1,-1,-3),\
        (-1, 0,-3),( 0, 0, 0),( 1, 0, 5),\
        (-1, 1,-3),( 0, 1, 5),( 1, 1, 5)]\
    ]
    ret = []
    for y in range(hei):
        for x in range(wid):
            maxval = -float('Inf')
            for kernel in k:
                tmpval = 0
                for rx, ry, val in kernel:
                    px = flip(x + rx, wid)
                    py = flip(y + ry, hei)
                    tmpval += data[py * wid + px] * val
                maxval = tmpval if tmpval > maxval else maxval
            ret.append(0 if maxval >= 135 else 255)
    return ret

def robinson_operator(data, hei, wid):
    k = [
        [\
        (-1,-1,-1),( 0,-1, 0),( 1,-1, 1),\
        (-1, 0,-2),( 0, 0, 0),( 1, 0, 2),\
        (-1, 1,-1),( 0, 1, 0),( 1, 1, 1)],\
        [\
        (-1,-1, 0),( 0,-1, 1),( 1,-1, 2),\
        (-1, 0,-1),( 0, 0, 0),( 1, 0, 1),\
        (-1, 1,-2),( 0, 1,-1),( 1, 1, 0)],\
        [\
        (-1,-1, 1),( 0,-1, 2),( 1,-1, 1),\
        (-1, 0, 0),( 0, 0, 0),( 1, 0, 0),\
        (-1, 1,-1),( 0, 1,-2),( 1, 1,-1)],\
        [\
        (-1,-1, 2),( 0,-1, 1),( 1,-1, 0),\
        (-1, 0, 1),( 0, 0, 0),( 1, 0,-1),\
        (-1, 1, 0),( 0, 1,-1),( 1, 1,-2)],\
        [\
        (-1,-1, 1),( 0,-1, 0),( 1,-1,-1),\
        (-1, 0, 2),( 0, 0, 0),( 1, 0,-2),\
        (-1, 1, 1),( 0, 1, 0),( 1, 1,-1)],\
        [\
        (-1,-1, 0),( 0,-1,-1),( 1,-1,-2),\
        (-1, 0, 1),( 0, 0, 0),( 1, 0,-1),\
        (-1, 1, 2),( 0, 1, 1),( 1, 1, 0)],\
        [\
        (-1,-1,-1),( 0,-1,-2),( 1,-1,-1),\
        (-1, 0, 0),( 0, 0, 0),( 1, 0, 0),\
        (-1, 1, 1),( 0, 1, 2),( 1, 1, 1)],\
        [\
        (-1,-1,-2),( 0,-1,-1),( 1,-1, 0),\
        (-1, 0,-1),( 0, 0, 0),( 1, 0, 1),\
        (-1, 1, 0),( 0, 1, 1),( 1, 1, 2)]\
    ]
    ret = []
    for y in range(hei):
        for x in range(wid):
            maxval = -float('Inf')
            for kernel in k:
                tmpval = 0
                for rx, ry, val in kernel:
                    px = flip(x + rx, wid)
                    py = flip(y + ry, hei)
                    tmpval += data[py * wid + px] * val
                maxval = tmpval if tmpval > maxval else maxval
            ret.append(0 if maxval >= 43 else 255)
    return ret

def nevatia_babu_operator(data, hei, wid):
    k = [
        [\
        (-2,-2, 100),(-1,-2, 100),( 0,-2, 100),( 1,-2, 100),( 2,-2, 100),\
        (-2,-1, 100),(-1,-1, 100),( 0,-1, 100),( 1,-1, 100),( 2,-1, 100),\
        (-2, 0,   0),(-1, 0,   0),( 0, 0,   0),( 1, 0,   0),( 2, 0,   0),\
        (-2, 1,-100),(-1, 1,-100),( 0, 1,-100),( 1, 1,-100),( 2, 1,-100),\
        (-2, 2,-100),(-1, 2,-100),( 0, 2,-100),( 1, 2,-100),( 2, 2,-100)],\
        [\
        (-2,-2, 100),(-1,-2, 100),( 0,-2, 100),( 1,-2, 100),( 2,-2, 100),\
        (-2,-1, 100),(-1,-1, 100),( 0,-1, 100),( 1,-1,  78),( 2,-1, -32),\
        (-2, 0, 100),(-1, 0,  92),( 0, 0,   0),( 1, 0, -92),( 2, 0,-100),\
        (-2, 1,  32),(-1, 1, -78),( 0, 1,-100),( 1, 1,-100),( 2, 1,-100),\
        (-2, 2,-100),(-1, 2,-100),( 0, 2,-100),( 1, 2,-100),( 2, 2,-100)],\
        [\
        (-2,-2, 100),(-1,-2, 100),( 0,-2, 100),( 1,-2,  32),( 2,-2,-100),\
        (-2,-1, 100),(-1,-1, 100),( 0,-1,  92),( 1,-1, -78),( 2,-1,-100),\
        (-2, 0, 100),(-1, 0, 100),( 0, 0,   0),( 1, 0,-100),( 2, 0,-100),\
        (-2, 1, 100),(-1, 1,  78),( 0, 1, -92),( 1, 1,-100),( 2, 1,-100),\
        (-2, 2, 100),(-1, 2, -32),( 0, 2,-100),( 1, 2,-100),( 2, 2,-100)],\
        [\
        (-2,-2,-100),(-1,-2,-100),( 0,-2,   0),( 1,-2, 100),( 2,-2, 100),\
        (-2,-1,-100),(-1,-1,-100),( 0,-1,   0),( 1,-1, 100),( 2,-1, 100),\
        (-2, 0,-100),(-1, 0,-100),( 0, 0,   0),( 1, 0, 100),( 2, 0, 100),\
        (-2, 1,-100),(-1, 1,-100),( 0, 1,   0),( 1, 1, 100),( 2, 1, 100),\
        (-2, 2,-100),(-1, 2,-100),( 0, 2,   0),( 1, 2, 100),( 2, 2, 100)],\
        [\
        (-2,-2,-100),(-1,-2,  32),( 0,-2, 100),( 1,-2, 100),( 2,-2, 100),\
        (-2,-1,-100),(-1,-1, -78),( 0,-1,  92),( 1,-1, 100),( 2,-1, 100),\
        (-2, 0,-100),(-1, 0,-100),( 0, 0,   0),( 1, 0, 100),( 2, 0, 100),\
        (-2, 1,-100),(-1, 1,-100),( 0, 1, -92),( 1, 1,  78),( 2, 1, 100),\
        (-2, 2,-100),(-1, 2,-100),( 0, 2,-100),( 1, 2, -32),( 2, 2, 100)],\
        [\
        (-2,-2, 100),(-1,-2, 100),( 0,-2, 100),( 1,-2, 100),( 2,-2, 100),\
        (-2,-1, -32),(-1,-1,  78),( 0,-1, 100),( 1,-1, 100),( 2,-1, 100),\
        (-2, 0,-100),(-1, 0, -92),( 0, 0,   0),( 1, 0,  92),( 2, 0, 100),\
        (-2, 1,-100),(-1, 1,-100),( 0, 1,-100),( 1, 1, -78),( 2, 1,  32),\
        (-2, 2,-100),(-1, 2,-100),( 0, 2,-100),( 1, 2,-100),( 2, 2,-100)]\
    ]
    ret = []
    for y in range(hei):
        for x in range(wid):
            maxval = -float('Inf')
            for kernel in k:
                tmpval = 0
                for rx, ry, val in kernel:
                    px = flip(x + rx, wid)
                    py = flip(y + ry, hei)
                    tmpval += data[py * wid + px] * val
                maxval = tmpval if tmpval > maxval else maxval
            ret.append(0 if maxval >= 12500 else 255)
    return ret

def main(operator, infilename):
    # get input image
    try:
        img = Image.open(infilename)
        wid, hei = img.size
    except Exception as e:
        print('Error:', str(e))
        sys.exit(1)

    # get 1D image data
    pixellist = list(img.getdata())

    # choose edge detection operator
    if operator == 'roberts':
        data = roberts_operator(pixellist, hei, wid)
    elif operator == 'prewitt':
        data = prewitt_operator(pixellist, hei, wid)
    elif operator == 'sobel':
        data = sobel_operator(pixellist, hei, wid)
    elif operator == 'frei_and_chen':
        data = frei_and_chen_operator(pixellist, hei, wid)
    elif operator == 'kirsch':
        data = kirsch_operator(pixellist, hei, wid)
    elif operator == 'robinson':
        data = robinson_operator(pixellist, hei, wid)
    elif operator == 'nevatia_babu':
        data = nevatia_babu_operator(pixellist, hei, wid)
    else:
        print('Error: no such operator')
        sys.exit(1)

    outfilename = operator + '-' + infilename
    out_img = Image.new('1', img.size)
    out_img.putdata(data)
    out_img.save(outfilename, 'bmp')

def usage():
    print('usage: ./edge_detection.py --operator=[operator] [input file]')

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["operator="]);
        infilename = args[0]
        for opt, arg in opts:
            if opt in ("--operator"):
                operator = arg
    except getopt.GetoptError:
        print("getopt error!")
        usage()
        sys.exit(1);
    except Exception as e:
        print('Error:', str(e))
        usage()
        sys.exit(1)

    main(operator, infilename)
