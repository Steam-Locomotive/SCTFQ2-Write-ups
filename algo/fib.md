## Fibonacci_Not! - 65 (Algorithmic) ##
#### Writeup by GenericNickname

Created: 2015-12-08

### Problem ###


What would be a CTF without a typical algorithm problem? This will test your system more than anything. Seeing as the Fibonacci sequence is overused, lets change it slightly shall we?

```
Given F(x) = G(x) - W(x)

G(x) = [G(x-1)+G(x-2)]^2

W(x) = [W(x-1)]^2 + [W(x-2)]^2
```

What is the sum of the digits of F(30)?

```
G(0) = 0 G(1) = 1

W(0) = 0 W(1) = 1
```

## Answer ##

### Overview ###

Implement the algorithm and calculate the answer.

### Details ###

I chose to use python for this, and simply implemented the math using recursion:
```python
import time,math

def g(x) :
    print x
    if x == 0 : return 0
    if x == 1 : return 1
    a = g(x - 1)
    b = g(x - 2)
    res = (a + b) * (a + b)
    return res

def w(x) :
    print x
    if x == 0 : return 0
    if x == 1 : return 1
    a = w(x - 1)
    b = w(x - 2)
    res = a * a + b * b
    return res

def f(x) :
    return g(x) - w(x)

def sum_digits(n):
    s = 0
    count = 0
    while n:
        s += n % 10
        n /= 10
        count += 1
        print count
    return s

num = f(30)
print sum_digits(num)
```
Unfortunately, this was taking way too long to run (the number would calculate but python was taking to long to count the digits), so we decided to switch to using sage. The only difference in the sage code was that
```python
num = f(30)
print sum_digits(num)
```
became
```python
num = f(30)
digits = num.digits()
print len(digits)
print sum(digits)
```

The sage script, which can be downloaded [here](/algo/fibonacci_not/fib_not.sage) finished the calculations in less than a minute. The script told us that the number had `98574916` digits which summed to `443589491`, which is correct!

### Flag ###

    443589491
