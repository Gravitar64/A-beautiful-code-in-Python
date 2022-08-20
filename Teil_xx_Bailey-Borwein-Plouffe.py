import math
from decimal import Decimal, getcontext
from time import perf_counter as pfc
from time import time


def pi(precision):
    getcontext().prec=precision
    return sum(1/Decimal(16)**k * 
        (Decimal(4)/(8*k+1) - 
         Decimal(2)/(8*k+4) - 
         Decimal(1)/(8*k+5) -
         Decimal(1)/(8*k+6)) for k in range (precision))

def sqrt(n, one):
    """
    Return the square root of n as a fixed point number with the one
    passed in.  It uses a second order Newton-Raphson convgence.  This
    doubles the number of significant figures on each iteration.
    """
    # Use floating point arithmetic to make an initial guess
    floating_point_precision = 10**16
    n_float = float((n * floating_point_precision) // one) / floating_point_precision
    x = (int(floating_point_precision * math.sqrt(n_float)) * one) // floating_point_precision
    n_one = n * one
    while 1:
        x_old = x
        x = (x + n_one // x) // 2
        if x == x_old:
            break
    return x

def pi_chudnovsky(one):
    """
    Calculate pi using Chudnovsky's series

    This calculates it in fixed point, using the value for one passed in
    """
    k = 1
    a_k = one
    a_sum = one
    b_sum = 0
    C = 640320
    C3_OVER_24 = C**3 // 24
    while 1:
        a_k *= -(6*k-5)*(2*k-1)*(6*k-1)
        a_k //= k*k*k*C3_OVER_24
        a_sum += a_k
        b_sum += k * a_k
        k += 1
        if a_k == 0:
            break
    total = 13591409*a_sum + 545140134*b_sum
    pi = (426880*sqrt(10005*one, one)*one) // total
    return pi

def calcPi():
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    while True:
        if 4*q+r-t < n*t:
            yield n
            nr = 10*(r-n*t)
            n  = ((10*(3*q+r))//t)-10*n
            q  *= 10
            r  = nr
        else:
            nr = (2*q+r)*l
            nn = (q*(7*k)+2+(r*l))//(t*l)
            q  *= k
            t  *= l
            l  += 2
            k += 1
            n  = nn
            r  = nr    


ANZ = 1_000_000

# start = pfc()
# print(pi(ANZ))
# print(pfc()-start)

start = pfc()
print(pi_chudnovsky(10**ANZ))
print(pfc()-start)

# start = pfc()
# pi = calcPi()
# i = 0
# for d in pi:
#   print(str(d),end='')
#   i += 1
#   if i > ANZ: break
# print('\n',pfc()-start)
