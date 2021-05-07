import random


def prime_test(N, k):
    return run_fermat(N, k), run_miller_rabin(N, k)


def mod_exp(x, y, N):
    if y == 0:
        return 1
    z = mod_exp(x, y // 2, N)
    if y % 2 == 0:
        return z ** 2 % N
    else:
        return x * (z ** 2) % N


def fprobability(k):
    return 1 - 1 / (2 ** k)


def mprobability(k):
    return 1 - (4 ** k)


def run_fermat(N, k=200):
    for i in range(0, k):
        a = random.randint(1, N - 1)
        if mod_exp(a, N - 1, N) != 1:
            return "composite"
    return "prime"


def b_helper(b, power, n):
    b_n = mod_exp(b, power, n)
    if b_n % 2 == 0:
        return "composite"
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
