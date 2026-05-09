import random
from math import gcd

import pytest
from core.base.Natural import Natural
from core.modules.NModule.GCF_NN_N import GCF_NN_N


def test_GCF_NN_N():
    n1 = Natural.from_str("100")
    n2 = Natural.from_str("50")
    n3 = Natural.from_str("100")
    assert str(GCF_NN_N(n1, n2)) == "50"
    assert str(GCF_NN_N(n1, n3)) == "100"


@pytest.mark.parametrize("iteration", range(5))
def test_GCF_NN_N_random(iteration):
    val1 = random.randint(0, 10**50)
    val2 = random.randint(0, 10**50)
    val3 = gcd(val1, val2)
    n1 = Natural.from_int(val1)
    n2 = Natural.from_int(val2)
    n3 = Natural.from_int(val3)
    assert str(GCF_NN_N(n1, n2)) == str(n3)


def test_GCF_NN_N_huge_numbers():
    n1 = Natural.from_str("1" + "0" * 1000000)
    n2 = Natural.from_str("1" + "0" * 100000)
    assert str(GCF_NN_N(n1, n2)) == str(n2)


def test_GCF_NN_N_Fibonacci():
    n1 = Natural.from_str("354224848179261915075")
    n2 = Natural.from_str("21892299583455516902")
    assert str(GCF_NN_N(n1, n2)) == "1"


def test_GCF_NN_N_equal_numbers():
    n1 = Natural.from_str("12345")
    n2 = Natural.from_str("12345")
    assert str(GCF_NN_N(n1, n2)) == "12345"


def test_GCF_NN_N_zero_cases():
    n_val = Natural.from_int(42)
    n_zero = Natural.from_int(0)
    with pytest.raises(ValueError):
        GCF_NN_N(n_val, n_zero)
    with pytest.raises(ValueError):
        GCF_NN_N(n_zero, n_zero)


def test_GCF_NN_N_two_zero():
    n1 = Natural.from_str("0")
    n2 = Natural.from_str("0")
    with pytest.raises(ValueError):
        GCF_NN_N(n1, n2)


def test_GCF_NN_N_no_mutation():
    n1 = Natural.from_str("456")
    n2 = Natural.from_str("123")
    orig1 = list(n1.digits)
    orig2 = list(n2.digits)
    _ = GCF_NN_N(n1, n2)
    assert n1.digits == orig1
    assert n2.digits == orig2
