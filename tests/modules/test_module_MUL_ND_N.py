import random
import pytest
import sys
from core.base.Natural import Natural
from core.modules.MUL_ND_N import MUL_ND_N

sys.set_int_max_str_digits(20000)

def test_mul_nd_n():
    n1 = Natural.from_str("123")
    d1 = Natural.from_str("3")
    n2 = Natural.from_str("456")
    d2 = Natural.from_str("2")
    n3 = Natural.from_str("7")
    d3 = Natural.from_str("8")

    assert str(MUL_ND_N(n1, d1)) == str(Natural.from_int(369))
    assert str(MUL_ND_N(n2, d2)) == str(Natural.from_int(912))
    assert str(MUL_ND_N(n3, d3)) == str(Natural.from_int(56))


@pytest.mark.parametrize("iteration", range(5))
def test_mul_nd_n_random(iteration):
    val1 = random.randint(0, 10**50)
    val2 = random.randint(0, 9)

    n1 = Natural.from_int(val1)
    d1 = Natural.from_int(val2)

    expected = val1 * val2
    assert str(MUL_ND_N(n1, d1)) == str(Natural.from_int(expected))


def test_mul_nd_n_huge_numbers():
    base_str = "9" * 10000
    n1 = Natural.from_str(base_str)
    d1 = Natural.from_str("9")

    expected_val = int(base_str) * 9
    assert str(MUL_ND_N(n1, d1)) == str(Natural.from_int(expected_val))


def test_extreme_cases():
    n_zero = Natural.from_int(0)
    d_zero = Natural.from_int(0)
    n_huge = Natural.from_str("1" + "0" * 1000)
    d_one = Natural.from_int(1)

    assert str(MUL_ND_N(n_huge, d_zero)) == str(Natural.from_int(0))
    assert str(MUL_ND_N(n_zero, d_one)) == str(Natural.from_int(0))
    assert str(MUL_ND_N(n_huge, d_one)) == str(n_huge)


def test_invalid_input():
    n1 = Natural.from_int(10)
    n2 = Natural.from_int(12)

    with pytest.raises(ValueError, match="Invalid value"):
        MUL_ND_N(n1, n2)

    with pytest.raises(ValueError, match="Invalid value"):
        MUL_ND_N(n1, "string") # type: ignore
