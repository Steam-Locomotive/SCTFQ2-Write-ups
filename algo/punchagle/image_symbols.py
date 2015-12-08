from PIL import Image
import os

def getImageSymbol(syms, img) :
    for x in range(0, len(syms)) :
        if(syms[x] == img) :
            return x
    return -1
#show flag is for debugging, can be ignored in normal running
def getRowCount(numerals, test, show = False) :
    #attempt to find 1 number row count
    num = test.crop((test.width / 2 - 3, 32-7, test.width / 2 + 2, 32))
    numRows = getImageSymbol(numerals, num)
    if (numRows == -1) :
        #if 1 number isn't readable, get row count from 2 numbers
        num1 = test.crop((test.width / 2 - 6, 32-7, test.width / 2 - 1, 32))
        num2 = test.crop((test.width / 2, 32-7, test.width / 2 + 5, 32))
        n1 = getImageSymbol(numerals, num1) * 10
        n2 = getImageSymbol(numerals, num2)
        if(n1 == -1 or n2 == -1) :
            if show:
                num.show()
                num1.show()
                num2.show()
            return -1
        numRows = n1 + n2
    return numRows

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
        else : tmp += str(sym)
    return tmp
            
            

def readTriangle(symbols, numerals, img) :
    rows = getRowCount(numerals, img)
    res = ""
    for x in range(1, rows + 1) :
        res += readTriangleRow(symbols, img, x)
    return res
        

symbols = []
numerals = []
symbolBase = Image.open("punchagle_symbols.png")
for x in range(0, 10) :
    symbols.append(symbolBase.crop((x * 11, 0, x * 11 + 11, 11)))
for x in range(0, 10) :
    offset = 0
    #this offset is due to how it was easiest to recognize the numbers;
    #all numbers other than 1 and 4 only took up 5 pixels, so I special-cased 1 and 4
    if x == 4 or x == 1 : offset = -1
    numerals.append(symbolBase.crop((x * 6 + 1 + offset, 11, x * 6 + 6 + offset, 18)))
    
out = open('symbolOutput.txt', 'w')

import os
rootdir = 'images'
count = 0
result = ""

for subdir, dirs, files in os.walk(rootdir):
    for f in files:
        count += 1
        if count % 100 == 0 : print count
        test = Image.open(os.path.join(subdir, f))
        result += '\nTriangle: ' + f + '\n'
        result += readTriangle(symbols, numerals, test)
out.write(result)
out.close()

        
    

