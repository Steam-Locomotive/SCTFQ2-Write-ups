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

I'm assuming you have read the solution to Punchagle and Punchagle 2, if not they can found [here](/algo/punchagle.md) and [here](/akgi/punchagle.md).

Rotate all the triangles so that they are readable. Read the symbols off the images as their decimal values or a marker for blanks and then locate the flag in the output, probably with the aid of an imaging library (as indicated by the hint). This is the same process as one and two, but with accounting for rotation.

### Details ###

Upon looking at all of the files, it is clear that the previous solution is not going to be successful, at least not without some method of correcting the rotation of the triangles. Need go home for moar codzenz

### Flag ###

    sctf{stoptheseprobspls}

### Extra Information ###
This solution would not have worked if the flag had been in one of the triangles that couldn't be read entirely, and honestly our solve did involve some amount of luck.
