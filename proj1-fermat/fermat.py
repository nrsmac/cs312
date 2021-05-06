import math
import random


def prime_test(N, k):
    # This is the main function connected to the Test button. You don't need to touch it.
    return run_fermat(N, k), run_miller_rabin(N, k)


def mod_exp(x, y, N):
    # You will need to implement this function and change the return value.
    if y == 0: return 1
    z = mod_exp(x, y // 2, N)
    if y % 2 == 0:
        return z ** 2 % N
    else:
        return x * (z ** 2) % N
    return 1


def fprobability(k):
    # You will need to implement this function and change the return value.   
    return 1-1/(2**k)

def mprobability(k):
    # You will need to implement this function and change the return value.   
    return 4**(-k) 


def run_fermat(N, k=200):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    is_prime = True

    a = []
    for a_n in range(0, k):
        a.append(random.randint(1, N - 1))
    for i in range(0, k):
        if a[i] ** (N - 1) % N != 1 % N:
            is_prime = False

    if is_prime:
        return "prime"
    else:
        return "composite"



def factor(n,k=1):
    m = (n-1)/2**k
    if m%1 != 0:
        return k-1, (n-1)/2**(k-1)
    else:
        return factor(n,k+1)

def b_helper(b,n):
    b_n = b**2 % n
    if b_n == 1:
        return "composite"
    elif b_n == -1:
        return "prime"
    else:
        return b_helper(b_n,n)

def run_miller_rabin(N, k): 
    k,m = factor(N)
    a = random.randint(2,N-2)
    b_0 = (a**m)%N
    if b_0 == 1 or b_0 == -1:
        return "prime"
    else:
        return b_helper(b_0,N)

