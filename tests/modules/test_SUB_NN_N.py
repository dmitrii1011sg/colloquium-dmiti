import random
import pytest
from core.base.Natural import Natural
from core.modules.SUB_NN_N import SUB_NN_N


def test_SUB_NN_N():
    n1 = Natural.from_str("100")
    n2 = Natural.from_str("50")
    n3 = Natural.from_str("100")
    assert str(SUB_NN_N(n1, n2)) == "50"
    assert str(SUB_NN_N(n1, n3)) == "0"


@pytest.mark.parametrize("iteration", range(5))
def test_SUB_NN_N_random(iteration):
    val1 = random.randint(0, 10**50)
    val2 = random.randint(0, 10**50)
    if val1 < val2:
        val1, val2 = val2, val1
    n1 = Natural.from_int(val1)
    n2 = Natural.from_int(val2)
    assert str(SUB_NN_N(n1, n2)) == str(val1 - val2)


def test_SUB_NN_N_huge_numbers():
    n1 = Natural.from_str("1" + "0" * 10000)
    n2 = Natural.from_str("1")
    assert str(SUB_NN_N(n1, n2)) == "9" * 10000


def test_SUB_NN_N_borrow_chain():
    n1 = Natural.from_str("1000")
    n2 = Natural.from_str("1")
    assert str(SUB_NN_N(n1, n2)) == "999"

    n3 = Natural.from_str("10000000")
    n4 = Natural.from_str("1")
    assert str(SUB_NN_N(n3, n4)) == "9999999"


def test_SUB_NN_N_equal_numbers():
    n1 = Natural.from_str("12345")
    n2 = Natural.from_str("12345")
    assert str(SUB_NN_N(n1, n2)) == "0"


def test_SUB_NN_N_zero_cases():
    n_val = Natural.from_int(42)
    n_zero = Natural.from_int(0)
    assert str(SUB_NN_N(n_val, n_zero)) == "42"
    assert str(SUB_NN_N(n_zero, n_zero)) == "0"


def test_SUB_NN_N_raises_when_first_less():
    n1 = Natural.from_str("5")
    n2 = Natural.from_str("10")
    with pytest.raises(ValueError):
        SUB_NN_N(n1, n2)


def test_SUB_NN_N_no_mutation():
    n1 = Natural.from_str("456")
    n2 = Natural.from_str("123")
    orig1 = list(n1.digits)
    orig2 = list(n2.digits)
    _ = SUB_NN_N(n1, n2)
    assert n1.digits == orig1
    assert n2.digits == orig2
