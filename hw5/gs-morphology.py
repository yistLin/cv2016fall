#!/usr/local/bin/python3.5
import sys
from PIL import Image

try:
    option = sys.argv[1]
    infilename = sys.argv[2]
    outfilename = sys.argv[3]
except Exception as e:
    print('usage: ./gs-morphology [option] [input file] [output file]')
    print('Error:', str(e))
    exit(1)

# global settings
kernel = [\
    (-1,-2),(0,-2),(1,-2),\
    (-2,-1),(-1,-1),(0,-1),(1,-1),(2,-1),\
    (-2,0),(-1,0),(0,0),(1,0),(2,0),\
    (-2,1),(-1,1),(0,1),(1,1),(2,1),\
    (-1,2),(0,2),(1,2)\
]

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

    # 4 options
    if option == 'erosion':
        out_data = erosion(data_seq, width, height)
    elif option == 'dilation':
        out_data = dilation(data_seq, width, height)
    elif option == 'opening':
        out_data = opening(data_seq, width, height)
    elif option == 'closing':
        out_data = closing(data_seq, width, height)
    else:
        print('usage: [option] should be erosion, dilation, opening, or closing')
        exit(1)

    # save output image
    out_img = Image.new('L', in_img.size)
    out_img.putdata(out_data)
    out_img.save(outfilename, 'bmp')

if __name__ == '__main__':
    main()
