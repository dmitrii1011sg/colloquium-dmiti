import random

import pytest
from core.base.Natural import Natural
from core.modules.ADD_1N_N import ADD_1N_N


def test_add_1n_n():
    n1 = Natural.from_str("0")
    n2 = Natural.from_str("5")
    n3 = Natural.from_str("99")
    assert str(ADD_1N_N(n1)) == "1"
    assert str(ADD_1N_N(n2)) == "6"
    assert str(ADD_1N_N(n3)) == "100"


@pytest.mark.parametrize("iteration", range(5))
def test_add_1n_n_random(iteration):
    val = random.randint(0, 10**50)
    n = Natural.from_int(val)
    result = ADD_1N_N(n)
    assert str(result) == str(val + 1)


def test_add_1n_n_huge_numbers():
    base_str = "9" * 10000
    n = Natural.from_str(base_str)
    result = ADD_1N_N(n)
    assert str(result) == "1" + "0" * 10000


def test_add_1n_n_extreme_cases():
    n_zero = Natural.from_int(0)
    n_huge = Natural.from_str("1" + "0" * 1000)
    assert str(ADD_1N_N(n_zero)) == "1"
    assert str(ADD_1N_N(n_huge)) == "1" + "0" * 999 + "1"


def test_add_1n_n_carry_chain():
    n1 = Natural.from_str("9")
    n2 = Natural.from_str("999")
    n3 = Natural.from_str("1999999999999")
    assert str(ADD_1N_N(n1)) == "10"
    assert str(ADD_1N_N(n2)) == "1000"
    assert str(ADD_1N_N(n3)) == "2000000000000"


def test_add_1n_n_no_mutation():
    n = Natural.from_str("123")
    original_digits = list(n.digits)
    original_length = n.length
    _ = ADD_1N_N(n)
    assert n.digits == original_digits
    assert n.length == original_length
