import random
import pytest

from core.base.Integer import Integer
from core.modules.ABS_Z_N import ABS_Z_N


def test_abs_z_n():
    n1 = Integer.from_str("-67")
    n2 = Integer.from_str("488")
    n3 = Integer.from_str("-99")
    assert str(ABS_Z_N(n1)) == "67"
    assert str(ABS_Z_N(n2)) == "488"
    assert str(ABS_Z_N(n3)) == "99"


@pytest.mark.parametrize("iteration", range(5))
def test_abs_z_n_random(iteration):
    val = random.randint(-10**3, 10**50)
    n = Integer.from_int(val)
    result = ABS_Z_N(n)
    assert str(result) == str(abs(val))


def test_abs_z_n_huge_numbers():
    base_str = "9" * 10000
    n = Integer.from_str(base_str)
    result = ABS_Z_N(n)
    assert str(result) == base_str


def test_abs_z_n_extreme_cases():
    n_zero = Integer.from_int(0)
    assert str(ABS_Z_N(n_zero)) == "0"


def test_abs_z_n_no_mutation():
    n = Integer.from_str("-1488")
    original_digits = list(n.number.digits)
    _ = ABS_Z_N(n)
    assert n.number.digits == original_digits
