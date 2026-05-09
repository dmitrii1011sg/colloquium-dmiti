import random

import pytest
from core.base.Integer import Integer
from core.modules.ZModule.DIV_ZZ_Z import DIV_ZZ_Z


def test_DIV_ZZ_Z():
    a = Integer.from_str("100")
    b = Integer.from_str("3")
    c = Integer.from_str("-4")
    d = Integer.from_str("-20")

    assert str(DIV_ZZ_Z(a, b)) == "33"
    assert str(DIV_ZZ_Z(a, c)) == "-25"
    assert str(DIV_ZZ_Z(d, c)) == "5"
    assert str(DIV_ZZ_Z(c, a)) == "-1"


@pytest.mark.parametrize("iteration", range(10))
def test_DIV_ZZ_Z_random(iteration):
    val1 = random.randint(-(10**50), 10**50)
    val2 = random.randint(1, 10**50)

    if random.choice([True, False]):
        val2 = -val2

    a = Integer.from_int(val1)
    b = Integer.from_int(val2)

    expected = val1 // val2
    assert int(DIV_ZZ_Z(a, b)) == expected


def test_DIV_ZZ_Z_huge_numbers():
    huge_str = "1" + "0" * 1000
    a = Integer.from_str(huge_str)
    b = Integer.from_str("2")
    c = Integer.from_str("-2")

    expected = "5" + "0" * 999
    assert str(DIV_ZZ_Z(a, b)) == expected
    assert str(DIV_ZZ_Z(a, c)) == "-" + expected


def test_DIV_ZZ_Z_sign_cases():
    assert str(DIV_ZZ_Z(Integer.from_str("10"), Integer.from_str("3"))) == "3"
    assert str(DIV_ZZ_Z(Integer.from_str("-10"), Integer.from_str("3"))) == "-4"
    assert str(DIV_ZZ_Z(Integer.from_str("10"), Integer.from_str("-3"))) == "-4"
    assert str(DIV_ZZ_Z(Integer.from_str("-10"), Integer.from_str("-3"))) == "3"


def test_DIV_ZZ_Z_division_by_zero():
    a = Integer.from_int(42)
    zero = Integer.from_int(0)

    with pytest.raises(ValueError):
        DIV_ZZ_Z(a, zero)


def test_DIV_ZZ_Z_small_dividend():
    a = Integer.from_str("3")
    b = Integer.from_str("10")
    c = Integer.from_str("-10")

    assert int(DIV_ZZ_Z(a, b)) == 0
    assert int(DIV_ZZ_Z(a, c)) == -1
    assert int(DIV_ZZ_Z(Integer.from_str("-3"), b)) == -1


def test_DIV_ZZ_Z_no_mutation():
    a = Integer.from_str("456")
    b = Integer.from_str("123")
    orig_a_digits = list(a.number.digits)
    orig_b_digits = list(b.number.digits)
    _ = DIV_ZZ_Z(a, b)
    assert a.number.digits == orig_a_digits
    assert b.number.digits == orig_b_digits
