import math

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

num = f(30)
digits = num.digits()
print len(digits)
print sum(digits)