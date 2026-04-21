from core.base.Natural import Natural
from core.modules.COM_NN_D import COM_NN_D
# Жуков Александр 5381

def SUB_NN_N(a: Natural, b: Natural) -> Natural:
    """
    Вычитание из первого натурального числа второго.

    Первое число должно быть больше или равно второму.

    Args:
        a (Natural): Уменьшаемое.
        b (Natural): Вычитаемое.

    Raises:
        ValueError: Параметры не соответствуют типам или a < b.

    Returns:
        Natural: Натуральное число, равное a - b.
    """
    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid value")

    if COM_NN_D(a, b) == 1:
        raise ValueError("Invalid value")

    result_digits: list[int] = []
    borrow = 0

    for i in range(a.length):
        digit_a = a.digits[i]
        digit_b = b.digits[i] if i < b.length else 0
        diff = digit_a - digit_b - borrow

        if diff < 0:
            diff += 10
            borrow = 1
        else:
            borrow = 0

        result_digits.append(diff)

    return Natural(result_digits, need_reverse=False)
