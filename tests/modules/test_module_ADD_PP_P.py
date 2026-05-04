import random

import pytest
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.PModule.ADD_PP_P import ADD_PP_P
from core.modules.QModule.ADD_QQ_Q import ADD_QQ_Q


def test_add_pp_p_simple():
    p1 = Polynom(
        [Rational.from_str("1"), Rational.from_str("2"), Rational.from_str("3")]
    )
    p2 = Polynom([Rational.from_str("4"), Rational.from_str("5")])
    result = ADD_PP_P(p1, p2)
    assert str(result) == "3x^2 + 7x + 5"


def test_add_pp_p_different_degrees():
    p1 = Polynom([Rational.from_str("1"), Rational.from_str("2")])
    p2 = Polynom(
        [Rational.from_str("3"), Rational.from_str("4"), Rational.from_str("5")]
    )
    result = ADD_PP_P(p1, p2)
    assert str(result) == "5x^2 + 6x + 4"


def test_add_pp_p_zero_polynom():
    p1 = Polynom([Rational.from_str("0")])
    p2 = Polynom(
        [Rational.from_str("3"), Rational.from_str("4"), Rational.from_str("5")]
    )
    result = ADD_PP_P(p1, p2)
    assert str(result) == "5x^2 + 4x + 3"


@pytest.mark.parametrize("iteration", range(10))
def test_add_pp_p_random(iteration):
    degree1 = random.randint(0, 10)
    degree2 = random.randint(0, 10)

    coeffs1 = [
        Rational.from_str(f"{random.randint(-10, 10)}/1") for _ in range(degree1 + 1)
    ]
    coeffs2 = [
        Rational.from_str(f"{random.randint(-10, 10)}/1") for _ in range(degree2 + 1)
    ]

    p1 = Polynom(coeffs1)
    p2 = Polynom(coeffs2)

    result = ADD_PP_P(p1, p2)

    expected_coeffs = []
    for i in range(max(degree1, degree2) + 1):
        c1 = coeffs1[i] if i <= degree1 else Rational.from_str("0")
        c2 = coeffs2[i] if i <= degree2 else Rational.from_str("0")
        expected_coeffs.append(ADD_QQ_Q(c1, c2))

    expected_result = Polynom(expected_coeffs)
    assert str(result) == str(expected_result)
