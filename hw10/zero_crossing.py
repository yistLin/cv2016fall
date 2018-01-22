#!/usr/local/bin/python3.5
import sys
import argparse
import numpy as np
from PIL import Image

def flip(p, boundary):
    if p < 0:
        return -p -1
    elif p >= boundary:
        return 2 * boundary - p - 1
    else:
        return p

def conv_runner(data, hei, wid, kernel, weight):
    ret = []
    for y in range(hei):
        for x in range(wid):
            s = 0
            for kx, ky, val in kernel:
                px = flip(x + kx, wid)
                py = flip(y + ky, hei)
                s += data[py * wid + px] * val
            ret.append(s * weight)
    return ret

def gaussian(x, mu, sig):
    return (1 / np.sqrt(2*np.power(sig,2)*np.pi) ) * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def gauss_2d(x, y, mu_x, mu_y, sig_x, sig_y):
    return gaussian(x, mu_x, sig_x) * gaussian(y, mu_y, sig_y)

def DOG(x, y):
    return gauss_2d(x, y, 0, 0, 1, 1) - gauss_2d(x, y, 0, 0, 3, 3)

def edge_detector(data, hei, wid, kernel, threshold):
    if kernel == 'laplacian':
        k = [\
            (-1,-1, 0),( 0,-1, 1),( 1,-1, 0),\
            (-1, 0, 1),( 0, 0,-4),( 1, 0, 1),\
            (-1, 1, 0),( 0, 1, 1),( 1, 1, 0)\
        ]
        weight = 1
    elif kernel == 'minimum-variance':
        k = [\
            (-1,-1, 2),( 0,-1,-1),( 1,-1, 2),\
            (-1, 0,-1),( 0, 0,-4),( 1, 0,-1),\
            (-1, 1, 2),( 0, 1,-1),( 1, 1, 2)\
        ]
        weight = 1/3
    elif kernel == 'LOG':
        k = [\
            (-5,-5, 0),(-4,-5, 0),(-3,-5,  0),(-2,-5, -1),(-1,-5, -1),( 0,-5, -2),( 1,-5, -1),( 2,-5, -1),( 3,-5,  0),( 4,-5, 0),( 5,-5, 0),\
            (-5,-4, 0),(-4,-4, 0),(-3,-4, -2),(-2,-4, -4),(-1,-4, -8),( 0,-4, -9),( 1,-4, -8),( 2,-4, -4),( 3,-4, -2),( 4,-4, 0),( 5,-4, 0),\
            (-5,-3, 0),(-4,-3,-2),(-3,-3, -7),(-2,-3,-15),(-1,-3,-22),( 0,-3,-23),( 1,-3,-22),( 2,-3,-15),( 3,-3, -7),( 4,-3,-2),( 5,-3, 0),\
            (-5,-2,-1),(-4,-2,-4),(-3,-2,-15),(-2,-2,-24),(-1,-2,-14),( 0,-2, -1),( 1,-2,-14),( 2,-2,-24),( 3,-2,-15),( 4,-2,-4),( 5,-2,-1),\
            (-5,-1,-1),(-4,-1,-8),(-3,-1,-22),(-2,-1,-14),(-1,-1, 52),( 0,-1,103),( 1,-1, 52),( 2,-1,-14),( 3,-1,-22),( 4,-1,-8),( 5,-1,-1),\
            (-5, 0,-2),(-4, 0,-9),(-3, 0,-23),(-2, 0, -1),(-1, 0,103),( 0, 0,178),( 1, 0,103),( 2, 0, -1),( 3, 0,-23),( 4, 0,-9),( 5, 0,-2),\
            (-5, 1,-1),(-4, 1,-8),(-3, 1,-22),(-2, 1,-14),(-1, 1, 52),( 0, 1,103),( 1, 1, 52),( 2, 1,-14),( 3, 1,-22),( 4, 1,-8),( 5, 1,-1),\
            (-5, 2,-1),(-4, 2,-4),(-3, 2,-15),(-2, 2,-24),(-1, 2,-14),( 0, 2, -1),( 1, 2,-14),( 2, 2,-24),( 3, 2,-15),( 4, 2,-4),( 5, 2,-1),\
            (-5, 3, 0),(-4, 3,-2),(-3, 3, -7),(-2, 3,-15),(-1, 3,-22),( 0, 3,-23),( 1, 3,-22),( 2, 3,-15),( 3, 3, -7),( 4, 3,-2),( 5, 3, 0),\
            (-5, 4, 0),(-4, 4, 0),(-3, 4, -2),(-2, 4, -4),(-1, 4, -8),( 0, 4, -9),( 1, 4, -8),( 2, 4, -4),( 3, 4, -2),( 4, 4, 0),( 5, 4, 0),\
            (-5, 5, 0),(-4, 5, 0),(-3, 5,  0),(-2, 5, -1),(-1, 5, -1),( 0, 5, -2),( 1, 5, -1),( 2, 5, -1),( 3, 5,  0),( 4, 5, 0),( 5, 5, 0)\
        ]
        weight = 1
    elif kernel == 'DOG':
        k = []
        for y in range(-5, 6):
            for x in range(-5, 6):
                k.append((x, y, DOG(x, y)))
                
        weight = 1
    else:
        print('Error: no such kernel.')
        sys.exit(1)

    neighbor = [\
        (-1,-1),( 0,-1),( 1,-1),\
        (-1, 0),( 0, 0),( 1, 0),\
        (-1, 1),( 0, 1),( 1, 1)\
    ]
    ret = []
    data = conv_runner(data, hei, wid, k, weight)
    for y in range(hei):
        for x in range(wid):
            zero_crossing = False
            if data[y * wid + x] > threshold:
                for kx, ky in neighbor:
                    nx = flip(x + kx, wid)
                    ny = flip(y + ky, hei)
                    if data[ny * wid + nx] < -threshold:
                        zero_crossing = True
                        break
            elif data[y * wid + x] < -threshold:
                for kx, ky in neighbor:
                    nx = flip(x + kx, wid)
                    ny = flip(y + ky, hei)
                    if data[ny * wid + nx] > threshold:
                        zero_crossing = True
                        break
            if zero_crossing:
                ret.append(0)
            else:
                ret.append(255)
    return ret

def main(infilename, kernel, threshold):
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
    data = edge_detector(pixellist, hei, wid, kernel, threshold)

    # save output image
    outfilename = kernel + '-' + str(threshold) + '-' + infilename
    out_img = Image.new('1', img.size)
    out_img.putdata(data)
    out_img.save(outfilename, 'bmp')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--kernel', type=str, help='use specific kernel to do zero crossing edge detection.')
    parser.add_argument('-t', '--threshold', type=int, help='set up threshold to determine white or black')
    parser.add_argument('infilename', type=str, help='input image name.')
    args = parser.parse_args()

    main(args.infilename, args.kernel, args.threshold)
