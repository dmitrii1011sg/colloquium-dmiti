import pytest
from core.base.Polynom import Polynom
from core.modules.PModule.NMR_P_P import NMR_P_P


def test_nmr_pp_simple_case():
    f = Polynom.from_str("x^3 - 3x^2 + 3x - 1")
    result = NMR_P_P(f)
    assert str(result) == "x - 1"


def test_nmr_pp_no_multiple_roots():
    f = Polynom.from_str("x^2 - 5x + 6")
    result = NMR_P_P(f)
    assert str(result) == "x^2 - 5x + 6"


def test_nmr_pp_with_constant_factor():
    f = Polynom.from_str("2x^2 - 4x + 2")
    result = NMR_P_P(f)
    assert str(result) in "2x - 2"


def test_nmr_pp_zero_polynomial():
    f = Polynom.from_str("0")
    result = NMR_P_P(f)
    assert str(result) == "0"


def test_nmr_pp_constant_polynomial():
    f = Polynom.from_str("5")
    result = NMR_P_P(f)
    assert str(result) == "5"


def test_nmr_pp_quadratic_perfect_square():
    f = Polynom.from_str("x^2 + 6x + 9")
    result = NMR_P_P(f)
    assert str(result) == "x + 3"


def test_nmr_pp_higher_degree():
    f = Polynom.from_str("x^4")
    result = NMR_P_P(f)
    assert str(result) == "x"


def test_nmr_pp_invalid_input():
    with pytest.raises(ValueError):
        NMR_P_P("not a polynom")


def test_nmr_pp_negative_coefficients():
    f = Polynom.from_str("-x^3 + 3x^2 - 3x + 1")
    result = NMR_P_P(f)
    assert str(result) in "-x + 1"
