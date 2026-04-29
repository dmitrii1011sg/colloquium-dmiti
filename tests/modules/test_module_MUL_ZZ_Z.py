import random

import pytest
from core.base.Integer import Integer
from core.modules.ZModule.MUL_ZZ_Z import MUL_ZZ_Z


def test_MUL_ZZ_Z():
    a = Integer.from_str("12")
    b = Integer.from_str("3")
    c = Integer.from_str("-4")
    d = Integer.from_str("-5")

    assert str(MUL_ZZ_Z(a, b)) == "36"
    assert str(MUL_ZZ_Z(a, c)) == "-48"
    assert str(MUL_ZZ_Z(c, d)) == "20"
    assert str(MUL_ZZ_Z(b, d)) == "-15"


@pytest.mark.parametrize("iteration", range(10))
def test_MUL_ZZ_Z_random(iteration):
    val1 = random.randint(-(10**50), 10**50)
    val2 = random.randint(-(10**50), 10**50)

    a = Integer.from_int(val1)
    b = Integer.from_int(val2)

    expected = val1 * val2
    assert int(MUL_ZZ_Z(a, b)) == expected


def test_MUL_ZZ_Z_huge_numbers():
    huge_str = "1" + "0" * 1000
    a = Integer.from_str(huge_str)
    b = Integer.from_str("2")
    expected = "2" + "0" * 1000
    assert str(MUL_ZZ_Z(a, b)) == expected


def test_MUL_ZZ_Z_sign_cases():
    assert str(MUL_ZZ_Z(Integer.from_str("5"), Integer.from_str("3"))) == "15"
    assert str(MUL_ZZ_Z(Integer.from_str("-5"), Integer.from_str("3"))) == "-15"
    assert str(MUL_ZZ_Z(Integer.from_str("5"), Integer.from_str("-3"))) == "-15"
    assert str(MUL_ZZ_Z(Integer.from_str("-5"), Integer.from_str("-3"))) == "15"


def test_MUL_ZZ_Z_zero_cases():
    a = Integer.from_int(42)
    zero = Integer.from_int(0)

    assert int(MUL_ZZ_Z(a, zero)) == 0
    assert int(MUL_ZZ_Z(zero, a)) == 0
    assert int(MUL_ZZ_Z(zero, zero)) == 0


def test_MUL_ZZ_Z_one_cases():
    a = Integer.from_int(42)
    one = Integer.from_int(1)
    neg_one = Integer.from_int(-1)

    assert int(MUL_ZZ_Z(a, one)) == 42
    assert int(MUL_ZZ_Z(a, neg_one)) == -42
    assert int(MUL_ZZ_Z(neg_one, neg_one)) == 1


def test_MUL_ZZ_Z_no_mutation():
    a = Integer.from_str("456")
    b = Integer.from_str("123")
    orig_a_digits = list(a.number.digits)
    orig_b_digits = list(b.number.digits)
    _ = MUL_ZZ_Z(a, b)
    assert a.number.digits == orig_a_digits
    assert b.number.digits == orig_b_digits
