import random
from fractions import Fraction

import pytest
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.PModule.MOD_PP_P import MOD_PP_P


def test_MOD_PP_P_exact_division():
    # (x^2 - 1) % (x - 1) = 0
    a = Polynom(
        [Rational.from_str("-1"), Rational.from_str("0"), Rational.from_str("1")]
    )
    b = Polynom([Rational.from_str("-1"), Rational.from_str("1")])
    result = MOD_PP_P(a, b)
    expected = Polynom([Rational.from_str("0")])
    assert str(result) == str(expected)


def test_MOD_PP_P_with_remainder():
    # (x^2 + 2x + 1) % (x + 2) = 1
    a = Polynom(
        [Rational.from_str("1"), Rational.from_str("2"), Rational.from_str("1")]
    )
    b = Polynom([Rational.from_str("2"), Rational.from_str("1")])
    result = MOD_PP_P(a, b)
    expected = Polynom([Rational.from_str("1")])
    assert str(result) == str(expected)


def test_MOD_PP_P_degree_less():
    # (x + 1) % (x^2 + 1) = x + 1 (остаток равен делимому)
    a = Polynom([Rational.from_str("1"), Rational.from_str("1")])
    b = Polynom(
        [Rational.from_str("1"), Rational.from_str("0"), Rational.from_str("1")]
    )
    result = MOD_PP_P(a, b)
    expected = Polynom([Rational.from_str("1"), Rational.from_str("1")])
    assert str(result) == str(expected)


def test_MOD_PP_P_by_constant():
    # (2x^2 + 4x) % 2 = 0
    a = Polynom(
        [Rational.from_str("0"), Rational.from_str("4"), Rational.from_str("2")]
    )
    b = Polynom([Rational.from_str("2")])
    result = MOD_PP_P(a, b)
    expected = Polynom([Rational.from_str("0")])
    assert str(result) == str(expected)


def test_MOD_PP_P_zero_dividend():
    # 0 % (x + 1) = 0
    a = Polynom([Rational.from_str("0")])
    b = Polynom([Rational.from_str("1"), Rational.from_str("1")])
    result = MOD_PP_P(a, b)
    expected = Polynom([Rational.from_str("0")])
    assert str(result) == str(expected)


def _calc_expected_remainder(num_coeffs, den_coeffs):
    """Справочная функция для вычисления остатка на чистых Fraction."""
    num = list(num_coeffs)
    den = list(den_coeffs)
    deg_num = len(num) - 1
    deg_den = len(den) - 1

    # Деление столбиком
    for i in range(deg_num - deg_den, -1, -1):
        if i + deg_den >= len(num):
            continue
        lead = num[i + deg_den] / den[deg_den]
        for j in range(len(den)):
            if i + j < len(num):
                num[i + j] -= lead * den[j]
    return num[: max(1, len(num))]  # Оставляем хотя бы один коэффициент


@pytest.mark.parametrize("iteration", range(10))
def test_MOD_PP_P_random(iteration):
    deg_a = random.randint(2, 8)
    deg_b = random.randint(1, 4)
    if deg_a < deg_b:
        deg_a, deg_b = deg_b, deg_a

    coeffs_a = [Fraction(random.randint(-10, 10)) for _ in range(deg_a + 1)]
    coeffs_b = [Fraction(random.randint(1, 10)) for _ in range(deg_b + 1)]

    p_a = Polynom([Rational.from_str(f"{c}/1") for c in coeffs_a])
    p_b = Polynom([Rational.from_str(f"{c}/1") for c in coeffs_b])

    result = MOD_PP_P(p_a, p_b)

    expected_coeffs = _calc_expected_remainder(coeffs_a, coeffs_b)
    expected_rationals = [
        Rational.from_str(f"{c.numerator}/{c.denominator}") for c in expected_coeffs
    ]
    expected = Polynom(expected_rationals)

    assert str(result) == str(expected)


def test_MOD_PP_P_property_deg_remainder_less():
    """Фундаментальное свойство: deg(remainder) < deg(divisor) или remainder == 0"""
    a = Polynom(
        [
            Rational.from_str("5"),
            Rational.from_str("3"),
            Rational.from_str("2"),
            Rational.from_str("1"),
        ]
    )
    b = Polynom(
        [Rational.from_str("-1"), Rational.from_str("2"), Rational.from_str("1")]
    )
    r = MOD_PP_P(a, b)

    # Проверяем, что результат либо ноль, либо его длина коэффициентов меньше, чем у b
    is_zero = all(str(c) in ("0", "0/1") for c in r.coefficients)
    if not is_zero:
        assert len(r.coefficients) < len(b.coefficients)


def test_MOD_PP_P_invalid_input():
    with pytest.raises(ValueError):
        MOD_PP_P("not polynom", Polynom([Rational.from_str("1")]))  # type: ignore

    with pytest.raises(ValueError):
        MOD_PP_P(Polynom([Rational.from_str("1")]), "not polynom")  # type: ignore

    with pytest.raises(ValueError):
        MOD_PP_P(None, Polynom([Rational.from_str("1")]))  # type: ignore


def test_MOD_PP_P_division_by_zero():
    a = Polynom([Rational.from_str("1"), Rational.from_str("2")])
    b = Polynom([Rational.from_str("0")])
    with pytest.raises(ZeroDivisionError):
        MOD_PP_P(a, b)


def test_MOD_PP_P_no_mutation():
    a = Polynom(
        [Rational.from_str("1"), Rational.from_str("2"), Rational.from_str("3")]
    )
    b = Polynom([Rational.from_str("1"), Rational.from_str("1")])
    _ = MOD_PP_P(a, b)
    # Проверка, что исходные многочлены не изменились
    assert str(a) == "3x^2 + 2x + 1"
    assert str(b) == "x + 1"
