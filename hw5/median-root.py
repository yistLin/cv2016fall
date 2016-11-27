#!/usr/local/bin/python3.5
import sys
import threading
from PIL import Image

try:
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
except Exception as e:
    print('usage: ./median-root [input file] [output file]')
    print('Error:', str(e))
    exit(1)

# global settings
kernel = [\
    (0,-3),\
    (-1,-2),(0,-2),(1,-2),\
    (-2,-1),(-1,-1),(0,-1),(1,-1),(2,-1),\
    (-3,0),(-2,0),(-1,0),(0,0),(1,0),(2,0),(3,0),\
    (-2,1),(-1,1),(0,1),(1,1),(2,1),\
    (-1,2),(0,2),(1,2),\
    (0,3)\
]

circular_kernel = [(-7, 0),(-6, -3),(-6, -2),(-6, -1),(-6, 0),(-6, 1),(-6, 2),(-6, 3),(-5, -4),(-5, -3),(-5, -2),(-5, -1),(-5, 0),(-5, 1),(-5, 2),(-5, 3),(-5, 4),(-4, -5),(-4, -4),(-4, -3),(-4, -2),(-4, -1),(-4, 0),(-4, 1),(-4, 2),(-4, 3),(-4, 4),(-4, 5),(-3, -6),(-3, -5),(-3, -4),(-3, -3),(-3, -2),(-3, -1),(-3, 0),(-3, 1),(-3, 2),(-3, 3),(-3, 4),(-3, 5),(-3, 6),(-2, -6),(-2, -5),(-2, -4),(-2, -3),(-2, -2),(-2, -1),(-2, 0),(-2, 1),(-2, 2),(-2, 3),(-2, 4),(-2, 5),(-2, 6),(-1, -6),(-1, -5),(-1, -4),(-1, -3),(-1, -2),(-1, -1),(-1, 0),(-1, 1),(-1, 2),(-1, 3),(-1, 4),(-1, 5),(-1, 6),(0, -7),(0, -6),(0, -5),(0, -4),(0, -3),(0, -2),(0, -1),(0, 0),(0, 1),(0, 2),(0, 3),(0, 4),(0, 5),(0, 6),(0, 7),(1, -6),(1, -5),(1, -4),(1, -3),(1, -2),(1, -1),(1, 0),(1, 1),(1, 2),(1, 3),(1, 4),(1, 5),(1, 6),(2, -6),(2, -5),(2, -4),(2, -3),(2, -2),(2, -1),(2, 0),(2, 1),(2, 2),(2, 3),(2, 4),(2, 5),(2, 6),(3, -6),(3, -5),(3, -4),(3, -3),(3, -2),(3, -1),(3, 0),(3, 1),(3, 2),(3, 3),(3, 4),(3, 5),(3, 6),(4, -5),(4, -4),(4, -3),(4, -2),(4, -1),(4, 0),(4, 1),(4, 2),(4, 3),(4, 4),(4, 5),(5, -4),(5, -3),(5, -2),(5, -1),(5, 0),(5, 1),(5, 2),(5, 3),(5, 4),(6, -3),(6, -2),(6, -1),(6, 0),(6, 1),(6, 2),(6, 3),(7, 0),]

def median_root(data, minhei, maxhei, hei, wid, maxIt):
    global kernel
    data_len = len(data)
    prev = data[:]
    result = data[:]
    it = 0

    while True:
        for y in range(minhei, maxhei):
            for x in range(wid):
                translated = []
                for x_k, y_k in kernel:
                    x_t = x + x_k
                    y_t = y + y_k
                    if 0 <= x_t < wid and 0 <= y_t < hei:
                        translated.append(prev[y_t * wid + x_t])
                translated = sorted(translated)
                result[y * wid + x] = translated[ int(len(translated) / 2) ]

        prev = result[:]
        it += 1
        if it > maxIt:
            break
    return result[ minhei*wid : maxhei*wid ]

class myThread (threading.Thread):
    def __init__(self, threadID, name, data, minhei, maxhei, hei, wid, maxIt, result):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.data = data
        self.hei = hei
        self.minhei = minhei
        self.maxhei = maxhei
        self.wid = wid
        self.maxIt = maxIt
        self.result = result

    def run(self):
        print ("Starting " + self.name)
        self.result += median_root(self.data, self.minhei, self.maxhei, self.hei, self.wid, self.maxIt)
        print ("Exiting " + self.name)

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

    # threading information
    threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4"]
    threadNum = len(threadList)
    threads = []
    results = [[] for _ in range(threadNum)]

    # Create new threads
    for i in range(threadNum):
        thread = myThread(i, threadList[i], data_seq, int(height * i / threadNum), int(height * (i+1) / threadNum), height, width, 10, results[i])
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    out_data = []
    for i in range(threadNum):
        out_data += results[i]

    print('Time to exit Main Thread')

    # save output image
    out_img = Image.new('L', in_img.size)
    out_img.putdata(out_data)
    out_img.save(outfilename, 'bmp')

if __name__ == '__main__':
    main()
