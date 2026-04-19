import random
import pytest
from core.base.Natural import Natural
from core.modules.DIV_NN_Dk import DIV_NN_Dk


def test_div_nn_dk():
    a = Natural.from_str("12345")
    b = Natural.from_str("67")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "1"
    assert str(DIV_NN_Dk(a, b, 1)) == "8"
    assert str(DIV_NN_Dk(a, b, 2)) == "4"
    assert str(DIV_NN_Dk(a, b, 3)) == "2"
    assert str(DIV_NN_Dk(a, b, 4)) == "5"
    assert str(DIV_NN_Dk(a, b, 5)) == "3"


def test_div_nn_dk_simple():
    a = Natural.from_str("100")
    b = Natural.from_str("25")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "4"
    assert str(DIV_NN_Dk(a, b, 1)) == "0"


def test_div_nn_dk_equal():
    a = Natural.from_str("50")
    b = Natural.from_str("50")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "1"
    assert str(DIV_NN_Dk(a, b, 1)) == "0"


def test_div_nn_dk_larger_first():
    a = Natural.from_str("50")
    b = Natural.from_str("100")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "2"


def test_div_nn_dk_exact():
    a = Natural.from_str("1000")
    b = Natural.from_str("8")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "1"
    assert str(DIV_NN_Dk(a, b, 1)) == "2"
    assert str(DIV_NN_Dk(a, b, 2)) == "5"
    assert str(DIV_NN_Dk(a, b, 3)) == "0"


def test_div_nn_dk_repeating():
    a = Natural.from_str("10")
    b = Natural.from_str("3")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "3"
    assert str(DIV_NN_Dk(a, b, 1)) == "3"
    assert str(DIV_NN_Dk(a, b, 2)) == "3"
    assert str(DIV_NN_Dk(a, b, 3)) == "3"


def test_div_nn_dk_k_zero():
    a = Natural.from_str("999")
    b = Natural.from_str("3")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "3"


def test_div_nn_dk_k_out_of_range():
    a = Natural.from_str("100")
    b = Natural.from_str("3")
    
    assert str(DIV_NN_Dk(a, b, 10)) == "3"


def test_div_nn_dk_zero_division():
    a = Natural.from_str("100")
    b = Natural.from_str("0")
    
    with pytest.raises(ZeroDivisionError):
        DIV_NN_Dk(a, b, 0)


@pytest.mark.parametrize("iteration", range(10))
def test_div_nn_dk_random(iteration):
    val1 = random.randint(1, 10**50)
    val2 = random.randint(1, 10**25)
    k = random.randint(0, 15)
    
    a = Natural.from_int(val1)
    b = Natural.from_int(val2)
    
    if val1 >= val2:
        quotient = val1 // val2
        remainder = val1 % val2
    else:
        quotient = val2 // val1
        remainder = val2 % val1
    
    quotient_str = str(quotient)
    
    if k < len(quotient_str):
        expected = int(quotient_str[k])
    else:
        remainder_val = remainder
        for i in range(k - len(quotient_str) + 1):
            remainder_val *= 10
            digit = remainder_val // min(val1, val2)
            remainder_val %= min(val1, val2)
            expected = digit if i == k - len(quotient_str) else expected
    
    assert str(DIV_NN_Dk(a, b, k)) == str(expected)


def test_div_nn_dk_huge_numbers():
    base_str = "9" * 10000
    a = Natural.from_str(base_str)
    b = Natural.from_str("3")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "3"
    assert str(DIV_NN_Dk(a, b, 5000)) == "3"
    assert str(DIV_NN_Dk(a, b, 9999)) == "3"


def test_div_nn_dk_one_digit():
    a = Natural.from_str("7")
    b = Natural.from_str("2")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "3"
    assert str(DIV_NN_Dk(a, b, 1)) == "5"


def test_div_nn_dk_pi():
    a = Natural.from_str("355")
    b = Natural.from_str("113")
    
    assert str(DIV_NN_Dk(a, b, 0)) == "3"
    assert str(DIV_NN_Dk(a, b, 1)) == "1"
    assert str(DIV_NN_Dk(a, b, 2)) == "4"
    assert str(DIV_NN_Dk(a, b, 3)) == "1"
    assert str(DIV_NN_Dk(a, b, 4)) == "5"
    assert str(DIV_NN_Dk(a, b, 5)) == "9"


def test_div_nn_dk_negative_k():
    a = Natural.from_int(100)
    b = Natural.from_int(3)
    
    with pytest.raises(ValueError):
        DIV_NN_Dk(a, b, -1)


def test_div_nn_dk_invalid_input():
    a = Natural.from_int(10)
    b = Natural.from_int(5)
    
    with pytest.raises(ValueError):
        DIV_NN_Dk("10", b, 0)
    
    with pytest.raises(ValueError):
        DIV_NN_Dk(a, "5", 0)