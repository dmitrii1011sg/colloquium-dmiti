import random

import pytest
from core.base.Natural import Natural
from core.modules.NModule.SUB_NDN_N import SUB_NDN_N


def test_SUB_NDN_N():
    n1 = Natural.from_str("200")
    n2 = Natural.from_str("50")
    d1 = 2
    d2 = 4
    assert str(SUB_NDN_N(n1, n2, d1)) == "100"
    assert str(SUB_NDN_N(n1, n2, d2)) == "0"


@pytest.mark.parametrize("iteration", range(5))
def test_SUB_NDN_N_random(iteration):
    val2 = random.randint(0, 10**50)
    val3 = random.randint(0, 9)
    min_val1 = val2 * val3
    val1 = random.randint(min_val1, min_val1 + 10**6)
    n1 = Natural.from_int(val1)
    n2 = Natural.from_int(val2)
    d = val3
    assert str(SUB_NDN_N(n1, n2, d)) == str(val1 - val2 * val3)


def test_SUB_NDN_N_huge_numbers():
    n1 = Natural.from_str("1" + "0" * 10000)
    n2 = Natural.from_str("1")
    d = 1
    assert str(SUB_NDN_N(n1, n2, d)) == "9" * 10000


def test_SUB_NDN_N_borrow_chain():
    n1 = Natural.from_str("1000")
    n2 = Natural.from_str("1")
    d1 = 1
    assert str(SUB_NDN_N(n1, n2, d1)) == "999"

    n3 = Natural.from_str("10000000")
    n4 = Natural.from_str("1")
    d2 = 1
    assert str(SUB_NDN_N(n3, n4, d2)) == "9999999"


def test_SUB_NDN_N_equal_numbers():
    n1 = Natural.from_str("12345")
    n2 = Natural.from_str("12345")
    d = 1
    assert str(SUB_NDN_N(n1, n2, d)) == "0"


def test_SUB_NDN_N_zero_cases():
    n_val = Natural.from_int(42)
    n_zero = Natural.from_int(0)
    d = 7
    assert str(SUB_NDN_N(n_val, n_zero, d)) == "42"
    assert str(SUB_NDN_N(n_zero, n_zero, d)) == "0"


def test_SUB_NDN_N_raises_when_first_less():
    n1 = Natural.from_str("5")
    n2 = Natural.from_str("10")
    d = 1
    with pytest.raises(ValueError):
        SUB_NDN_N(n1, n2, d)


def test_SUB_NDN_N_raises_when_d_not_digit():
    n1 = Natural.from_str("1000")
    n2 = Natural.from_str("10")
    d = 12
    with pytest.raises(ValueError):
        SUB_NDN_N(n1, n2, d)


def test_SUB_NDN_N_no_mutation():
    n1 = Natural.from_str("456")
    n2 = Natural.from_str("123")
    d = 1
    orig1 = list(n1.digits)
    orig2 = list(n2.digits)
    _ = SUB_NDN_N(n1, n2, d)
    assert n1.digits == orig1
    assert n2.digits == orig2