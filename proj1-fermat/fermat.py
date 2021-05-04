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
    return 0.0


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


def run_miller_rabin(N, k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    return 'composite'
