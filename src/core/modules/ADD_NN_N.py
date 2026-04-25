from core.base.Natural import Natural
from core.modules.COM_NN_D import COM_NN_D

# Жуков Александр 5381


def ADD_NN_N(a: Natural, b: Natural) -> Natural:
    """
    Сложение двух натуральных чисел.

    Args:
        a (Natural): Первое слагаемое.
        b (Natural): Второе слагаемое.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Natural: Натуральное число, равное a + b.
    """
    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid value")

    bigger, smaller = (b, a) if COM_NN_D(a, b) == 1 else (a, b)

    result_digits: list[int] = []
    carry = 0

    for i in range(bigger.length):
        digit_big = bigger.digits[i]
        digit_small = smaller.digits[i] if i < smaller.length else 0
        total = digit_big + digit_small + carry
        result_digits.append(total % 10)
        carry = total // 10

    if carry > 0:
        result_digits.append(carry)

    return Natural(result_digits, need_reverse=False)
