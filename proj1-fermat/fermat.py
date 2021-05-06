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


def fprobability(k):
    # You will need to implement this function and change the return value.   
    return 1 - 1 / (2 ** k)


def mprobability(k):
    # You will need to implement this function and change the return value.   
    return 1 - (4 ** (-k))


def run_fermat(N, k=200):
    for i in range(0, k):
        a = random.randint(1, N - 1)
        if mod_exp(a, N - 1, N) != 1:
            # can be prime
            return "composite"
    return "prime"


def b_helper(b, power, n):  # (ranNum, power, N )
    # check if it is even
    # if mod_exp(variables)  ==(N-1) can be prime
    # if mod_exp() return !1 this case can be composite

    b_n = mod_exp(b, power, n)
    if b_n == (n - 1):
        return "prime"
    elif b_n != 1:
        return b_helper(b_n, power // 2, n)


def run_miller_rabin(N, k):
    for i in range(k):
        if N % 2 == 0:
            return "composite"
        a = random.randint(2, N - 2)
        b_0 = mod_exp(a, N - 1, N)
        if b_0 == 1 or b_0 == -1:
            return "prime"
        else:
            return b_helper(b_0, N - 1, N)
