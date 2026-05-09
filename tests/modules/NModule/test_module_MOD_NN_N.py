import random

import pytest
from core.base.Natural import Natural
from core.modules.NModule.MOD_NN_N import MOD_NN_N


def test_MOD_NN_N():
    n1 = Natural.from_str("100")
    n2 = Natural.from_str("7")
    n3 = Natural.from_str("4")
    assert str(MOD_NN_N(n1, n2)) == "2"
    assert str(MOD_NN_N(n1, n3)) == "0"


@pytest.mark.parametrize("iteration", range(5))
def test_MOD_NN_N_random(iteration):
    val1 = random.randint(0, 10**50)
    val2 = random.randint(1, 10**25)
    n1 = Natural.from_int(val1)
    n2 = Natural.from_int(val2)
    assert str(MOD_NN_N(n1, n2)) == str(val1 % val2)


def test_MOD_NN_N_huge_numbers():
    n1 = Natural.from_str("1" + "0" * 100)
    n2 = Natural.from_str("1" + "0" * 50)
    assert str(MOD_NN_N(n1, n2)) == "0"


def test_MOD_NN_N_smaller_dividend():
    n1 = Natural.from_str("5")
    n2 = Natural.from_str("10")
    assert str(MOD_NN_N(n1, n2)) == "5"


def test_MOD_NN_N_equal_numbers():
    n1 = Natural.from_str("12345")
    n2 = Natural.from_str("12345")
    assert str(MOD_NN_N(n1, n2)) == "0"


def test_MOD_NN_N_divide_by_one():
    n1 = Natural.from_str("987654321")
    n2 = Natural.from_str("1")
    assert str(MOD_NN_N(n1, n2)) == "0"


def test_MOD_NN_N_zero_dividend():
    n_zero = Natural.from_int(0)
    n_val = Natural.from_int(42)
    assert str(MOD_NN_N(n_zero, n_val)) == "0"


def test_MOD_NN_N_raises_on_zero_divisor():
    n1 = Natural.from_str("100")
    n_zero = Natural.from_int(0)
    with pytest.raises(ValueError):
        MOD_NN_N(n1, n_zero)


def test_MOD_NN_N_no_mutation():
    n1 = Natural.from_str("12345")
    n2 = Natural.from_str("67")
    orig1 = list(n1.digits)
    orig2 = list(n2.digits)
    _ = MOD_NN_N(n1, n2)
    assert n1.digits == orig1
    assert n2.digits == orig2
