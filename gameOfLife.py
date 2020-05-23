import os
import re
from PIL import Image
import numpy as np
import random
import time

resolution = os.popen('xdpyinfo | grep dimensions').read()
resolutionFormat = re.compile('\d+x\d+\s')
res = resolutionFormat.findall(resolution)[0].split('x')
width, hight = int(res[0]),int(res[1])
#width, hight = 750,450

scale = 9
foo = scale//2

centers = []
data = np.full([hight,width], 255, dtype=np.uint8)

for i in range((hight//scale)):
    for j in range((width//scale)):
        row = i*scale + foo
        col = j*scale + foo
        centers.append((row,col))


randomList = random.sample(range(0, (width//scale)*(hight//scale)),2000)

for i in randomList:
    row,col = centers[i]
    if data[row-foo:row+foo+1,col-foo:col+foo+1].all() != 0:
        data[row-foo:row+foo+1,col-foo:col+foo+1] = 0
############### TEST#################
##Oscillators
#Blinker(period 2)

# data[103-foo:103+foo+1,247-foo:247+foo+1] = 0
# data[103-foo:103+foo+1,247-2*foo:247+2*foo+1] = 0
# data[103-foo:103+foo+1,247-3*foo:247+3*foo+1] = 0

######################################
img = Image.fromarray(data)
img.save('gameOfLife.png')
changeBackground = 'gsettings set org.gnome.desktop.background picture-uri "file:///home/mohamad/gameOfLife/gameOfLife/gameOfLife.png"' 
os.system(changeBackground)

# for i in range(10):
while True:
    time.sleep(5)
    newData = data.copy()
    for row,col in centers:
        btm = data[(row+scale)%hight, col]
        tp = data[(row-scale)%hight, col]
        rght = data[row, (col+scale)%width]
        lft = data[row, (col-scale)%width]
        btmrght = data[(row+scale)%hight, (col+scale)%width]
        btmlft = data[(row+scale)%hight, (col-scale)%width]
        tprght = data[(row-scale)%hight, (col+scale)%width]
        tplft = data[(row-scale)%hight, (col-scale)%width]
       # print(btm , tp , rght , lft , btmrght ,btmlft , tprght , tplft)
        totalSum = int((int(btm) + int(tp) + int(rght) + int(lft) + int(btmrght)+ int(btmlft) + int(tprght) + int(tplft) )/255)
       # print(col,row,totalSum)
        if data[row, col]  == 0:
            #print("alive")
            if (totalSum < 5) or (totalSum > 6):
                #print("will be dead",row,col,totalSum)
                newData[row-foo:row+foo+1,col-foo:col+foo+1] = 255
        else:
            #print("dead")
            if totalSum == 5:
                #print("will be born",row,col,totalSum)
                newData[row-foo:row+foo+1,col-foo:col+foo+1] = 0

    data = newData

    img = Image.fromarray(data)
    img.save('gameOfLife.png')

    changeBackground = 'gsettings set org.gnome.desktop.background picture-uri "file:///home/mohamad/gameOfLife/gameOfLife/gameOfLife.png"' 
    os.system(changeBackground)


# TODO

# find a good name for foo variable :)
# add margine due to the screen resolution 
# check if it reaches a stable form restart the program and notifiy the user
# add the ocilation shape option to start with
# add clock to it
# add note to it so it is always on screen
# creat gui and and add other fun patterns like Fractals ...
# and so many things...


