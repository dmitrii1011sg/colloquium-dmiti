import random

import pytest
from core.base.Integer import Integer
from core.base.Natural import Natural
from core.modules.ZModule.TRANS_N_Z import TRANS_N_Z


def test_trans_n_z():
    n1 = Natural.from_str("777")
    n2 = Natural.from_str("4664")
    n3 = Natural.from_str("100")
    assert str(TRANS_N_Z(n1)) == "777"
    assert str(TRANS_N_Z(n2)) == "4664"
    assert str(TRANS_N_Z(n3)) == "100"


@pytest.mark.parametrize("iteration", range(5))
def test_trans_n_z_random(iteration):
    val = random.randint(0, 10**50)
    n = Natural.from_int(val)
    result = TRANS_N_Z(n)
    assert str(result) == str(val)


def test_trans_n_z_huge_numbers():
    base_str = "9" * 10000
    n = Natural.from_str(base_str)
    result = TRANS_N_Z(n)
    assert str(result) == base_str


def test_trans_n_z_no_mutation():
    n = Natural.from_str("456")
    original_digits = list(n.digits)
    original_length = n.length
    _ = TRANS_N_Z(n)
    assert n.digits == original_digits
    assert n.length == original_length


def test_invalid_input():
    n1 = Integer.from_int(-1025)

    with pytest.raises(ValueError, match="Invalid value"):
        TRANS_N_Z(n1)  # type: ignore
