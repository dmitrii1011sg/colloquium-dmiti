import random

import pytest
from core.base.Natural import Natural
from core.modules.MUL_Nk_N import MUL_Nk_N


def test_mul_nk_n():
    a = Natural.from_str("123")
    k = Natural.from_str("3")
    result = MUL_Nk_N(a, k)
    assert str(result) == "123000"

    a = Natural.from_str("5")
    k = Natural.from_str("0")
    result = MUL_Nk_N(a, k)
    assert str(result) == "5"

    a = Natural.from_str("0")
    k = Natural.from_str("5")
    result = MUL_Nk_N(a, k)
    assert str(result) == "0"

    a = Natural.from_str("0")
    k = Natural.from_str("0")
    result = MUL_Nk_N(a, k)
    assert str(result) == "0"

    a = Natural.from_str("1")
    k = Natural.from_str("1")
    result = MUL_Nk_N(a, k)
    assert str(result) == "10"

    a = Natural.from_str("999")
    k = Natural.from_str("2")
    result = MUL_Nk_N(a, k)
    assert str(result) == "99900"


@pytest.mark.parametrize("iteration", range(5))
def test_mul_nk_n_random(iteration):
    val = random.randint(0, 10**50)
    k_val = random.randint(0, 50)

    a = Natural.from_int(val)
    k = Natural.from_int(k_val)

    expected = val * (10**k_val)
    result = MUL_Nk_N(a, k)

    assert str(result) == str(expected)


def test_mul_nk_n_huge_numbers():
    base_str = "1" + "2" * 10000
    a = Natural.from_str(base_str)
    k = Natural.from_str("100")
    result = MUL_Nk_N(a, k)

    expected_str = base_str + "0" * 100
    assert str(result) == expected_str

    a = Natural.from_str("1" + "0" * 1000)
    k = Natural.from_str("1000")
    result = MUL_Nk_N(a, k)
    assert str(result) == "1" + "0" * 2000


def test_extreme_cases():
    a = Natural.from_str("123456789")
    k = Natural.from_str("0")
    result = MUL_Nk_N(a, k)
    assert str(result) == "123456789"

    a = Natural.from_str("0")
    k = Natural.from_str("10")
    result = MUL_Nk_N(a, k)
    assert str(result) == "0"

    a = Natural.from_str("1")
    k = Natural.from_str("100")
    result = MUL_Nk_N(a, k)
    assert str(result) == "1" + "0" * 100


def test_almost_equal():
    a = Natural.from_str("9999999999")
    k = Natural.from_str("1")
    result = MUL_Nk_N(a, k)
    assert str(result) == "99999999990"

    a = Natural.from_str("1000000000")
    k = Natural.from_str("2")
    result = MUL_Nk_N(a, k)
    assert str(result) == "100000000000"
