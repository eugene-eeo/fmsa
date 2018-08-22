# fmsa

Toy Python implementation of the algorithms presented in [Fast Multiplication with Slow Additions](http://loup-vaillant.fr/tutorials/fast-scalarmult),
although these routines are admittedly not so fast. Currently the following
algorithms are implemented:

 - `mul` – naive multiplication.
 - `mul_w` – uses windows of size 4.
 - `mul_sw` – uses sliding windows of size 4.
 - `mul_ssw` – uses signed sliding windows of size 4.
 - `mul_naf` – first converts s to non adjacent form.
 - `compute_ucomb_table` – computes an unsigned lookup table.
 - `mul_ucomb` – takes the unsigned lookup table returned by `compute_ucomb_table`
   and multiplies it with another number, using a 4-bit comb. This should only be
   used when `p` doesn't change throughout the lifetime of the program, since
   computing the unsigned lookup table is quite expensive.

All functions are tested with numbers up to `2^128`.

## API

#### `mul(s: int, p: int) -> int`

Returns **s × p**, assuming that **s >> p** (**s** is much larger than **p**),
although this assumption doesn't need to hold true. This is the same signature,
guarantee, and assumption made by all `mul_{...}` functions except for `mul_ucomb`.


#### `compute_ucomb_table(p: int, n: int) -> UCombTable`

Returns an unsigned lookup table for **p**. Assumptions:

 - p ≤ 2<sup>n</sup> - 1
 - n is a multiple of 4


#### `mul_ucomb(s: int, uct: UCombTable) -> int`

Using a 4-bit comb, returns **s × uct.p**. Assumes that:

 - s ≤ 2<sup>uct.n</sup> - 1


## Tests

```sh
$ pip install -r dev-requirements.txt
$ py.test tests.py --cov=fmsa
```
