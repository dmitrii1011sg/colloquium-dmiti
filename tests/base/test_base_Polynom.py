import pytest
from core.base.Polynom import Polynom
from core.base.Rational import Rational


def _r(s: str) -> Rational:
    return Rational.from_str(s)


def test_polynom_creation():
    p = Polynom([_r("3"), _r("0"), _r("5")])
    assert p.degree == 2
    assert str(p) == "5x^2 + 3"


def test_polynom_constant():
    p = Polynom([_r("7")])
    assert p.degree == 0
    assert str(p) == "7"


def test_polynom_zero():
    p = Polynom([_r("0")])
    assert p.degree == 0
    assert str(p) == "0"


def test_polynom_strip_leading_zeros():
    p = Polynom([_r("1"), _r("2"), _r("0"), _r("0")])
    assert p.degree == 1
    assert str(p) == "2x + 1"


def test_polynom_all_zeros():
    p = Polynom([_r("0"), _r("0"), _r("0")])
    assert p.degree == 0
    assert str(p) == "0"


def test_polynom_linear():
    p = Polynom([_r("3"), _r("1")])
    assert p.degree == 1
    assert str(p) == "x + 3"


def test_polynom_negative_coefficients():
    p = Polynom([_r("-3"), _r("-2"), _r("1")])
    assert p.degree == 2
    assert str(p) == "x^2 - 2x - 3"


def test_polynom_rational_coefficients():
    p = Polynom([_r("1/2"), _r("-3/4"), _r("5/6")])
    assert p.degree == 2
    assert str(p) == "5/6x^2 - 3/4x + 1/2"


def test_polynom_with_zero_middle():
    p = Polynom([_r("1"), _r("0"), _r("0"), _r("1")])
    assert p.degree == 3
    assert str(p) == "x^3 + 1"


def test_polynom_invalid_data():
    with pytest.raises(ValueError):
        Polynom([])
    with pytest.raises(ValueError):
        Polynom("not a list")
    with pytest.raises(ValueError):
        Polynom([1, 2, 3])
    with pytest.raises(ValueError):
        Polynom([_r("1"), "x", _r("2")])


def test_polynom_repr():
    p = Polynom([_r("3"), _r("0"), _r("5")])
    assert repr(p) == "Polynom(5x^2 + 3)"


def test_polynom_fields():
    p = Polynom([_r("1/2"), _r("3")])
    assert isinstance(p.coefficients, list)
    assert all(isinstance(c, Rational) for c in p.coefficients)
    assert isinstance(p.degree, int)
    assert len(p.coefficients) == p.degree + 1


def test_polynom_high_degree():
    coeffs = [_r("0")] * 9 + [_r("1")]
    p = Polynom(coeffs)
    assert p.degree == 9
    assert str(p) == "x^9"
