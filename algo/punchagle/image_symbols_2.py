from PIL import Image
import os

from PIL import ImageChops
import math, operator

from itertools import izip
def diffImages (i1, i2) :
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."
     
    pairs = izip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
     
    ncomponents = i1.size[0] * i1.size[1] * 3
    perc = (dif / 255.0 * 100) / ncomponents
    return perc

def getImageSymbol(syms, img) :
    least = (100, -1)
    for x in range(0, len(syms)) :
        if x == 3 or x == 4 or x == 8 or x == 9 : continue
        diff = diffImages(syms[x], img)
        if diff < least[0] : least = diff, x
    if least[1] == 10 : return -1
    return least[1]

def readTriangleRow(symbols, img, row) :
    x1 = img.width / 2 - 15 - (row - 1) * 10
    y1 = 40 + (row - 1) * 20
    x2 = img.width / 2 + 16 + (row - 1) * 10
    y2 = 51 + (row - 1) * 20
    rowSyms = img.crop((x1, y1, x2, y2))
    symbolCount = row + 1
    tmp = ""
    res = ""
    for x in range(0, symbolCount) :
        sym = getImageSymbol(symbols, rowSyms.crop((20 * x, 0, 20 * x + 11, 11)))
        if(sym == -1) : tmp += 'x'
        elif sym == -2 : return "-1"
        else : tmp += str(sym)
    return tmp
            
            

def readTriangle(symbols, numerals, img) :
    rows = int(math.ceil((img.height - 40) / 20))
    if rows == -2 : return ""
    res = ""
    for x in range(1, rows + 1) :
        strn = readTriangleRow(symbols, img, x)
        if strn == "-1" : return ""
        res += strn
    return res

def findSquareEdges(img, tries = 0) :
    tries = tries + 1
    w = img.width
    h = img.height
    foundEdge = False
    for y in range(0, h / 2) :
        l = img.getpixel((w / 4, y))
        r = img.getpixel((w * 3 / 4, y))
        if l != r and tries < 3:
            if(l == (0, 0, 0)) :
                img = img.rotate(-1)
                return findSquareEdges(img, tries)
            else :
                img = img.rotate(1)
                return findSquareEdges(img, tries)
        if l != (0, 0, 0) or r != (0, 0, 0) :
            x = y
            x2 = w - y
            if(img.getpixel((x, h / 2)) == (0, 0, 0)) : x = x + 1
            if x2 + 1 < w and (img.getpixel((x2 + 1, h / 2)) != (0, 0, 0)) : x2 = x2 - 1
            return img.crop((x, y, x2, h - y))
        

symbols = []
numerals = []
symbolBase = Image.open("punchagle3_symbols.png")
for x in range(0, 11) :
    symbols.append(symbolBase.crop((x * 11, 0, x * 11 + 11, 11)))
for x in range(0, 10) :
    offset = 0
    if x == 4 or x == 1 : offset = -1
    numerals.append(symbolBase.crop((x * 6 + 1 + offset, 11, x * 6 + 6 + offset, 18)))
    
out = open('symbolsOut3.txt', 'w')

import os
rootdir = 'fixedImages'
count = 0
result = ""
result1 = ""

for subdir, dirs, files in os.walk(rootdir):
    for f in files:
        if f[0] == 'a' : continue
        count += 1
        print f
        if count % 100 == 0 : print count
        test = findSquareEdges(Image.open(os.path.join(subdir, f)).convert("RGB"))
        result += '\nTriangle: ' + f + '\n'
        thisTriangle = readTriangle(symbols, numerals, test)
        result += thisTriangle
        result1 += thisTriangle
out.write(result1)
out.write(result)
out.close()
        

        
    

