import random

import pytest
from core.base.Natural import Natural
from core.modules.NModule.NZER_N_B import NZER_N_B


def test_nzer_n_b():
    n_zero = Natural.from_str("0")
    n_one = Natural.from_str("1")
    n_big = Natural.from_str("100")
    assert NZER_N_B(n_zero) is False
    assert NZER_N_B(n_one) is True
    assert NZER_N_B(n_big) is True


@pytest.mark.parametrize("iteration", range(5))
def test_nzer_n_b_random(iteration):
    val = random.randint(0, 10**50)
    n = Natural.from_int(val)
    expected = val != 0
    assert NZER_N_B(n) == expected


def test_nzer_n_b_huge_numbers():
    n_huge = Natural.from_str("9" * 10000)
    n_huge_with_zero_tail = Natural.from_str("1" + "0" * 10000)
    assert NZER_N_B(n_huge) is True
    assert NZER_N_B(n_huge_with_zero_tail) is True


def test_nzer_n_b_extreme_cases():
    n_zero_from_int = Natural.from_int(0)
    n_zero_from_str = Natural.from_str("0")
    n_zero_from_list = Natural([0])
    assert NZER_N_B(n_zero_from_int) is False
    assert NZER_N_B(n_zero_from_str) is False
    assert NZER_N_B(n_zero_from_list) is False


def test_nzer_n_b_edge_values():
    n_one = Natural.from_int(1)
    n_nine = Natural.from_int(9)
    n_ten = Natural.from_int(10)
    assert NZER_N_B(n_one) is True
    assert NZER_N_B(n_nine) is True
    assert NZER_N_B(n_ten) is True
