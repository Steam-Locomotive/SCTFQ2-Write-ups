## Punchagle - 100 (Algo) ##

#### Write-up by GenericNickname

Created: 2015-12-07

### Problem ###

There's a lot of images here, like, a lot. But they have significance.

Each image contains a punchagle, similar to the punch cards used in old computers. You're given that each shape represents a number, 0-9, and when 1 to 3 shapes in a row are converted to numbers, they make an ASCII character decimal value.
```
  0 = filled circle
  1 = outlined circle
  2 = filled square
  3 = outline square
  4 = filled triangle
  5 = outlined triangle
  6 = filled semicircle UP
  7 = outlined semicircle UP
  8 = filled semicircle DOWN
  9 = outlined semicircle DOWN
```

The flag is hidden somewhere in those, convert all the images and find it. sctf{FLAG} is the format.

### Files ###
[images.7z](http://compete.sctf.io/2015q2/problemfiles/56/images.7z)

### Hint ###

Imaging libraries might help.

## Answer ##

### Overview ###

Read the symbols off the images as their decimal values and then locate the flag in the output, probably with the aid of an imaging library (as indicated by the hint).

### Details ###

There are many imaging libraries, but I decided to go with [Pillow](https://python-pillow.github.io/), which is for Python (Python 2.7 in my case). After examining some images, I realized it would be possible to just go through and match the numbers at the top of the images and then go through row by row and match the symbols. Pillow allowed me to do direct image evaluation, so it was just a matter of isolating the numbers and symbols, then trying to match them.

I made this image by copying the symbols out of the triangles so I would have something to match against:
<br/>
![punchagle symbols]: /aglo/punchagle/punchagle_symbols.png  "Punchagle Symbols"

To get the symbols into python, I loaded them as two arrays:

```python
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
```

After making my list of symbols, I wrote a function that would tell me what symbol index a particular image matched to, or -1 if it couldn't find a match:

```python
def getImageSymbol(syms, img) :
    for x in range(0, len(syms)) :
        if(syms[x] == img) :
            return x
    return -1
```
The nice thing about the triangles in this set is that it was very easy to determine where numbers and symbols were in the triangles, so I used a lot of hard coded values to read them.
<br/>
I used this function to read how many rows were in the triangles by checking first for 1 digit, and if it didn't match, then reading for 2 digits:

```python
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
```

Once I knew how many rows there were, I went through each row and read the symbols off it with this function:

```python
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
		#this if can be ignored for now, it will be helpful for Punchagle 2 where symbols are omitted 
        if(sym == -1) : tmp += 'x'
        else : tmp += str(sym)
    return tmp
```

The rest of my program was a funtion for reading the triangles and walking through the directory to read all the images:

```python
def readTriangle(symbols, numerals, img) :
    rows = getRowCount(numerals, img)
    res = ""
    for x in range(1, rows + 1) :
        res += readTriangleRow(symbols, img, x)
    return res
```

```python
out = open('symbolOutput.txt', 'w')

import os
rootdir = 'images'
count = 0
result = ""

for subdir, dirs, files in os.walk(rootdir):
    for f in files:
        count += 1
        if count % 100 == 0 : print count #to see how far we've gotten
        test = Image.open(os.path.join(subdir, f))
        result += '\nTriangle: ' + f + '\n'
        result += readTriangle(symbols, numerals, test)
out.write(result)
out.close()
```

The entire program can be downloaded here: [image_symbols.py](/algo/punchagle/image_symbols.py)

Now that I had symbolOutput.txt, I could search for the ASCII values that should show up where the flag is. The problem says that the flag starts with sctf{ so I looked for ```11599116102123``` in the output and identified the end by ```125```, which is }. The entire string of digits was ```1159911610212311211410111611612199111111108114105116101125```, which, when turned into ASCII yields the flag: ```sctf{prettycoolrite}```

### Flag ###

	sctf{prettycoolrite}

### Extra Information ###
This solution would not have worked if the flag had been across triangles (which will come into play in Punchagle 3), although it could have been modified to work by removing ```result += '\nTriangle: ' + f + '\n'``` from the output.
