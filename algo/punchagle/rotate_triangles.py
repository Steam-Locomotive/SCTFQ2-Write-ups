from PIL import Image
import os
rootdir = 'images'
fixeddir = 'fixedImages'
count = 0
result = ""

import math

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.degrees(math.acos(dotproduct(v1, v2) / (length(v1) * length(v2))))

def pDistance(p1, p2) :
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def getQuadrant(c1) :
    if c1[0] > 0:
        if c1[1] > 0 : return 1
        else : return 4
    else :
        if c1[1] > 0 : return 2
        else : return 3

def isLeftMoreThanRight(img):
    white = (255, 255, 255)
    left = 0
    right = 0
    for i in range(0, img.height):
        if img.getpixel(((int)(img.width / 8), i)) == white:
            left = left + 1
    for i in range(0, img.height):
        if img.getpixel(((int)(img.width / 8 + (img.width / 4) + (img.width / 2)), i)) == white:
            right = right + 1
    return (left > right)

        
def getPointToRotate(c1, c2, center) :
    c1 = (c1[0] - center[0], (test.height - c1[1]) - center[1])
    c2 = (c2[0] - center[0], (test.height - c2[1]) - center[1])
    q1 = getQuadrant(c1)
    q2 = getQuadrant(c2)
    used = [False] * 5
    used[q1] = True
    used[q2] = True
    ##c1 will always be the lower quadrant
    if q1 > q2 :
        temp = c1
        c1 = c2
        c2 = temp
    if q1 == q2 :
        if q1 == 1 : return c1 if c1[1] > c2[1] else c2
        if q1 == 2 : return c1 if c1[0] < c2[0] else c2
        if q1 == 3 : return c1 if c1[1] < c2[1] else c2
        if q1 == 4 : return c1 if c1[0] > c2[0] else c2
    if used[1] and used[2] : return c2
    if used[1] and used[3] : return c1
    if used[1] and used[4] : return c1
    if used[2] and used[3] : return c2
    if used[2] and used[4] : return c2
    if used[3] and used[4] : return c2

##Main code starts here
for subdir, dirs, files in os.walk(rootdir):
    for f in files:
        count += 1
        if count % 100 == 0 : print count
        test = Image.open(os.path.join(subdir, f))
        yellow = (255, 255, 0)
        cor1 = (-1, -1)
        cor2 = (-1, -1)
        inset = 0
        down = up = left = right = False
        while cor2 == (-1, -1) :
            x = test.width - inset
            y = test.height - inset
            if (not down) :
                for i in range (1, x) :
                    if test.getpixel((x - i, y - 1)) == yellow :
                        down = True
                        if(cor1 == (-1, -1)) :
                            cor1 = (x - i, y - 1)
                        else :
                            cor2 = (x - i, y - 1)
                        break
            if(cor1 == (-1, -1) or cor2 == (-1, -1) and not left) :
                for i in range (1, y) :
                    if test.getpixel((inset, y - i)) == yellow :
                        left = True
                        if(cor1 == (-1, -1)) :
                            cor1 = (inset, y - i)
                        else :
                            cor2 = (inset, y - i)
                        break
            if(cor1 == (-1, -1) or cor2 == (-1, -1) and not up) :
                for i in range (1, x) :
                    if test.getpixel((inset + i, inset)) == yellow :
                        up = True
                        if(cor1 == (-1, -1)) :
                            cor1 = (inset + i, inset)
                        else :
                            cor2 = (inset + i, inset)
                        break
            if(cor1 == (-1, -1) or cor2 == (-1, -1) and not right) :
                for i in range (1, y) :
                    if test.getpixel((x - 1, inset + i)) == yellow :
                        right = True
                        if(cor1 == (-1, -1)) :
                            cor1 = (x - 1, inset + i)
                        else :
                            cor2 = (x - 1, inset + i)
                        break
            if(cor2 == (-1, -1)) :
                inset += 1

        toRotate = 0
        distance = pDistance(cor1, cor2)
        center = (test.width / 2, test.height / 2)
        orig = (distance / 2, -distance / 2)
        right = getPointToRotate(cor1, cor2, center)
        toRotate = (angle((right), (orig)))
        if isLeftMoreThanRight(test):
            toRotate *= -1
        newImg = test.rotate(math.ceil(toRotate))
        newImg.save(os.path.join(fixeddir, f))

