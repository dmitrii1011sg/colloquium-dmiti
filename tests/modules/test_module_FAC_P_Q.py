import random
from fractions import Fraction

import pytest
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.PModule.FAC_P_Q import FAC_P_Q


def test_FAC_P_Q_simple():
    # 2/3x + 1/6
    a = Polynom(
        [Rational.from_str("1/6"), Rational.from_str("2/3")]
    )
    result = FAC_P_Q(a)
    expected = Rational.from_str("1/6")
    assert str(result) == str(expected)


def test_FAC_P_Q_all_int():
    # 4x^2 + 2x + 6
    a = Polynom(
        [Rational.from_str("6"), Rational.from_str("2"), Rational.from_str("4")]
    )
    result = FAC_P_Q(a)
    expected = Rational.from_str("2")
    assert str(result) == str(expected)


def test_FAC_P_Q_negative_coefficients():
    # -3/7x + 2/5
    a = Polynom(
        [Rational.from_str("2/5"), Rational.from_str("-3/7")]
    )
    result = FAC_P_Q(a)
    expected = Rational.from_str("1/35")
    assert str(result) == str(expected)


def test_FAC_P_Q_single_term():
    # 5/8
    a = Polynom([Rational.from_str("5/8")])
    result = FAC_P_Q(a)
    expected = Rational.from_str("5/8")
    assert str(result) == str(expected)


def test_FAC_P_Q_zero_polynom():
    # 0
    a = Polynom([Rational.from_str("0")])
    result = FAC_P_Q(a)
    expected = Rational.from_str("0")
    assert str(result) == str(expected)


def test_FAC_P_Q_same_denominators():
    # 2/3x + 4/3
    a = Polynom(
        [Rational.from_str("4/3"), Rational.from_str("2/3")]
    )
    result = FAC_P_Q(a)
    expected = Rational.from_str("2/3")
    assert str(result) == str(expected)


def test_FAC_P_Q_same_numerators():
    # 3/4x + 3/5
    a = Polynom(
        [Rational.from_str("3/5"), Rational.from_str("3/4")]
    )
    result = FAC_P_Q(a)
    expected = Rational.from_str("3/20")
    assert str(result) == str(expected)


@pytest.mark.parametrize("iteration", range(10))
def test_FAC_P_Q_random(iteration):
    degree = random.randint(1, 5)
    coeffs = []
    numerators = []
    denominators = []
    for _ in range(degree + 1):
        num = random.randint(-10, 10)
        if num == 0:
            num = 1
        den = random.randint(1, 10)
        coeffs.append(Rational.from_str(f"{num}/{den}"))
        numerators.append(abs(num))
        denominators.append(den)

    a = Polynom(coeffs)

    import math
    expected_gcd = numerators[0]
    for n in numerators[1:]:
        expected_gcd = math.gcd(expected_gcd, n)

    expected_lcm = denominators[0]
    for d in denominators[1:]:
        expected_lcm = expected_lcm * d // math.gcd(expected_lcm, d)

    expected_fraction = Fraction(expected_gcd, expected_lcm)

    result = FAC_P_Q(a)

    result_as_fraction = Fraction(int(result.numer), int(result.denom))
    assert result_as_fraction == expected_fraction

def test_FAC_P_Q_invalid_input():
    with pytest.raises(ValueError):
        FAC_P_Q("not polynom")  # type: ignore

    with pytest.raises(ValueError):
        FAC_P_Q(None)  # type: ignore


def test_FAC_P_Q_no_mutation():
    a = Polynom(
        [Rational.from_str("1/2"), Rational.from_str("3/4")]
    )
    original_str = str(a)
    _ = FAC_P_Q(a)
    # Проверка, что исходный многочлен не изменился
    assert str(a) == original_str