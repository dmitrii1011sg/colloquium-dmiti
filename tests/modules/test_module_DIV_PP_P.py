import random
from fractions import Fraction

import pytest
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.PModule.DIV_PP_P import DIV_PP_P


def test_DIV_PP_P_simple_exact():
    # (x^2 - 1) / (x - 1) = x + 1
    a = Polynom([Rational.from_str("-1"), Rational.from_str("0"), Rational.from_str("1")])
    b = Polynom([Rational.from_str("-1"), Rational.from_str("1")])
    result = DIV_PP_P(a, b)
    expected = Polynom([Rational.from_str("1"), Rational.from_str("1")])
    assert str(result) == str(expected)


def test_DIV_PP_P_with_remainder():
    # (x^2 + 2x + 1) / (x + 2) = x (остаток 1, в частное не входит)
    a = Polynom([Rational.from_str("1"), Rational.from_str("2"), Rational.from_str("1")])
    b = Polynom([Rational.from_str("2"), Rational.from_str("1")])
    result = DIV_PP_P(a, b)
    expected = Polynom([Rational.from_str("0"), Rational.from_str("1")])
    assert str(result) == str(expected)


def test_DIV_PP_P_by_self():
    # P / P = 1
    coeffs = [Rational.from_str(f"{random.randint(-5, 5)}/1") for _ in range(4)]
    p = Polynom(coeffs)
    # Гарантируем ненулевой старший коэффициент
    p.coefficients[-1] = Rational.from_str("1")
    result = DIV_PP_P(p, p)
    assert str(result) == str(Polynom([Rational.from_str("1")]))


def test_DIV_PP_P_degree_less():
    # (x + 1) / (x^2 + 1) = 0
    a = Polynom([Rational.from_str("1"), Rational.from_str("1")])
    b = Polynom([Rational.from_str("1"), Rational.from_str("0"), Rational.from_str("1")])
    result = DIV_PP_P(a, b)
    assert str(result) == "0"


def test_DIV_PP_P_skip_degree():
    # (x^2 + 1) / 1 = x^2 + 1
    a = Polynom([Rational.from_str("1"), Rational.from_str("0"), Rational.from_str("1")])
    b = Polynom([Rational.from_str("1")])
    result = DIV_PP_P(a, b)
    assert str(result) == "x^2 + 1"


def test_DIV_PP_P_by_constant():
    # (2x^2 + 4x) / 2 = x^2 + 2x
    a = Polynom([Rational.from_str("0"), Rational.from_str("4"), Rational.from_str("2")])
    b = Polynom([Rational.from_str("2")])
    result = DIV_PP_P(a, b)
    expected = Polynom([Rational.from_str("0"), Rational.from_str("2"), Rational.from_str("1")])
    assert str(result) == str(expected)


def _calc_expected_quotient(num_coeffs, den_coeffs):
    """Справочная функция для вычисления частного на чистых Fraction."""
    num = list(num_coeffs)
    den = list(den_coeffs)
    deg_num = len(num) - 1
    deg_den = len(den) - 1
    if deg_num < deg_den:
        return [Fraction(0)]

    q_deg = deg_num - deg_den
    q = [Fraction(0)] * (q_deg + 1)
    for i in range(q_deg, -1, -1):
        if i + deg_den >= len(num):
            continue
        lead_coeff = num[i + deg_den] / den[deg_den]
        q[i] = lead_coeff
        for j in range(len(den)):
            if i + j < len(num):
                num[i + j] -= lead_coeff * den[j]
    return q


@pytest.mark.parametrize("iteration", range(10))
def test_DIV_PP_P_random(iteration):
    deg_a = random.randint(2, 8)
    deg_b = random.randint(1, 4)
    if deg_a < deg_b:
        deg_a, deg_b = deg_b, deg_a

    coeffs_a = [Fraction(random.randint(-10, 10)) for _ in range(deg_a + 1)]
    coeffs_b = [Fraction(random.randint(1, 10)) for _ in range(deg_b + 1)]  # старший != 0

    p_a = Polynom([Rational.from_str(f"{c}/1") for c in coeffs_a])
    p_b = Polynom([Rational.from_str(f"{c}/1") for c in coeffs_b])

    result = DIV_PP_P(p_a, p_b)

    expected_coeffs = _calc_expected_quotient(coeffs_a, coeffs_b)
    expected_rationals = [
        Rational.from_str(f"{c.numerator}/{c.denominator}") for c in expected_coeffs
    ]
    expected = Polynom(expected_rationals)
    assert str(result) == str(expected)


def test_DIV_PP_P_invalid_input():
    with pytest.raises(ValueError):
        DIV_PP_P("not polynom", Polynom([Rational.from_str("1")]))  # type: ignore

    with pytest.raises(ValueError):
        DIV_PP_P(Polynom([Rational.from_str("1")]), "not polynom")  # type: ignore

    with pytest.raises(ValueError):
        DIV_PP_P(None, Polynom([Rational.from_str("1")]))  # type: ignore


def test_DIV_PP_P_no_mutation():
    a = Polynom([Rational.from_str("1"), Rational.from_str("2"), Rational.from_str("3")])
    b = Polynom([Rational.from_str("1"), Rational.from_str("1")])
    _ = DIV_PP_P(a, b)
    # Проверка, что исходные многочлены не изменились
    assert str(a) == "3x^2 + 2x + 1"
    assert str(b) == "x + 1"
