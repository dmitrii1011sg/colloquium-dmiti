import random
from fractions import Fraction

import pytest
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.PModule.MUL_PP_P import MUL_PP_P


def test_MUL_PP_P_simple():
    # (x + 2) * (x - 1) = x^2 + x - 2
    p1 = Polynom([Rational.from_str("2"), Rational.from_str("1")])
    p2 = Polynom([Rational.from_str("-1"), Rational.from_str("1")])
    result = MUL_PP_P(p1, p2)
    expected = Polynom(
        [Rational.from_str("-2"), Rational.from_str("1"), Rational.from_str("1")]
    )
    assert str(result) == str(expected)


def test_MUL_PP_P_by_zero():
    p1 = Polynom(
        [Rational.from_str("5"), Rational.from_str("2"), Rational.from_str("1")]
    )
    p2 = Polynom([Rational.from_str("0")])
    result = MUL_PP_P(p1, p2)
    expected = Polynom([Rational.from_str("0")])
    assert str(result) == str(expected)


def test_MUL_PP_P_by_one():
    p1 = Polynom(
        [Rational.from_str("3"), Rational.from_str("-2"), Rational.from_str("4")]
    )
    p2 = Polynom([Rational.from_str("1")])
    result = MUL_PP_P(p1, p2)
    expected = Polynom(
        [Rational.from_str("3"), Rational.from_str("-2"), Rational.from_str("4")]
    )
    assert str(result) == str(expected)


def test_MUL_PP_P_constants():
    p1 = Polynom([Rational.from_str("3")])
    p2 = Polynom([Rational.from_str("7")])
    result = MUL_PP_P(p1, p2)
    expected = Polynom([Rational.from_str("21")])
    assert str(result) == str(expected)


@pytest.mark.parametrize("iteration", range(10))
def test_MUL_PP_P_random(iteration):
    deg_a = random.randint(0, 5)
    deg_b = random.randint(0, 5)

    # Генерируем коэффициенты (порядок: от x^0 к x^n)
    coeffs_a = [
        Rational.from_str(f"{random.randint(-5, 5)}/1") for _ in range(deg_a + 1)
    ]
    coeffs_b = [
        Rational.from_str(f"{random.randint(-5, 5)}/1") for _ in range(deg_b + 1)
    ]

    p1 = Polynom(coeffs_a)
    p2 = Polynom(coeffs_b)

    # Вычисляем ожидаемый результат через fractions
    fa = [Fraction(int(c.numer), int(c.denom)) for c in coeffs_a]
    fb = [Fraction(int(c.numer), int(c.denom)) for c in coeffs_b]

    exp_coeffs = [Fraction(0)] * (deg_a + deg_b + 1)
    for i, va in enumerate(fa):
        for j, vb in enumerate(fb):
            exp_coeffs[i + j] += va * vb

    # Собираем ожидаемый Polynom
    exp_rationals = [
        Rational.from_str(f"{c.numerator}/{c.denominator}") for c in exp_coeffs
    ]
    expected = Polynom(exp_rationals)

    result = MUL_PP_P(p1, p2)
    assert str(result) == str(expected)


def test_MUL_PP_P_commutative():
    p1 = Polynom(
        [Rational.from_str("1"), Rational.from_str("2"), Rational.from_str("3")]
    )
    p2 = Polynom([Rational.from_str("4"), Rational.from_str("-1")])
    res1 = MUL_PP_P(p1, p2)
    res2 = MUL_PP_P(p2, p1)
    assert str(res1) == str(res2)


def test_MUL_PP_P_no_mutation():
    p1 = Polynom([Rational.from_str("2"), Rational.from_str("5")])
    p2 = Polynom([Rational.from_str("-1"), Rational.from_str("3")])
    _ = MUL_PP_P(p1, p2)
    assert str(p1) == "5x + 2"
    assert str(p2) == "3x - 1"


def test_MUL_PP_P_invalid_input():
    with pytest.raises(ValueError):
        MUL_PP_P("not polynom", Polynom([Rational.from_str("1")]))  # type: ignore

    with pytest.raises(ValueError):
        MUL_PP_P(Polynom([Rational.from_str("1")]), "not polynom")  # type: ignore

    with pytest.raises(ValueError):
        MUL_PP_P(None, Polynom([Rational.from_str("1")]))  # type: ignore


def test_MUL_PP_P_high_degree():
    # (x^2 + 1) * (x^3 + x) = x^5 + x^3 + x^3 + x = x^5 + 2x^3 + x
    p1 = Polynom(
        [Rational.from_str("1"), Rational.from_str("0"), Rational.from_str("1")]
    )
    p2 = Polynom(
        [
            Rational.from_str("0"),
            Rational.from_str("1"),
            Rational.from_str("0"),
            Rational.from_str("1"),
        ]
    )
    result = MUL_PP_P(p1, p2)
    expected = Polynom(
        [
            Rational.from_str("0"),
            Rational.from_str("1"),
            Rational.from_str("0"),
            Rational.from_str("2"),
            Rational.from_str("0"),
            Rational.from_str("1"),
        ]
    )
    assert str(result) == str(expected)
