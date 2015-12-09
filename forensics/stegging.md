## Stegging - 25 (Forensics) ##
#### Writeup by GenericNickname

Created: 2015-12-08

### Problem ###

The cat tried to steg something. For some reason he sort of failed to desteg. Maybe he mixed up something?

Also, here are the Stegging for Dummies articles.

## Files ##
[original.jpg](http://compete.sctf.io/2015q2/problemfiles/29/original.jpg)

[stegged.jpg](http://compete.sctf.io/2015q2/problemfiles/29/stegged.jpg)

## Answer ##

### Overview ###

Locate the flag in these two files.

### Details ###

The problem tells you to learn about stegging, or [Steganography](https://en.wikipedia.org/wiki/Steganography), and one of the simplest methods is to just put the data to be hidden at the end of the file. However, we are given both images, so it does not seem as though this is the case.

The next simplest thing to try is to just look for a difference between the files. This can be done from command line with either `bindiff` on OSX or linux, or `FC` on windows. I personally used `FC original.jpg stegged.jpg > stegged.txt`. 
The flag can then be found on the first few lines of the output.
### Flag ###

    flag{y0u_have_gradu4ted_fr0m_th3_baby'5 b07713!!}