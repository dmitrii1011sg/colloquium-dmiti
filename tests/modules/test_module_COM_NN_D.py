import random

import pytest
from core.base.Natural import Natural
from core.modules.COM_NN_D import COM_NN_D


def test_com_nn_d():
    n1 = Natural.from_str("100")
    n2 = Natural.from_str("50")
    n3 = Natural.from_str("100")

    assert COM_NN_D(n1, n2) == 2
    assert COM_NN_D(n2, n1) == 1
    assert COM_NN_D(n1, n3) == 0


@pytest.mark.parametrize("iteration", range(5))
def test_com_nn_d_random(iteration):
    val1 = random.randint(0, 10**50)
    val2 = random.randint(0, 10**50)

    n1 = Natural.from_int(val1)
    n2 = Natural.from_int(val2)

    if val1 > val2:
        expected = 2
    elif val1 < val2:
        expected = 1
    else:
        expected = 0

    assert COM_NN_D(n1, n2) == expected


def test_com_nn_d_huge_numbers():
    base_str = "9" * 10000
    n1 = Natural.from_str(base_str + "5")
    n2 = Natural.from_str(base_str + "4")

    assert COM_NN_D(n1, n2) == 2
    assert COM_NN_D(n2, n1) == 1


def test_extreme_cases():
    n_zero = Natural.from_int(0)
    n_huge = Natural.from_str("1" + "0" * 1000)

    assert COM_NN_D(n_huge, n_zero) == 2
    assert COM_NN_D(n_zero, n_huge) == 1


def test_almost_equal():
    n1 = Natural.from_str("2000000000000")
    n2 = Natural.from_str("1999999999999")

    assert COM_NN_D(n1, n2) == 2

    n3 = Natural.from_str("99999")
    n4 = Natural.from_str("100000")

    assert COM_NN_D(n3, n4) == 1
