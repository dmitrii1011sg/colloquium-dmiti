import pytest
from core.base.Polynom import Polynom
from core.modules.PModule.DER_P_P import DER_P_P


def test_der_pp_linear():
    f = Polynom.from_str("2x + 3")
    result = DER_P_P(f)
    assert str(result) == "2"


def test_der_pp_quadratic():
    f = Polynom.from_str("3x^2 + 2x + 1")
    result = DER_P_P(f)
    assert str(result) == "6x + 2"


def test_der_pp_cubic():
    f = Polynom.from_str("x^3 - 3x^2 + 3x - 1")
    result = DER_P_P(f)
    assert str(result) == "3x^2 - 6x + 3"


def test_der_pp_constant():
    f = Polynom.from_str("5")
    result = DER_P_P(f)
    assert str(result) == "0"


def test_der_pp_zero():
    f = Polynom.from_str("0")
    result = DER_P_P(f)
    assert str(result) == "0"


def test_der_pp_monomial():
    f = Polynom.from_str("x^4")
    result = DER_P_P(f)
    assert str(result) == "4x^3"


def test_der_pp_with_fractions():
    f = Polynom.from_str("1/2 x^2 + 1/3 x + 1/4")
    result = DER_P_P(f)
    assert str(result) == "x + 1/3"


def test_der_pp_negative_coefficients():
    f = Polynom.from_str("-2x^3 + 5x^2 - 4x + 1")
    result = DER_P_P(f)
    assert str(result) == "-6x^2 + 10x - 4"


def test_der_pp_higher_degree():
    f = Polynom.from_str("x^7 + 3x^5 - 2x^3 + x")
    result = DER_P_P(f)
    assert str(result) == "7x^6 + 15x^4 - 6x^2 + 1"


def test_der_pp_invalid_input():
    with pytest.raises(ValueError):
        DER_P_P("not a polynom")


def test_der_pp_no_x_term():
    f = Polynom.from_str("5x^2 + 3")
    result = DER_P_P(f)
    assert str(result) == "10x"


def test_der_pp_all_terms():
    f = Polynom.from_str("x^5 + 4x^4 + 3x^3 + 2x^2 + x + 1")
    result = DER_P_P(f)
    assert str(result) == "5x^4 + 16x^3 + 9x^2 + 4x + 1"
