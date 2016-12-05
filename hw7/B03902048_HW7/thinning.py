#!/usr/local/bin/python3.5
import sys
from PIL import Image

def binarize(data):
    ret = []
    for p in data:
        ret.append(1 if p > 127 else 0)
    return ret

def downsampling(data, hei, wid):
    ret = []
    offset = 8
    for y in range(0, hei, offset):
        for x in range(0, wid, offset):
            ret.append(data[y * wid + x])
    return (ret, int(hei/offset), int(wid/offset))

def expand(data, hei, wid):
    ret = []
    ret += [0] * (wid+2)

    offset = 0
    for h in range(hei):
        ret += [0] + data[offset : offset+wid] + [0]
        offset += wid
    
    ret += [0] * (wid+2)
    return (ret, hei+2, wid+2)

def markIB(data, hei, wid):
    ret = [0] * len(data)
    for y in range(1, hei-1):
        for x in range(1, wid-1):
            curr = y * wid + x
            count = 0
            if data[curr]:
                count += data[curr-1] + data[curr+1]
                count += data[curr-wid-1] + data[curr-wid] + data[curr-wid+1]
                count += data[curr+wid-1] + data[curr+wid] + data[curr+wid+1]
                if count < 8:
                    ret[curr] = 1
                elif count == 8:
                    ret[curr] = 2
    return ret

def mark_deletable(data, hei, wid):
    for y in range(1, hei-1):
        for x in range(1, wid-1):
            curr = y * wid + x
            if data[curr] == 1:
                if 2 in [data[curr-1], data[curr+1], data[curr-wid-1], data[curr-wid], data[curr-wid+1], data[curr+wid-1], data[curr+wid], data[curr+wid+1]]:
                    data[curr] = 3

def h(b, c, d, e):
    return 1 if b == c and (d != b or e != b) else 0

def print_data(data, hei, wid):
    print('printing data:')
    for y in range(hei):
        for x in range(wid):
            if data[y*wid+x] != 0:
                print(data[y*wid+x], end=' ')
            else:
                print(' ', end=' ')
        print()

def thinning(data, hei, wid):
    # expand the border of image
    exp_data, exp_hei, exp_wid = expand(data, hei, wid)

    prev_data = exp_data[:]

    while True:
        # mark border(1) and interior(2)
        marked = markIB(exp_data, exp_hei, exp_wid)

        # find deletable border(3)
        mark_deletable(marked, exp_hei, exp_wid)

        for y in range(1, exp_hei-1):
            for x in range(1, exp_wid-1):
                curr = y * exp_wid + x
                if marked[curr] == 3:
                    f = 0
                    f += h(exp_data[curr], exp_data[curr+1], exp_data[curr-exp_wid+1], exp_data[curr-exp_wid])
                    f += h(exp_data[curr], exp_data[curr-exp_wid], exp_data[curr-exp_wid-1], exp_data[curr-1])
                    f += h(exp_data[curr], exp_data[curr-1], exp_data[curr+exp_wid-1], exp_data[curr+exp_wid])
                    f += h(exp_data[curr], exp_data[curr+exp_wid], exp_data[curr+exp_wid+1], exp_data[curr+1])
                    if f == 1:
                        marked[curr] = 0
                        exp_data[curr] = 0

        for i in range(len(exp_data)):
            if exp_data[i] != prev_data[i]:
                break
        else:
            break
        prev_data = exp_data[:]

    return exp_data, exp_hei, exp_wid

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
    data, hei, wid = thinning(data, hei, wid)

    try:
        out_f = open(outfilename, 'w')
    except Exception as e:
        print('Error:', str(e))
        exit(1)

    for y in range(1, hei-1):
        for x in range(1, wid-1):
            if data[y*wid+x] == 1:
                out_f.write('*')
            else:
                out_f.write(' ')
        out_f.write("\n")
    out_f.close()

    # generate 64x64 image output
    out_img = Image.new('L', (wid, hei))
    output_data = []
    for p in data:
        output_data.append(255 if p == 1 else 0)
    out_img.putdata(output_data)
    out_img.save('thinned-' + infilename, 'bmp')

if __name__ == '__main__':
    main()
