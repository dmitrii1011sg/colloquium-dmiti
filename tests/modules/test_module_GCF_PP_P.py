import pytest
from core.base.Polynom import Polynom
from core.modules.PModule.GCF_PP_P import GCF_PP_P


def test_gcf_pp_simple_case():
    f = Polynom.from_str("x^2 - 1")
    g = Polynom.from_str("x - 1")
    result = GCF_PP_P(f, g)
    assert str(result) == "x - 1"


def test_gcf_pp_coprime():
    f = Polynom.from_str("x^2 + 1")
    g = Polynom.from_str("x - 1")
    result = GCF_PP_P(f, g)
    assert str(result) == "1"


def test_gcf_pp_with_constant_factor():
    f = Polynom.from_str("2x^2 + 4x + 2")
    g = Polynom.from_str("3x + 3")
    result = GCF_PP_P(f, g)
    assert str(result) == "x + 1"


def test_gcf_pp_first_is_multiple():
    f = Polynom.from_str("4x^3 - 2x^2 + 6x - 2")
    g = Polynom.from_str("2x^3 - x^2 + 3x - 1")
    result = GCF_PP_P(f, g)
    expected = Polynom.from_str("x^3 - 1/2x^2 + 3/2x - 1/2")
    assert str(result) == str(expected)


def test_gcf_pp_both_zero():
    f = Polynom.from_str("0")
    g = Polynom.from_str("0")
    result = GCF_PP_P(f, g)
    assert str(result) == "0"


def test_gcf_pp_second_is_zero():
    f = Polynom.from_str("3x + 6")
    g = Polynom.from_str("0")
    result = GCF_PP_P(g, f)
    assert str(result) == "x + 2"


def test_gcf_pp_with_fractions():
    f = Polynom.from_str("1/2x^2 + x + 1/2")
    g = Polynom.from_str("1/3x + 1/3")
    result = GCF_PP_P(f, g)
    assert str(result) == "x + 1"


def test_gcf_pp_invalid_input_first():
    with pytest.raises(ValueError):
        GCF_PP_P("not a polynom", Polynom.from_str("x"))


def test_gcf_pp_invalid_input_second():
    with pytest.raises(ValueError):
        GCF_PP_P(Polynom.from_str("x"), "not a polynom")


def test_gcf_pp_both_invalid():
    with pytest.raises(ValueError):
        GCF_PP_P("invalid", "invalid")


def test_gcf_pp_quadratic_and_linear():
    f = Polynom.from_str("x^2 - 4")
    g = Polynom.from_str("x + 2")
    result = GCF_PP_P(f, g)
    assert str(result) == "x + 2"


def test_gcf_pp_negative_leading_coefficient():
    f = Polynom.from_str("-x^2 + 1")
    g = Polynom.from_str("x - 1")
    result = GCF_PP_P(f, g)
    assert str(result) == "x - 1"


def test_gcf_pp_equal_polynomials():
    f = Polynom.from_str("2x^3 - 4x^2 + 2x")
    g = Polynom.from_str("2x^3 - 4x^2 + 2x")
    result = GCF_PP_P(f, g)
    assert str(result) == "x^3 - 2x^2 + x"
