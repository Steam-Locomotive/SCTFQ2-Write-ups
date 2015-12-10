## Punchagle 3 - 250 (Algo) ##

#### Write-up by GenericNickname

Created: 2015-12-07

### Problem ###

Same format as Punchagle 1 & 2, except this time, some shapes have been omitted, AND the triangles are randomly rotated.

`sctf{FLAG}` is the format.

### Files ###
[images.7z](http://compete.sctf.io/2015q2/problemfiles/58/images.7z)

### Hint ###

Imaging libraries REALLY ARE **NECESSARY** if you haven't figured that out yet!

## Answer ##

### Overview ###

I'm assuming you have read the solution to Punchagle and Punchagle 2, if not they can found [here](punchagle.md) and [here](punchagle2.md).

Rotate all the triangles so that they are readable. Read the symbols off the images as their decimal values or a marker for blanks and then locate the flag in the output, probably with the aid of an imaging library (as indicated by the hint). This is the same process as one and two, but with accounting for rotation.

### Details ###

Upon looking at all of the files, it is clear that the previous solution is not going to be successful, at least not without some method of correcting the rotation of the triangles.

Rotation is by far the worst part of this problem, and it was only made worse due to me being lazy. I didn't want to learn opencv or some imaging library other than Pillow, so I wrote a script to rotate all the images so that they were all either upright or almost upright.

Just fixing the rotation turned into a three step process. First, I wrote some logic to locate the two corners of the triangle that should be at the bottom, by scanning along the edges of the images until I found them, making sure to only match once per side:
```python
from PIL import Image
import os
rootdir = 'images'
fixeddir = 'fixedImages'
count = 0
result = ""

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
```

Once I had the two coordinates, I decided to pick one and rotate it so that it should be in the bottom right corner. This was done by comparing the quandrants of the cordinates after making them relative to the center of the image:

```python
def getQuadrant(c1) :
    if c1[0] > 0:
        if c1[1] > 0 : return 1
        else : return 4
    else :
        if c1[1] > 0 : return 2
        else : return 3

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
```
Finally, I used some vector math to get the angle between the bottom right corner and my cordinate:

```python
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
```
and then I used Pillow's rotate function to rotate the images and save them to a new directory (this is in the file system for loop from earlier):
```python
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
```
The full code for the rotation can be downloaded [here](punchagle/rotate_triangles.py).

This code doesn't work perfectly, as some of the images were off by a few degrees (this was particularly bad on smaller triangles), and it also had some issues dealing with triangles that had already been correctly oriented. Some of these issues we fixed by hand, and others we ignored and hoped wouldn't hinder us.

Now that I had correctly oriented triangles (mostly), I had to read the symbols off of them. Unfortunately, the old code from Punchagle and Punchagle 2 will not work without some modifications, because the rotation messed up the numbers and symbols.

The first step was to get rid of the black borders that all of the images had due to their canceled out rotation, and in the function I wrote for doing so, I also allowed it to try to correct minor imperfections in the initial rotation code:
```python
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
```

Now to match symbols that had been skewed by rotation, I found a function that would return a percentage of how different two images were:

```python
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
```

and modified my symbol matching to go through all the symbols and figure out which one the data from the triangle was most similar to (I also skipped indices 3, 4, 8, and 9, because those were the missing symbols for this set of images):

```python
def getImageSymbol(syms, img) :
    least = (100, -1)
    for x in range(0, len(syms)) :
        if x == 3 or x == 4 or x == 8 or x == 9 : continue
        diff = diffImages(syms[x], img)
        if diff < least[0] : least = diff, x
    if least[1] == 10 : return -1
    return least[1]
```

To accomadate blanks with this new matching system, I had to update my symbol table to have a blank tile as well:
<br/>
![punchagle 3 symbols](punchagle/punchagle3_symbols.png)

Fortunately, I was able to use the same `readTriangleRow` function as before, but I did have to make a minor modification to `readTriangle`. The numbers were by far more messed up than the symbols after the rotation, so instead I used some basic math to determine how many rows each triangle should have:

```python
def readTriangle(symbols, numerals, img) :
    rows = int(math.ceil((img.height - 40) / 20)) #this is the different line
    res = ""
    for x in range(1, rows + 1) :
        res += readTriangleRow(symbols, img, x)
    return res
```

Finally, all the code gets run by another directory for loop, and this time the output is one line of all the triangles (although I later learned that because of how my code reads file systems this wouldn't have worked), and then each triangle separated out to make them easier to look through:

```python
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
```

The full code for reading the triangles can be downloaded [here](punchagle/image_symbols_2.py).

Since I knew that 3, 4, 8, and 9 were all omitted from the file and replaced by x's, i searhced for `115xx11610212x` in the output, but that was unsucessful. However, `15xx11610212x` did show up, and a `125` could be seen later in the same triangle, so I figured it was the flag.

This was the output: `15xx11610212x11511611111211610x10111510111211x111xx11511210x115125`. It was then that I realized that this flag must have been slightly across triangles, with the missing open circle for the first `1` of `115` in the previous triangle. Because the x's were more spread out in this flag, it was easier to decode by hand, so I didn't bother to use a brute force method as I did for Punchagle 2.

The finals numbers were `1159911610212311511611111211610410111510111211411198115112108115125`, or `sctf{stoptheseprobsplease}` when turned into ASCII.
### Flag ###

    sctf{stoptheseprobspls}

### Extra Information ###
This solution would not have worked if the flag had been in one of the triangles that couldn't be read entirely due to imperfect rotation, or if the flag had been more split up between the two triangles.
