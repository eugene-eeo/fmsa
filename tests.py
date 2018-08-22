import os
import pytest
from pytest import list_of

from fmsa import *


options = {
    "min_num": 0,
    "max_num": 2**128 - 1,
    "ncalls": int(os.environ.get('FMSA_ROUNDS', '10')),
}


@pytest.mark.randomize(**options)
def test_itoa_atoi(x: int):
    assert atoi(itoa(x)) == x


@pytest.mark.randomize(min_num=1, max_num=100)
def test_pad(a: int, n: int):
    A = pad(itoa(a), n)
    assert atoi(A) == a
    assert len(A) % n == 0


def make_test_mul(func):

    @pytest.mark.randomize(**options)
    def test(s: int, p: int):
        return func(s, p) == s * p

    return test


test_mul     = make_test_mul(mul)
test_mul_w   = make_test_mul(mul_w)
test_mul_sw  = make_test_mul(mul_sw)
test_mul_naf = make_test_mul(mul_naf)
test_mul_ssw = make_test_mul(mul_ssw)


def make_test_ucomb_n(n):
    opts = options.copy()
    opts["max_num"] = 2**n - 1

    @pytest.mark.randomize(**opts)
    def test(s: int, p: int):
        uct = compute_ucomb_table(p, n)
        assert mul_ucomb(s, uct) == s * p

    return test


test_mul_ucomb_8   = make_test_ucomb_n(8)
test_mul_ucomb_16  = make_test_ucomb_n(16)
test_mul_ucomb_32  = make_test_ucomb_n(32)
test_mul_ucomb_64  = make_test_ucomb_n(64)
test_mul_ucomb_128 = make_test_ucomb_n(128)
