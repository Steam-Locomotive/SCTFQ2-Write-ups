## Obfuscat - 130 (Web Exploitation) ##
#### Writeup by Oksisane

### Problem ###

Ready for some obfus-cat-ion? ;) Have fun: [http://obfuscat.problem.sctf.io](http://obfuscat.problem.sctf.io)

### Hint ###

It's a static HTML file. There's no server-side games being played here.

## Answer ##

### Overview ###

Figure out the string corresponding to the final hash check and work backwards
### Details ###
Checking the source of the page, the following comment seems suspicious: 
```
// http://md5online.net
```

At the end of the JavaScript the final check which determines if the input is valid compares a string to the md5 hash `0f957300a52431c2d0de0da9fc7223c9`

```javascript

if (CryptoJS.MD5(string).toString() == "0f957300a52431c2d0de0da9fc7223c9") {
	document.getElementById("message").innerHTML = "Correct!";
} else {
	throw Error();
}
```

Running this hash through [md5online.net](http://md5online.net/) gives the string `r3v3rse_th1s_str1ng`. After this, the only challenge left is to reverse the JavaScript provided such that the `string`  variable is set to `r3v3rse_th1s_str1ng`. 

Let's begin.

The first step for any JavaScript obfuscation challenge is to make the source code easier to read, adding line breaks and braces where needed.
[jsbeautifier](http://jsbeautifier.org/) outputs [this source](obfuscat/obfuscat.js) which is a lot cleaner. 

Another hint added later in the competition tells us the flag format is `flag{xxxxxxxxxxxxxxxxxx}`. The code:
```js
 var query = location.search.substring(1).split(/{|}/);
 if (query[0] != "flag") throw Error();
    // flag format: flag{xxxxxxxxxxxxxxxxxx}
 if (query[2]) throw Error();
 var message = ("The " + query[0] + " is a string.").split(" ");
 var query2 = query[1].split("$");
```
will split the flag string such that `xxxxxxxxxxxxxxxxxx` is set to `query[2]`. `query[0]` is set to `flag`, and `message` is set to `["The","flag","is","a","string"]` due to the `.split(" "). The next line,
```js
var query2 = query[1].split("$");
```
splits the flag string, `xxxxxxxxxxxxxxxxxx` based on the character `$`. This array becomes very important later in the problem. Another hint states that `Only query2[8] has more than one character`, so we can construct the flag like this: `flag(x$x$x$x$x$x$x$x$xx)`.

The rest of this problem will be filling in these 9 sections of the flag. The next piece of code is interesting.
```js
if (query2[8].split("").map(function(k) {
    return k.charCodeAt(0);
}).reduce(function(y, n) {
    return y + Math.pow(n ^ 95, 4);
}) != 0x2f7b81) throw Error();
```
Given that `query2[8]` is two characters the function can be essentially simplified to:
```python
char2 + (char1 ^ 95)**4
```
where `^` is the `xor` function. The following python script guesses characters until they satisfy the condition
```python
for a in range(33,126):
    for b in range(33,126):
        if 0x2f7b81 == (a + (b^95)**4):
            print chr(a) + " " + chr(b)
```
The output of this code function is `qu`, giving us the first piece of the flag!



### Flag ###

    flag{S$z$e$P$t$@$s$r$qu}
