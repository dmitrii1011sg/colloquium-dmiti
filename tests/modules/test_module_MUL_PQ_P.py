import random

import pytest
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.PModule.MUL_PQ_P import MUL_PQ_P
from core.modules.QModule.MUL_QQ_Q import MUL_QQ_Q


def test_MUL_PQ_P_simple():
    p = Polynom(
        [Rational.from_str("1"), Rational.from_str("2"), Rational.from_str("3")]
    )
    r = Rational.from_str("3")
    result = MUL_PQ_P(p, r)
    assert str(result) == "9x^2 + 6x + 3"


def test_MUL_PQ_P_zero_polynom():
    p = Polynom([Rational.from_str("0")])
    r = Rational.from_str("5")
    result = MUL_PQ_P(p, r)
    assert str(result) == "0"


@pytest.mark.parametrize("iteration", range(10))
def test_MUL_PQ_P_random(iteration):
    degree1 = random.randint(0, 10)
    r = random.randint(0, 10**50)

    coeffs1 = [
        Rational.from_str(f"{random.randint(-10, 10)}/1") for _ in range(degree1 + 1)
    ]

    p1 = Polynom(coeffs1)
    r = Rational.from_str(str(r))

    result = MUL_PQ_P(p1, r)

    expected_coeffs = []
    for i in range(degree1 + 1):
        c1 = coeffs1[i] if i <= degree1 else Rational.from_str("0")
        expected_coeffs.append(MUL_QQ_Q(c1, r))

    expected_result = Polynom(expected_coeffs)
    assert str(result) == str(expected_result)
