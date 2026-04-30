import random

import pytest
from core.base.Integer import Integer
from core.modules.ZModule.DIV_ZZ_Z import DIV_ZZ_Z
from core.modules.ZModule.MOD_ZZ_Z import MOD_ZZ_Z
from core.modules.ZModule.MUL_ZZ_Z import MUL_ZZ_Z
from core.modules.ZModule.SUB_ZZ_Z import SUB_ZZ_Z


def test_MOD_ZZ_Z():
    a = Integer.from_str("100")
    b = Integer.from_str("3")
    c = Integer.from_str("-4")
    d = Integer.from_str("-20")
    e = Integer.from_str("7")

    assert str(MOD_ZZ_Z(a, b)) == "1"
    assert str(MOD_ZZ_Z(a, c)) == "0"
    assert str(MOD_ZZ_Z(d, c)) == "0"
    assert str(MOD_ZZ_Z(e, b)) == "1"


@pytest.mark.parametrize("iteration", range(10))
def test_MOD_ZZ_Z_random(iteration):
    val2 = random.randint(1, 10**50)

    if random.choice([True, False]):
        val2 = -val2

    val1 = random.randint(-(10**50), 10**50)

    a = Integer.from_int(val1)
    b = Integer.from_int(val2)

    expected = val1 % val2
    assert int(MOD_ZZ_Z(a, b)) == expected


def test_MOD_ZZ_Z_huge_numbers():
    huge_str = "1" + "0" * 1000
    a = Integer.from_str(huge_str)
    b = Integer.from_str("3")
    c = Integer.from_str("-3")

    assert str(MOD_ZZ_Z(a, b)) == "1"
    assert str(MOD_ZZ_Z(a, c)) == "-2"


def test_MOD_ZZ_Z_sign_cases():
    assert str(MOD_ZZ_Z(Integer.from_str("10"), Integer.from_str("3"))) == "1"
    assert str(MOD_ZZ_Z(Integer.from_str("-10"), Integer.from_str("3"))) == "2"
    assert str(MOD_ZZ_Z(Integer.from_str("10"), Integer.from_str("-3"))) == "-2"
    assert str(MOD_ZZ_Z(Integer.from_str("-10"), Integer.from_str("-3"))) == "-1"


def test_MOD_ZZ_Z_zero_cases():
    a = Integer.from_int(42)
    zero = Integer.from_int(0)

    with pytest.raises(ValueError):
        MOD_ZZ_Z(a, zero)

    b = Integer.from_int(7)
    c = Integer.from_int(42)
    assert int(MOD_ZZ_Z(c, b)) == 0


def test_MOD_ZZ_Z_mod_less_than_divisor():
    a = Integer.from_str("3")
    b = Integer.from_str("10")

    assert str(MOD_ZZ_Z(a, b)) == "3"

    a_neg = Integer.from_str("-3")
    assert str(MOD_ZZ_Z(a_neg, b)) == "7"


def test_MOD_ZZ_Z_property():
    for _ in range(20):
        val2 = random.randint(1, 1000)
        if random.choice([True, False]):
            val2 = -val2

        val1 = random.randint(-10000, 10000)

        a = Integer.from_int(val1)
        b = Integer.from_int(val2)

        q = DIV_ZZ_Z(a, b)
        r = MOD_ZZ_Z(a, b)

        assert int(SUB_ZZ_Z(a, MUL_ZZ_Z(b, q))) == int(r)


def test_MOD_ZZ_Z_no_mutation():
    a = Integer.from_str("456")
    b = Integer.from_str("123")
    orig_a_digits = list(a.number.digits)
    orig_b_digits = list(b.number.digits)
    _ = MOD_ZZ_Z(a, b)
    assert a.number.digits == orig_a_digits
    assert b.number.digits == orig_b_digits
