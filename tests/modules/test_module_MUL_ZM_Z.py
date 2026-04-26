import random
import pytest

from core.base.Integer import Integer
from core.modules.MUL_ZM_Z import MUL_ZM_Z


def test_mul_zm_z():
    n1 = Integer.from_str("123")
    n2 = Integer.from_str("-1156")
    n3 = Integer.from_str("-1")
    assert str(MUL_ZM_Z(n1)) == "-123"
    assert str(MUL_ZM_Z(n2)) == "1156"
    assert str(MUL_ZM_Z(n3)) == "1"


@pytest.mark.parametrize("iteration", range(5))
def test_mul_zm_z_random(iteration):
    val = random.randint(-10**3, 10**50)
    n = Integer.from_int(val)
    result = MUL_ZM_Z(n)
    assert str(result) == str(-1*val)


def test_mul_zm_z_huge_numbers():
    base_str = "9" * 10000
    n = Integer.from_str(base_str)
    result = MUL_ZM_Z(n)
    assert str(result) == "-" + base_str


def test_mul_zm_z_extreme_cases():
    n_zero = Integer.from_int(0)
    assert str(MUL_ZM_Z(n_zero)) == "0"


def test_mul_zm_z_no_mutation():
    n = Integer.from_str("6967")
    original_digits = list(n.number.digits)
    _ = MUL_ZM_Z(n)
    assert n.number.digits == original_digits