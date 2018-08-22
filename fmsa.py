from collections import namedtuple


def itoa(i: int) -> list:
    """
    Converts an integer into a list.
    """
    b = bin(i)[2:]  # remove 0b prefix
    return list(map(int, reversed(b)))


def atoi(A: list) -> int:
    """
    atoi(itoa(x)) == x
    """
    i = 0
    for x in reversed(A):
        i *= 2
        i += x
    return i


def pad(A: list, n: int) -> list:
    """
    Pad A with zeroes to make sure that the length of the return value
    is a multiple of n.
    """
    r = len(A) % n
    return A + [0] * (n - r)


def mul(s: int, p: int) -> int:
    """
    Multiply two numbers s and p together naively. Assumes that s is big
    and p is small.
    """
    r = 0
    for x in reversed(itoa(s)):
        r *= 2
        if x == 1:
            r += p
    return r


def mul_w(s: int, p: int) -> int:
    """
    Multiply two numbers s and p using the window method.
    """

    # convert s into windows of 4
    # e.g. 0001 0010 0011 1011
    #   => 0001 0002 0003 000b
    S = pad(itoa(s), 4)
    n = len(S)
    for i in range(0, n // 4):
        S[i * 4] = (S[i * 4]
                    + 2 * S[i * 4 + 1]
                    + 4 * S[i * 4 + 2]
                    + 8 * S[i * 4 + 3])
        S[i * 4 + 1] = 0
        S[i * 4 + 2] = 0
        S[i * 4 + 3] = 0

    # build lookup table
    px = [0] * 16
    for i in range(1, 15 + 1):
        px[i] = px[i-1] + p

    r = 0
    for x in reversed(S):
        r *= 2
        if x != 0:
            r += px[x]
    return r


def mul_sw(s: int, p: int) -> int:
    """
    Multiply two numbers s and p using the sliding window method.
    """

    # add 3 more bits so in case the MSB = 1, we have enough
    # space to store 3 more 0s. we want to ignore the extra
    # padding bits as well
    S = pad(itoa(s), 4) + [0] * 3
    n = len(S) - 3
    for i in range(0, n):
        if S[i] == 1:
            S[i] = (S[i]
                    + 2 * S[i + 1]
                    + 4 * S[i + 2]
                    + 8 * S[i + 3])
            S[i + 1] = 0
            S[i + 2] = 0
            S[i + 3] = 0

    # build lookup table
    px = [0] * 16
    for i in range(1, 15 + 1):
        px[i] = px[i-1] + p

    r = 0
    for x in reversed(S):
        r *= 2
        if x != 0:
            r += px[x]
    return r


def mul_naf(s: int, p: int) -> int:
    """
    Multiplies s and p by first converting s into non-adjacent form.
    """
    S = itoa(s) + [0]
    n = len(S)
    for i in range(0, n):
        if S[i] == 1 and S[i+1] == 1:
            S[i] = -1
            j = i
            while S[j] == 1:
                S[j] = 0
                j += 1
            S[j] = 1

    r = 0
    for x in reversed(S):
        r *= 2
        if x ==  1: r += p
        if x == -1: r -= p
    return r


def mul_ssw(s: int, p: int) -> int:
    """
    Multiplies s and p by first converting s into signed sliding windows form.
    """
    # similar to mul_sw but we need to add 4 bits because we may
    # propagate a carry into the extra 4th bit.
    S = pad(itoa(s), 4) + [0] * 4
    n = len(S) - 4
    for i in range(1, n):
        if S[i] != 0:
            S[i] = S[i] + 2 * S[i+1] + 4 * S[i+2] + 8 * S[i+3]
            S[i + 1] = 0
            S[i + 2] = 0
            S[i + 3] = 0
            if S[i] > 8:
                # MSB == 1 so need to propagate a carry
                # and do 2**4 - window (similar concept
                # to non adjacent form)
                S[i] -= 16
                j = i + 4
                while S[j] != 0:
                    S[j] = 0
                    j += 1
                S[j] = 1

    # build lookup table
    px = [0] * 16
    for i in range(1, 15 + 1):
        px[i] = px[i-1] + p

    r = 0
    for x in reversed(S):
        r *= 2
        if x > 0: r += px[x]
        if x < 0: r -= px[-x]
    return r


UCombTable = namedtuple('UCombTable', 'n,p,px')


def compute_ucomb_table(p: int, n: int) -> UCombTable:
    """
    Computes an unsigned lookup table for `p`, suitable for use in `mul_ucomb`.
    n must be a multiple of 4.
    """
    assert n % 4 == 0

    p0 = p
    p1 = p * (2 ** (    n//4))
    p2 = p * (2 ** (2 * n//4))
    p3 = p * (2 ** (3 * n//4))

    px = [0] * 16
    for i in range(1, 15+1):
        u = 0
        if i      % 2 == 1: u += p0
        if (i//2) % 2 == 1: u += p1
        if (i//4) % 2 == 1: u += p2
        if (i//8) % 2 == 1: u += p3
        px[i] = u
    return UCombTable(n, p, px)


def mul_ucomb(s: int, uct: UCombTable) -> int:
    """
    Multiplies `s` and `uct.p` together using a 4-bit comb.
    Note than we must have `s <= (2 ** uct.n - 1)`.
    """
    n, _, px = uct

    assert s <= (2 ** n - 1)

    S = pad(itoa(s), n)
    q = n // 4

    comb = [0] * q
    for i in range(0, q):
        comb[i] = (      S[i        ]
                   + 2 * S[i + q    ]
                   + 4 * S[i + q * 2]
                   + 8 * S[i + q * 3])

    r = 0
    for c in reversed(comb):
        r *= 2
        r += px[c]
    return r
