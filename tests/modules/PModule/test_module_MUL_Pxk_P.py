import random

import pytest
from core.base.Natural import Natural
from core.base.Polynom import Polynom
from core.modules.PModule.MUL_Pxk_P import MUL_Pxk_P


def test_MUL_Pxk_P_shift_simple():
    a = Polynom.from_str("x+2")
    k = Natural.from_int(2)
    result = MUL_Pxk_P(a, k)
    assert str(result) == "x^3 + 2x^2"


def test_MUL_Pxk_P_k_zero_returns_same():
    a = Polynom.from_str("2x^2+3x+1")
    k = Natural.from_int(0)
    result = MUL_Pxk_P(a, k)
    assert str(result) == "2x^2 + 3x + 1"


def test_MUL_Pxk_P_zero_polynomial():
    a = Polynom.from_str("0")
    k = Natural.from_int(5)
    result = MUL_Pxk_P(a, k)
    assert str(result) == "0"


def test_MUL_Pxk_P_large_shift():
    a = Polynom.from_str("1 + 2x")
    k = Natural.from_int(4)
    result = MUL_Pxk_P(a, k)
    assert str(result) == "2x^5 + x^4"


def test_MUL_Pxk_P_no_mutation():
    a = Polynom.from_str("x^2 + 1")
    orig = str(a)
    k = Natural.from_int(3)
    _ = MUL_Pxk_P(a, k)
    assert str(a) == orig


@pytest.mark.parametrize("iteration", range(5))
def test_MUL_Pxk_P_random_shifts(iteration):
    deg = random.randint(0, 5)
    coeffs = [str(random.randint(-5, 5)) for _ in range(deg + 1)]
    terms = []
    for i in range(len(coeffs) - 1, -1, -1):
        c = int(coeffs[i])
        if c == 0:
            continue
        if i == 0:
            terms.append(str(c))
        elif i == 1:
            terms.append(f"{c}x")
        else:
            terms.append(f"{c}x^{i}")

    poly_str = "+".join(terms) if terms else "0"
    a = Polynom.from_str(poly_str)
    k = Natural.from_int(random.randint(0, 5))
    result = MUL_Pxk_P(a, k)
    coeff_list = []
    for part in a.coefficients:
        coeff_list.append(str(part))
    expected_coeffs = ["0"] * int(str(k)) + coeff_list
    exp_terms = []
    for i in range(len(expected_coeffs) - 1, -1, -1):
        val = expected_coeffs[i]
        if val.startswith("-"):
            num = val
        else:
            num = val
        if num == "0":
            continue
        if i == 0:
            exp_terms.append(num)
        elif i == 1:
            exp_terms.append(f"{num}x")
        else:
            exp_terms.append(f"{num}x^{i}")

    expected_str = "+".join(exp_terms) if exp_terms else "0"
    expected = Polynom.from_str(expected_str)
    assert str(result) == str(expected)
