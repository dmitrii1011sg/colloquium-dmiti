import random

import pytest
from core.base.Integer import Integer
from core.modules.ZModule.SUB_ZZ_Z import SUB_ZZ_Z


def test_SUB_ZZ_Z():
    a = Integer.from_str("100")
    b = Integer.from_str("50")
    c = Integer.from_str("-30")
    d = Integer.from_str("-70")
    e = Integer.from_str("100")

    assert str(SUB_ZZ_Z(a, b)) == "50"
    assert str(SUB_ZZ_Z(a, e)) == "0"
    assert str(SUB_ZZ_Z(b, c)) == "80"
    assert str(SUB_ZZ_Z(c, d)) == "40"
    assert str(SUB_ZZ_Z(a, d)) == "170"


@pytest.mark.parametrize("iteration", range(10))
def test_SUB_ZZ_Z_random(iteration):
    val1 = random.randint(-(10**50), 10**50)
    val2 = random.randint(-(10**50), 10**50)

    a = Integer.from_int(val1)
    b = Integer.from_int(val2)

    expected = val1 - val2
    assert int(SUB_ZZ_Z(a, b)) == expected


def test_SUB_ZZ_Z_huge_numbers():
    huge_str = "1" + "0" * 10000
    a = Integer.from_str(huge_str)
    b = Integer.from_str("1")
    assert str(SUB_ZZ_Z(a, b)) == "9" * 10000

    a_neg = Integer.from_str("-" + huge_str)
    b_neg = Integer.from_str("-1")
    assert str(SUB_ZZ_Z(a_neg, b_neg)) == "-" + "9" * 10000


def test_SUB_ZZ_Z_sign_cases():
    assert str(SUB_ZZ_Z(Integer.from_str("10"), Integer.from_str("3"))) == "7"
    assert str(SUB_ZZ_Z(Integer.from_str("3"), Integer.from_str("10"))) == "-7"
    assert str(SUB_ZZ_Z(Integer.from_str("-10"), Integer.from_str("-3"))) == "-7"
    assert str(SUB_ZZ_Z(Integer.from_str("-3"), Integer.from_str("-10"))) == "7"
    assert str(SUB_ZZ_Z(Integer.from_str("10"), Integer.from_str("-3"))) == "13"
    assert str(SUB_ZZ_Z(Integer.from_str("-10"), Integer.from_str("3"))) == "-13"


def test_SUB_ZZ_Z_zero_cases():
    a = Integer.from_int(42)
    b = Integer.from_int(-42)
    zero = Integer.from_int(0)

    assert int(SUB_ZZ_Z(a, zero)) == 42
    assert int(SUB_ZZ_Z(zero, a)) == -42
    assert int(SUB_ZZ_Z(zero, b)) == 42
    assert int(SUB_ZZ_Z(zero, zero)) == 0


def test_SUB_ZZ_Z_no_mutation():
    a = Integer.from_str("456")
    b = Integer.from_str("123")
    orig_a_digits = list(a.number.digits)
    orig_b_digits = list(b.number.digits)
    _ = SUB_ZZ_Z(a, b)
    assert a.number.digits == orig_a_digits
    assert b.number.digits == orig_b_digits
