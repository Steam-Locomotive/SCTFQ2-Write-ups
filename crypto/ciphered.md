## Ciphered - 5 (Cryptography) ##

#### Writeup by Oksisane

Created: 2015-12-08

### Problem ###

I accidentally encrypted my flag, and I don't know how to decrypt it :(

Can you help me please?

### Files ###
[encrypted.py](http://compete.sctf.io/2015q2/problemfiles/26/encrypt.py)
[encrypted.txt](http://compete.sctf.io/2015q2/problemfiles/26/encrypted.txt)
## Answer ##

### Overview ###

Shift the characters till they can be base 64 decoded, then repeat

### Details ###
The source runs for 80 counts on the text, at random choosing to either shift the characters in the current text by one or base64 encode the current text. To decrypt, we simply need to reverse this process. Our code should shift the message by one character until it is valid base64, then decrypt the base64 and repeat. Here's the code I used:
```python
import base64
import random
import string

file = open('encrypted.txt','r')
encrypted = file.read()
alphabet = string.ascii_letters + string.digits
def findNextPlain(encrypted):
    text = ""
    i = 0
    while len(text) == 0 and i < 62:
        alphabet_shift = alphabet[i:] + alphabet[:i]
        enctemp = encrypted.translate(str.maketrans(alphabet, alphabet_shift))
        try:
            text = base64.b64decode(enctemp.encode('utf8')).decode('utf8')
        except:
            print ("error")
        i += 1
        print (i)
    return text
temp = findNextPlain(encrypted)
while "{" not in temp:
    temp = findNextPlain(temp)
out = open('out.txt','w')
out.write(temp)
out.close()

```


### Flag ###

    sctf{thank_you_based_64}
