from core.base.Natural import Natural
from core.modules.NModule.ADD_NN_N import ADD_NN_N
from core.modules.NModule.COM_NN_D import COM_NN_D
from core.modules.NModule.DIV_NN_Dk import DIV_NN_Dk
from core.modules.NModule.MUL_Nk_N import MUL_Nk_N
from core.modules.NModule.SUB_NDN_N import SUB_NDN_N

# Жуков Александр 5381


def DIV_NN_N(a: Natural, b: Natural) -> Natural:
    """
    Неполное частное от деления первого натурального числа на второе.

    Args:
        a (Natural): Делимое.
        b (Natural): Делитель (отличный от нуля).

    Raises:
        ValueError: Параметры не соответствуют типам или делитель равен нулю.

    Returns:
        Natural: Натуральное число, равное целой части от a / b.
    """
    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid value")

    if b.length == 1 and b.digits[0] == 0:
        raise ValueError("Division by zero")

    if COM_NN_D(a, b) == 1:
        return Natural([0], need_reverse=False)

    current = a
    result = Natural([0], need_reverse=False)

    while COM_NN_D(current, b) != 1:
        digit, power = DIV_NN_Dk(current, b)
        digit_num = Natural([digit], need_reverse=False)
        divisor_shifted = MUL_Nk_N(b, Natural.from_int(power))
        current = SUB_NDN_N(current, divisor_shifted, digit_num)
        partial = MUL_Nk_N(digit_num, Natural.from_int(power))
        result = ADD_NN_N(result, partial)

    return result
