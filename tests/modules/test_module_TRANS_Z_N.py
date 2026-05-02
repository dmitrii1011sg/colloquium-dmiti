import random

import pytest
from core.base.Integer import Integer
from core.base.Natural import Natural
from core.modules.ZModule.TRANS_Z_N import TRANS_Z_N


def test_trans_z_n():
    n1 = Integer.from_str("111")
    n2 = Integer.from_str("228")
    n3 = Integer.from_str("1337")
    assert str(TRANS_Z_N(n1)) == "111"
    assert str(TRANS_Z_N(n2)) == "228"
    assert str(TRANS_Z_N(n3)) == "1337"


@pytest.mark.parametrize("iteration", range(5))
def test_trans_z_n_random(iteration):
    val = random.randint(0, 10**50)
    n = Integer.from_int(val)
    result = TRANS_Z_N(n)
    assert str(result) == str(val)


def test_trans_z_n_huge_numbers():
    base_str = "9" * 10000
    n = Integer.from_str(base_str)
    result = TRANS_Z_N(n)
    assert str(result) == base_str


def test_trans_z_n_extreme_cases():
    n_zero = Integer.from_int(0)
    assert str(TRANS_Z_N(n_zero)) == "0"


def test_trans_z_n_no_mutation():
    n = Integer.from_str("6967")
    original_digits = list(n.number.digits)
    _ = TRANS_Z_N(n)
    assert n.number.digits == original_digits


def test_invalid_input():
    n1 = Natural.from_int(10)
    n2 = Integer.from_int(-25852)

    with pytest.raises(ValueError, match="Invalid value"):
        TRANS_Z_N(n1)  # type: ignore

    with pytest.raises(ValueError, match="Invalid value"):
        TRANS_Z_N(n2)
