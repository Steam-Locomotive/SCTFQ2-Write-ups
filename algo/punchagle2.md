## Punchagle 2 - 170 (Algo) ##

#### Write-up by Generic Nickname

Created: 2015-12-07

### Problem ###

Same format as Punchagle 1, except this time, some shapes have been omitted.

```sctf{FLAG}``` is the format.

### Files ###
[images.7z](http://compete.sctf.io/2015q2/problemfiles/57/images.7z)

### Hint ###

Imaging libraries are necessary if you haven't figured that out already.

## Answer ##

### Overview ###

I'm assuming you have read the solution to Punchagle, if not it can be found [here](/algo/punchagle.md).

Read the symbols off the images as their decimal values or a marker for blanks and then locate the flag in the output, probably with the aid of an imaging library (as indicated by the hint). This is the same process as one, but with accounting for blanks.

### Details ###
Running the same code from Punchagle will get an output file, but with x's replacing the places in triangles without symbols. This happens because my symbol matching returns -1 if it doesn't match, and in the function below I specify that -1's should be x's.
```python
#this is the same function as in the original Punchagle solution
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
    	#this is the relevant line where the -1's turn into x's
        sym = getImageSymbol(symbols, rowSyms.crop((20 * x, 0, 20 * x + 11, 11)))
        if(sym == -1) : tmp += 'x'
        else : tmp += str(sym)
    return tmp
```

Once again I have a symbolOutput.txt, so I can search for the string that I want. However, I need to account for omitted digits.
<br/>
After looking at a couple triangles, it becomes obvious that the missing digits are 3, 4, 7, and 8, so i can take my search from Punchagle 1 and repeat it, switching those numbers for x's. Looking for ```1159911610212x``` in the output and identifying the end by ```125``` once again reveals the needed text . The entire string of digits was ```1159911610212x10x10110x10x11110x10110x10x111125```. Being lazy, I wrote a really quick python script to brute force the missing digits for me:
```python
data = '10x 101 10x 10x 111 10x 101 10x 10x 111'
toBrute = data.split(' ')
things = 'ghkl'

for a in range(0, 4) :
    for b in range (0, 4) :
        for c in range(0, 4) :
            for d in range (0, 4) :
                for e in range(0, 4) :
                    for f in range (0, 4) :
                        print things[a] + 'e' + things[b] + things[c] + 'o' + things[d] + 'e' + things[e] + things[f] + 'o'

```

After looking through the output, it can be seen that the words hellohello, which would make the flag ```sctf{hellohello}```. Submitting the problem reveals that it is indeed the correct flag.

### Flag ###

    sctf{hellohello}

### Extra Information ###
This solution would not have worked if the flag had been across triangles (which will come into play in Punchagle 3), although it could have been modified to work by removing ```result += '\nTriangle: ' + f + '\n'``` from the output.
