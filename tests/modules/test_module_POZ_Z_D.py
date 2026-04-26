import random
import pytest

from core.base.Integer import Integer
from core.modules.POZ_Z_D import POZ_Z_D


def test_poz_z_d():
    n1 = Integer.from_str("10000")
    n2 = Integer.from_str("-415")
    n3 = Integer.from_str("0")
    assert str(POZ_Z_D(n1)) == "2"
    assert str(POZ_Z_D(n2)) == "1"
    assert str(POZ_Z_D(n3)) == "0"

@pytest.mark.parametrize("iteration", range(5))
def test_poz_z_d_random(iteration):
    val = random.randint(-10**3, 10**50)
    n = Integer.from_int(val)
    result = POZ_Z_D(n)
    if val == 0:
        assert str(result) == "0"
    if val == abs(val):
        assert str(result) == "2"
    else:
        assert str(result) == "1"

def test_poz_z_d_huge_numbers():
    base_str = "9" * 10000
    n = Integer.from_str(base_str)
    result = POZ_Z_D(n)
    assert str(result) == "2"


def test_poz_z_d_extreme_cases():
    n = Integer.from_str("+7156425")
    assert str(POZ_Z_D(n)) == "2"


def test_poz_z_d_no_mutation():
    n = Integer.from_str("555")
    original_digits = list(n.number.digits)
    _ = POZ_Z_D(n)
    assert n.number.digits == original_digits