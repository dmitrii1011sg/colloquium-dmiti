import pytest
from core.base.Natural import Natural


def test_natural_creation():
    n = Natural([1, 2, 3], need_reverse=True)
    assert n.digits == [3, 2, 1]
    assert n.length == 3


def test_natural_from_str():
    n = Natural.from_str("1230")
    assert str(n) == "1230"
    assert n.digits == [0, 3, 2, 1]


def test_strip_zeros():
    n = Natural([7, 0, 0], need_reverse=False)
    assert n.digits == [7]
    assert n.length == 1


def test_invalid_data():
    with pytest.raises(ValueError):
        Natural.from_str("abc")
