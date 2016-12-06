#!/usr/local/bin/python3.5
import sys
from math import log10
from PIL import Image

def main():
    # initial setup
    try:
        original_filename = sys.argv[1]
        processed_filename = sys.argv[2]
    except Exception as e:
        print('usage: ./calc_SNR.py [original] [processed]')
        print('Error:', str(e))
        exit(1)

    # get input image
    try:
        ori_img = Image.open(original_filename)
        proc_img = Image.open(processed_filename)
    except Exception as e:
        print('Error:', str(e))
        exit(1)

    # get 1D image data
    ori_pixellist = list(ori_img.getdata())
    proc_pixellist = list(proc_img.getdata())

    # calculate mu, mu_n
    mu = sum(ori_pixellist) / len(ori_pixellist)
    mu_n = sum([ (proc_pixellist[i] - ori_pixellist[i]) for i in range(len(proc_pixellist)) ]) / len(proc_pixellist)

    # calculate VS
    vs = sum( [(p - mu)**2 for p in ori_pixellist] ) / len(ori_pixellist)
    vn = sum( [(proc_pixellist[i] - ori_pixellist[i] - mu_n)**2 for i in range(len(proc_pixellist))] ) / len(proc_pixellist)

    # calculate SNR
    snr = 10 * log10(vs / vn)

    print('SNR of %s(original) and %s(processed) =' % (original_filename, processed_filename), str(snr))

if __name__ == '__main__':
    main()
