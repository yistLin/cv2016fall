#!/usr/local/bin/python3.5
import sys
from PIL import Image, ImageDraw

LABEL = 0
THRESHOLD = 500

def get_label():
    global LABEL
    LABEL += 1
    return LABEL

infilename = sys.argv[1]
outfilename = sys.argv[2]

inImg = Image.open(infilename)

data_seq = list(inImg.getdata())

label_map = [0] * len(data_seq)

width, height = inImg.size
nei_offset = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,1),(-1,1),(1,0),(1,1)]
# nei_offset = [(-1,0),(0,-1),(1,0),(0,1)]

# label connected components
for y in range(height):
    for x in range(width):
        if label_map[y*width+x] == 0 and data_seq[y*width+x] == 255:
            curr_label = get_label()
            curr_color = data_seq[y*width+x]
            
            state_q = []
            label_map[y * width + x] = -1
            state_q.append((x,y))
            
            while len(state_q) != 0:
                tmp_x, tmp_y = state_q.pop(0)
                label_map[tmp_y * width + tmp_x] = curr_label
                
                for offset in nei_offset:
                    off_x = tmp_x + offset[0]
                    off_y = tmp_y + offset[1]
                    if 0 <= off_x < width and 0 <= off_y < height and label_map[off_y*width+off_x] == 0 and data_seq[off_y*width+off_x] == curr_color:
                        label_map[off_y * width + off_x] = -1
                        state_q.append((off_x,off_y))

# process labeled region that cover more than 500 pixels
count_label = [0] * (LABEL+1)
label_array = [[] for _ in range(LABEL+1)]
for y in range(height):
    for x in range(width):
        count_label[label_map[y*width+x]] += 1
        label_array[label_map[y*width+x]].append((x,y))

outImg = Image.open(infilename).convert('RGB')
draw = ImageDraw.Draw(outImg)

for i in range(1,len(count_label)):
    if count_label[i] >= THRESHOLD:
        topVal = min(label_array[i], key=lambda x: x[1])[1]
        bottomVal = max(label_array[i], key=lambda x: x[1])[1]
        leftVal = min(label_array[i], key=lambda x: x[0])[0]
        rightVal = max(label_array[i], key=lambda x: x[0])[0]
        print("label-count =", count_label[i], ",", topVal, bottomVal, leftVal, rightVal)

        sum_x, sum_y = 0, 0
        for j in range(len(label_array[i])):
            sum_x += label_array[i][j][0]
            sum_y += label_array[i][j][1]
        avg_x = int(sum_x / len(label_array[i]))
        avg_y = int(sum_y / len(label_array[i]))
        rcolor = (255, 0, 0)
        draw.rectangle([(leftVal,topVal),(rightVal,bottomVal)], outline=rcolor)
        draw.line([(avg_x-5,avg_y-5),(avg_x+5,avg_y+5)], fill=rcolor)
        draw.line([(avg_x+5,avg_y-5),(avg_x-5,avg_y+5)], fill=rcolor)

print("LABEL =", LABEL)

outImg.save(outfilename, 'bmp')

