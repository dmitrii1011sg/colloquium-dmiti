import pytest
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.PModule.DEG_P_N import DEG_P_N


def test_deg_p_n_quadratic():
    p = Polynom(
        [Rational.from_str("3"), Rational.from_str("0"), Rational.from_str("5")]
    )
    result = DEG_P_N(p)
    assert result == 2


def test_deg_p_n_linear():
    p = Polynom([Rational.from_str("-3/4"), Rational.from_str("2/1")])
    result = DEG_P_N(p)
    assert result == 1


def test_deg_p_n_constant():
    p = Polynom([Rational.from_str("7/1")])
    result = DEG_P_N(p)
    assert result == 0


def test_deg_p_n_zero():
    p = Polynom([Rational.from_str("0")])
    result = DEG_P_N(p)
    assert result == 0


def test_deg_p_n_cubic():
    p = Polynom(
        [
            Rational.from_str("1"),
            Rational.from_str("-2"),
            Rational.from_str("0"),
            Rational.from_str("3/1"),
        ]
    )
    result = DEG_P_N(p)
    assert result == 3


def test_deg_p_n_leading_zeros_stripped():
    p = Polynom(
        [
            Rational.from_str("1"),
            Rational.from_str("2"),
            Rational.from_str("0"),
            Rational.from_str("0"),
        ]
    )
    result = DEG_P_N(p)
    assert result == 1


def test_deg_p_n_high_degree():
    coeffs = [Rational.from_str("0")] * 10 + [Rational.from_str("1/1")]
    p = Polynom(coeffs)
    result = DEG_P_N(p)
    assert result == 10


def test_deg_p_n_negative_coefficients():
    p = Polynom(
        [Rational.from_str("-1/2"), Rational.from_str("0"), Rational.from_str("-3/1")]
    )
    result = DEG_P_N(p)
    assert result == 2


def test_deg_p_n_invalid_input():
    with pytest.raises(ValueError):
        DEG_P_N("not a polynom")  # type: ignore

    with pytest.raises(ValueError):
        DEG_P_N(3.14)  # type: ignore

    with pytest.raises(ValueError):
        DEG_P_N(None)  # type: ignore
