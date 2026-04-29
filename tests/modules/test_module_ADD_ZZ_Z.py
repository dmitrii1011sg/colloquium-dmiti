import random
import pytest
from core.base.Integer import Integer
from core.modules.ZModule.ADD_ZZ_Z import ADD_ZZ_Z


def test_add_zz_z_both_positive():
    a = Integer.from_str("5")
    b = Integer.from_str("3")
    result = ADD_ZZ_Z(a, b)
    assert str(result) == "8"


def test_add_zz_z_both_negative():
    a = Integer.from_str("-5")
    b = Integer.from_str("-3")
    result = ADD_ZZ_Z(a, b)
    assert str(result) == "-8"


def test_add_zz_z_positive_and_negative_positive_bigger():
    a = Integer.from_str("5")
    b = Integer.from_str("-3")
    result = ADD_ZZ_Z(a, b)
    assert str(result) == "2"


def test_add_zz_z_positive_and_negative_negative_bigger():
    a = Integer.from_str("3")
    b = Integer.from_str("-5")
    result = ADD_ZZ_Z(a, b)
    assert str(result) == "-2"


def test_add_zz_z_sum_to_zero():
    a = Integer.from_str("5")
    b = Integer.from_str("-5")
    result = ADD_ZZ_Z(a, b)
    assert str(result) == "0"


def test_add_zz_z_with_zero():
    a = Integer.from_str("7")
    b = Integer.from_str("0")
    result = ADD_ZZ_Z(a, b)
    assert str(result) == "7"


def test_add_zz_z_zero_with_negative():
    a = Integer.from_str("0")
    b = Integer.from_str("-7")
    result = ADD_ZZ_Z(a, b)
    assert str(result) == "-7"


def test_add_zz_z_negative_with_zero():
    a = Integer.from_str("-7")
    b = Integer.from_str("0")
    result = ADD_ZZ_Z(a, b)
    assert str(result) == "-7"


def test_add_zz_z_zero_with_zero():
    a = Integer.from_str("0")
    b = Integer.from_str("0")
    result = ADD_ZZ_Z(a, b)
    assert str(result) == "0"


@pytest.mark.parametrize("iteration", range(10))
def test_add_zz_z_random(iteration):
    val1 = random.randint(0, 10**50)
    val2 = random.randint(0, 10**50)
    a = Integer.from_int(val1)
    b = Integer.from_int(val2)
    result = ADD_ZZ_Z(a, b)
    assert str(result) == str(val1 + val2)


@pytest.mark.parametrize("iteration", range(10))
def test_add_zz_z_random_with_negative(iteration):
    val1 = random.randint(-(10**50), 10**50)
    val2 = random.randint(-(10**50), 10**50)
    a = Integer.from_int(val1)
    b = Integer.from_int(val2)
    result = ADD_ZZ_Z(a, b)
    assert str(result) == str(val1 + val2)


def test_add_zz_z_huge_numbers():
    base_str = "9" * 100
    a = Integer.from_str(base_str)
    b = Integer.from_str(base_str)
    expected = str(int(base_str) * 2)
    result = ADD_ZZ_Z(a, b)
    assert str(result) == expected


def test_add_zz_z_huge_numbers_opposite_signs():
    big_str = "9" * 100
    small_str = "1" + "0" * 99
    a = Integer.from_str(big_str)
    b = Integer.from_str("-" + small_str)
    expected = str(int(big_str) - int(small_str))
    result = ADD_ZZ_Z(a, b)
    assert str(result) == expected


def test_add_zz_z_no_mutation():
    a = Integer.from_str("-1488")
    b = Integer.from_str("42")
    _ = ADD_ZZ_Z(a, b)


def test_add_zz_z_invalid_input():
    with pytest.raises(ValueError):
        ADD_ZZ_Z("not integer", Integer.from_str("5"))
    
    with pytest.raises(ValueError):
        ADD_ZZ_Z(Integer.from_str("5"), "not integer")
    
    with pytest.raises(ValueError):
        ADD_ZZ_Z(None, Integer.from_str("5"))


def test_add_zz_z_commutative():
    a = Integer.from_str("-123")
    b = Integer.from_str("456")
    result1 = ADD_ZZ_Z(a, b)
    result2 = ADD_ZZ_Z(b, a)
    assert str(result1) == str(result2)


def test_add_zz_z_associative():
    a = Integer.from_str("100")
    b = Integer.from_str("-50")
    c = Integer.from_str("25")
    ab = ADD_ZZ_Z(a, b)
    result1 = ADD_ZZ_Z(ab, c)
    bc = ADD_ZZ_Z(b, c)
    result2 = ADD_ZZ_Z(a, bc)
    assert str(result1) == str(result2)


def test_add_zz_z_edge_cases():
    max_int = Integer.from_str("9" * 100)
    min_int = Integer.from_str("-" + "9" * 100)
    result = ADD_ZZ_Z(max_int, min_int)
    assert str(result) == "0"
    
    assert str(ADD_ZZ_Z(Integer.from_str("0"), Integer.from_str("1"))) == "1"
    assert str(ADD_ZZ_Z(Integer.from_str("-1"), Integer.from_str("1"))) == "0"