import random

import pytest
from core.base.Natural import Natural
from core.modules.ADD_NN_N import ADD_NN_N


def test_ADD_NN_N():
    n1 = Natural.from_str("100")
    n2 = Natural.from_str("50")
    n3 = Natural.from_str("0")
    assert str(ADD_NN_N(n1, n2)) == "150"
    assert str(ADD_NN_N(n2, n1)) == "150"
    assert str(ADD_NN_N(n1, n3)) == "100"


@pytest.mark.parametrize("iteration", range(5))
def test_ADD_NN_N_random(iteration):
    val1 = random.randint(0, 10**50)
    val2 = random.randint(0, 10**50)
    n1 = Natural.from_int(val1)
    n2 = Natural.from_int(val2)
    assert str(ADD_NN_N(n1, n2)) == str(val1 + val2)


def test_ADD_NN_N_huge_numbers():
    base_str = "9" * 10000
    n1 = Natural.from_str(base_str)
    n2 = Natural.from_str("1")
    assert str(ADD_NN_N(n1, n2)) == "1" + "0" * 10000


def test_ADD_NN_N_different_lengths():
    n1 = Natural.from_str("99999")
    n2 = Natural.from_str("1")
    n3 = Natural.from_str("1234")
    n4 = Natural.from_str("5")
    assert str(ADD_NN_N(n1, n2)) == "100000"
    assert str(ADD_NN_N(n3, n4)) == "1239"
    assert str(ADD_NN_N(n4, n3)) == "1239"


def test_ADD_NN_N_zero_cases():
    n_zero = Natural.from_int(0)
    n_val = Natural.from_int(42)
    assert str(ADD_NN_N(n_zero, n_zero)) == "0"
    assert str(ADD_NN_N(n_zero, n_val)) == "42"
    assert str(ADD_NN_N(n_val, n_zero)) == "42"


def test_ADD_NN_N_no_mutation():
    n1 = Natural.from_str("123")
    n2 = Natural.from_str("456")
    orig1 = list(n1.digits)
    orig2 = list(n2.digits)
    _ = ADD_NN_N(n1, n2)
    assert n1.digits == orig1
    assert n2.digits == orig2
