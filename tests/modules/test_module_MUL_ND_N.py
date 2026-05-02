import random
import sys

import pytest
from core.base.Natural import Natural
from core.modules.NModule.MUL_ND_N import MUL_ND_N

sys.set_int_max_str_digits(20000)


def test_mul_nd_n():
    n1 = Natural.from_str("123")
    d1 = 3
    n2 = Natural.from_str("456")
    d2 = 2
    n3 = Natural.from_str("7")
    d3 = 8

    assert str(MUL_ND_N(n1, d1)) == "369"
    assert str(MUL_ND_N(n2, d2)) == "912"
    assert str(MUL_ND_N(n3, d3)) == "56"


@pytest.mark.parametrize("iteration", range(5))
def test_mul_nd_n_random(iteration):
    val1 = random.randint(0, 10**50)
    val2 = random.randint(0, 9)

    n1 = Natural.from_int(val1)
    d1 = val2

    expected = val1 * val2
    assert str(MUL_ND_N(n1, d1)) == str(expected)


def test_mul_nd_n_huge_numbers():
    base_str = "9" * 10000
    n1 = Natural.from_str(base_str)
    d1 = 9

    expected_str = str(int(base_str) * 9)
    assert str(MUL_ND_N(n1, d1)) == expected_str


def test_extreme_cases():
    n_zero = Natural.from_int(0)
    d_zero = 0
    n_huge = Natural.from_str("1" + "0" * 1000)
    d_one = 1

    assert str(MUL_ND_N(n_huge, d_zero)) == "0"
    assert str(MUL_ND_N(n_zero, d_one)) == "0"
    assert str(MUL_ND_N(n_huge, d_one)) == str(n_huge)


def test_invalid_input():
    n1 = Natural.from_int(10)

    with pytest.raises(ValueError, match="Invalid value"):
        MUL_ND_N(n1, 12)

    with pytest.raises(ValueError, match="Invalid value"):
        MUL_ND_N(n1, "string")