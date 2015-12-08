## Obfuscat - 130 (Web Exploitation) ##
#### Writeup by Oksisane

### Problem ###

Ready for some obfus-cat-ion? ;) Have fun: [http://obfuscat.problem.sctf.io](http://obfuscat.problem.sctf.io)

### Hint ###

It's a static HTML file. There's no server-side games being played here.

## Answer ##

### Overview ###

Figure out the string corresponding to the final hash check and work backwards to construct the flag
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

####Initial Steps
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

The rest of this problem will be filling in these 9 sections of the flag. 


####Query2[8]
The next piece of code is interesting.
```js
if (query2[8].split("").map(function(k) {
    return k.charCodeAt(0);
}).reduce(function(y, n) {
    return y + Math.pow(n ^ 95, 4);
}) != 0x2f7b81) throw Error();
```
Given that `query2[8]` is two characters the function can be essentially simplified to:
```python
char1 + (char2 ^ 95)**4
```
where `^` is the `xor` function. The following python script guesses characters until they satisfy the condition
```python
for a in range(33,126):
    for b in range(33,126):
        if 0x2f7b81 == (a + (b^95)**4):
            print chr(a) + " " + chr(b)
```
The output of this code function is `qu`, giving us the first piece of the flag!

The next section of the code performs some functions on the `message` variable. Since we already know the contents of message we can figure out the value of the three variables by running the code on the message and breakpointing the result. `h.words` turns out to be equal to `[108211444, 434422999, -821768299]`, and will be used later. We can ignore the other two variables since they are never used in the code. Some functions put in the array `funcs` next, which we will need later in the challenge.

####MersenneTwister
The next section of the code creates a `MersenneTwister` object. A Mersenne Twister is a way of generating random numbers based off a seed value. Crucially, if the `MersenneTwister` is seeded with the same value it will always return the same numbers in the same order. 

Looking at this code:
```js
var m = new MersenneTwister((funcs[0] + "" [~~(query2[0] / 21)]).split(/\s/).join("").split("").map(function(x) {
    return x.charCodeAt(0);
}).reduce(function(a, b) {
    return a + b;
}) + 0xa0);
```
there is only one portion of our input mentioned, `query2[0]`. However, even this is misleading because `~~(query2[0] / 21)])` always evaluates to 0 since `query2[0]` is a string. Thus, the whole instantiation of the object can be simplified to 
```js
var m = new MersenneTwister(4744)
```
Progress!

####String
At last we come to the construction of the string variable. The variable seems to be made up of 3 parts, joined together with a delimiter between them. Sound familiar? The 3 parts are very likely the three words of the string we found at the start, `r3v3rse_th1s_str1ng` with the delimiter `_`. Since the code used to delimit is 
```js
[stringarray].join(funcs[0](query2[3].charCodeAt(0) + 0xF));
```
we need a character that when added to 16 (0xF) equals `_`. It turns out this is P, so that is the value of `query2[3]`.

The last step that remains is reversing each of the three indexes used to make `r3v3rse`, `th1s`, and `str1ng`.

In case you want to keep track, so far we have filled in two of the 9 indexes of the flag, making the current string
`flag{x$x$x$P$x$x$x$x$qu}`
####r3v3rse
The code we are given for the first index of string is:
```js
(function(n) {
return n.split("").map(funcs[query2[5].charCodeAt(0) ^ 66]).join("") + n.charAt(query2[6].charCodeAt(0) - query2[7].charCodeAt(0));
            })(funcs[1](Array.prototype).sort()[query2[1].charCodeAt(0) - 0x65].substring(0, 6))
```
The code executes a function based on the input 
```js
funcs[1](Array.prototype).sort()[query2[1].charCodeAt(0) - 0x65].substring(0, 6)
```
`funcs[1]` is `Object.getOwnPropertyNames`. Running this on `Array.prototype` and sorting the output gives:
```
["concat", "constructor", "copyWithin", "entries",
"every", "fill", "filter", "find", "findIndex", "forEach",
"includes", "indexOf", "join", "keys", "lastIndexOf",
"length", "map", "pop", "push", "reduce", "reduceRight",
"reverse", "shift", "slice", "some", "sort", "splice",
"toLocaleString", "toString", "unshift"]
```
We can see `reverse` at the `21st` index of the array. This must be how the function gets the string `r3vers3`! Since the code gets the element 
```js
query2[1].charCodeAt(0) - 0x65]
```
from the array, we can compute `21+64`, which is `z` if converted to ASCII! This is the value of `query2[1]`.
Next we analyze the function this is called on (keep in mind `substring(0,6)` which only gives us the first 6 characters of reverse):
```js
function(n) one {
    return n.split("").map(funcs[query2[5].charCodeAt(0) ^ 66]).join("") + n.charAt(query2[6].charCodeAt(0) - query2[7].charCodeAt(0));
}
one("revers")
```
The function calls `funcs[query2[5].charCodeAt(0) ^ 66]` on each character of our input. Looking at the list of functions in `func`, `func[2]` is most likely the function being called since it returns a character. Thus, `query2[5].charCode(0) ^ 66` must be equal 2 to. Solving for `query2[5]` gives us `@` as the character!

Looking at `func[2]`, we can see it returns either the input character or `3` if the input equals `query2[2]`. This is most likely how our string `revers` has `e` replaced with three. This gives us `query2[2]`!  Finally, the function adds the character 
```js
n.charAt(query2[6].charCodeAt(0) - query2[7].charCodeAt(0))
```
the string `r3v3rs`. This must be how the gets the `e` added back on! Since it is not immediately clear what the values of the two variables in `query2[6].charCodeAt(0) - query2[7].charCodeAt(0)` actually are (we can only figure out the difference between them), we will come back to this later.

Our flag is now:
`flag{x$z$e$P$x$@$x$x$qu}`

We also know that the ASCII values of `query2[6]` and `query2[7]` are either 1 or 4 apart (indexes of the e in the string `revers`)
####th1s
We start off the word `th1s` with this code:
```js
funcs[query2[8].charCodeAt(1) - 0x72](function(m, n) {
    return m + (funcs[0](n ^ h.words.splice(0, 1) & 0xff));
}
```
Since we already know the value of `query2[8]` and `q` we can simplify this to:
```js
funcs[3](function(m, n) {
    return m + (funcs[0](n ^ h.words.splice(0, 1) & 0xff));
}
```
replacing `func[3]` with the actual function yeilds this.
```js
[query2[4], 0x9c, 0xe6, ~~(query2[6].charCodeAt(0) *
2)].reduce(function(m, n) {
    return m + (funcs[0](n ^ h.words.splice(0, 1) &
    0xff));
```
Another reduce, this time with multiple arguments! If you are unfamiliar with reduce, you can read up about it [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/Reduce). Remember `h.words` we used earlier? The numbers, `[108211444, 434422999, -821768299]` will finally come into use here. We first notice that the reduce function performs an operation on a set of 4 integers to create the string `th1s`. The first character, `query2[4]` is used to start the string. That means `query2[4]` must be equal to `t`! 

Next, the characters `h` and `1` are generated from the calculation `funcs[0](n ^ h.words.splice(0, 1)`. Each time this is performed, a number is removed from `h.words`. Finally, the same calculation is run on the last character, `query2[6].charCodeAt(0) * 2`. Since we know what the final character must be, we can construct the equation
```
(n ^ -821768299 & 0xff)/2 = query2[6]
```
This gives us 115, or `s` in ascii, the value of `query2[6]`! Using what we discovered above we also know that `query2[7]` is either one more than `query2[6]` (`r`) or 4 more (`w`).

Our flag is now 
`flag{x$z$e$P$t$@$s$r$qu}`
####str1ng
Running the function
```js
[181, 78, 28, query2[0].charCodeAt(0), 225, 129].map(function(x) {
	  return funcs[0](((m.genrand_int32() * Math.sqrt(m.random())) & 0xff) ^ x);
```

we can see that it generates the first three characters, `str` based off the seed provided. MersenneTwister will generate the same numbers in the same order based on the seed (which we know is `4744`). So, we need the output of the 7th and 8th usages of the random function to give the `1` in `str1ng`. Evaluating this quick script gave us the answer:
```js
function threeSolve(guess){
	var m = new MersenneTwister(4744);
	var three = [181, 78, 28, guess, 225, 129].map(function(x) {
			return String.fromCharCode(((m.genrand_int32() * Math.sqrt(m.random())) & 0xff) ^ x);
	}).join("");
	return three
}
for (var i = 0; i < 255; i++){
    if (threeSolve(i) == '1'){
        console.log(i)
    }
}
```
which gave the output `83` or `S`. We now have all the characters needed for the flag! If we navigate to [http://obfuscat.problem.sctf.io?flag{S$z$e$P$t$@$s$r$qu}](http://obfuscat.problem.sctf.io?flag{S$z$e$P$t$@$s$r$qu}) we can verify the flag is correct!
### Flag ###

    flag{S$z$e$P$t$@$s$r$qu}
