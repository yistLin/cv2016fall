#!/usr/local/bin/python3.5
import sys
from PIL import Image

try:
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
except Exception as e:
    print('usage: ./yokoi.py [input file] [output file]')
    print('Error:', str(e))
    exit(1)

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

def get_pattern(a1, a2, a3):
    if a1 == 1:
        if a2 == 1 and a3 == 1:
            return 'r'
        else:
            return 'q'
    else:
        return 's'

def yokoi(data, hei, wid):
    expd = [0] * (hei+2) * (wid+2)
    for y in range(hei):
        for x in range(wid):
            expd[(y+1) * (wid+2) + (x+1)] = data[y * wid + x]

    result = [' '] * (hei * wid)
    f = {'r':0, 'q':0, 's':0}
    for y in range(1, hei+1):
        for x in range(1, wid+1):
            f['r'] = 0
            f['q'] = 0
            f['s'] = 0
            if expd[y * (wid+2) + x] == 1:
                f[get_pattern(expd[y*(wid+2)+(x+1)],expd[(y-1)*(wid+2)+(x+1)],expd[(y-1)*(wid+2)+x])] += 1
                f[get_pattern(expd[(y-1)*(wid+2)+x],expd[(y-1)*(wid+2)+(x-1)],expd[y*(wid+2)+(x-1)])] += 1
                f[get_pattern(expd[y*(wid+2)+(x-1)],expd[(y+1)*(wid+2)+(x-1)],expd[(y+1)*(wid+2)+x])] += 1
                f[get_pattern(expd[(y+1)*(wid+2)+x],expd[(y+1)*(wid+2)+(x+1)],expd[y*(wid+2)+(x+1)])] += 1
                if f['r'] == 4:
                    result[(y-1) * wid + (x-1)] = str(5)
                else:
                    result[(y-1) * wid + (x-1)] = str(f['q'])
            else:
                result[(y-1) * wid + (x-1)] = ' '
    return result

def main():
    # get input image
    try:
        in_img = Image.open(infilename)
    except Exception as e:
        print('Error:', str(e))
        exit(1)
    width, height = in_img.size
    
    # get 1D image data
    data_seq = list(in_img.getdata())

    # binarize the image
    bin_data = binarize(data_seq)

    # downsampling the image
    down_data, newhei, newwid = downsampling(bin_data, height, width)

    # yokoi neighborhood operate
    out_data = yokoi(down_data, newhei, newwid)

    # open output file
    try:
        out_file = open(outfilename, 'w')
    except Exception as e:
        print('Error:', str(e))
        exit(1)
    linecounter = 0
    for p in out_data:
        out_file.write(p)
        linecounter += 1
        if linecounter >= newwid:
            out_file.write("\n")
            linecounter = 0
    out_file.close()

if __name__ == '__main__':
    main()

