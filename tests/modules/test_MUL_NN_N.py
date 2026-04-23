import random
import pytest
from core.base.Natural import Natural
from core.modules.MUL_NN_N import MUL_NN_N


def test_mul_nn_n():
    """Базовые тесты умножения"""
    # 0 * любое = 0
    a1 = Natural.from_str("0")
    b1 = Natural.from_str("123")
    assert str(MUL_NN_N(a1, b1)) == "0"
    
    # любое * 0 = 0
    a2 = Natural.from_str("456")
    b2 = Natural.from_str("0")
    assert str(MUL_NN_N(a2, b2)) == "0"
    
    # 1 * число = число
    a3 = Natural.from_str("1")
    b3 = Natural.from_str("12345")
    assert str(MUL_NN_N(a3, b3)) == "12345"
    
    # число * 1 = число
    a4 = Natural.from_str("6789")
    b4 = Natural.from_str("1")
    assert str(MUL_NN_N(a4, b4)) == "6789"
    
    # небольшие числа
    a5 = Natural.from_str("12")
    b5 = Natural.from_str("34")
    assert str(MUL_NN_N(a5, b5)) == "408"  # 12 * 34 = 408
    
    a6 = Natural.from_str("123")
    b6 = Natural.from_str("45")
    assert str(MUL_NN_N(a6, b6)) == "5535"  # 123 * 45 = 5535


@pytest.mark.parametrize("iteration", range(10))
def test_mul_nn_n_random(iteration):
    """Случайные тесты с большими числами"""
    val1 = random.randint(0, 10**50)
    val2 = random.randint(0, 10**50)
    
    a = Natural.from_int(val1)
    b = Natural.from_int(val2)
    
    result = MUL_NN_N(a, b)
    expected = val1 * val2
    
    assert str(result) == str(expected)


def test_mul_nn_n_huge_numbers():
    """Тест с огромными числами"""
    # 999...9 * 999...9
    size = 100
    base_str = "9" * size
    a = Natural.from_str(base_str)
    b = Natural.from_str(base_str)
    
    result = MUL_NN_N(a, b)
    # 99*99=9801, 999*999=998001, 9999*9999=99980001
    expected_str = "9" * (size - 1) + "8" + "0" * (size - 1) + "1"
    
    assert str(result) == expected_str


def test_mul_nn_n_extreme_cases():
    """Крайние случаи"""
    # 10^k * 10^m = 10^(k+m)
    a = Natural.from_str("1" + "0" * 100)
    b = Natural.from_str("1" + "0" * 50)
    result = MUL_NN_N(a, b)
    assert str(result) == "1" + "0" * 150
    
    # Огромное число на 0
    a = Natural.from_str("1" + "0" * 1000)
    b = Natural.from_str("0")
    assert str(MUL_NN_N(a, b)) == "0"
    
    # Огромное число на 1
    a = Natural.from_str("123456789" * 100)
    b = Natural.from_str("1")
    assert str(MUL_NN_N(a, b)) == str(a)


def test_mul_nn_n_commutative():
    """Проверка коммутативности: a * b == b * a"""
    test_cases = [
        ("12", "34"),
        ("123", "456"),
        ("999", "1"),
        ("0", "12345"),
        ("1" + "0" * 50, "987654321"),
    ]
    
    for str_a, str_b in test_cases:
        a = Natural.from_str(str_a)
        b = Natural.from_str(str_b)
        
        ab = MUL_NN_N(a, b)
        ba = MUL_NN_N(b, a)
        
        assert str(ab) == str(ba)


def test_mul_nn_n_associative():
    """Проверка ассоциативности: (a * b) * c == a * (b * c)"""
    a = Natural.from_str("12")
    b = Natural.from_str("34")
    c = Natural.from_str("56")
    
    ab_then_c = MUL_NN_N(MUL_NN_N(a, b), c)
    a_then_bc = MUL_NN_N(a, MUL_NN_N(b, c))
    
    assert str(ab_then_c) == str(a_then_bc)
    # 12 * 34 * 56 = 12 * 1904 = 22848, 12 * 34 = 408, 408 * 56 = 22848


def test_mul_nn_n_distributive():
    """Проверка дистрибутивности: a * (b + c) == a * b + a * c"""
    from core.modules.ADD_NN_N import ADD_NN_N
    
    a = Natural.from_str("12")
    b = Natural.from_str("34")
    c = Natural.from_str("56")
    
    left = MUL_NN_N(a, ADD_NN_N(b, c))
    right = ADD_NN_N(MUL_NN_N(a, b), MUL_NN_N(a, c))
    
    assert str(left) == str(right)


def test_mul_nn_n_no_mutation():
    """Проверка, что исходные числа не изменяются"""
    a = Natural.from_str("12345")
    b = Natural.from_str("67890")
    
    original_a_digits = list(a.digits)
    original_b_digits = list(b.digits)
    original_a_length = a.length
    original_b_length = b.length
    
    _ = MUL_NN_N(a, b)
    
    assert a.digits == original_a_digits
    assert b.digits == original_b_digits
    assert a.length == original_a_length
    assert b.length == original_b_length