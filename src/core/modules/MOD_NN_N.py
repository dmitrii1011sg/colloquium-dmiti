from core.base.Natural import Natural
from core.modules.COM_NN_D import COM_NN_D
from core.modules.DIV_NN_N import DIV_NN_N
from core.modules.SUB_NDN_N import SUB_NDN_N
from core.modules.MUL_Nk_N import MUL_Nk_N
# Жуков Александр 5381

def MOD_NN_N(a: Natural, b: Natural) -> Natural:
    """
    Остаток от деления первого натурального числа на второе.

    Args:
        a (Natural): Делимое.
        b (Natural): Делитель (отличный от нуля).

    Raises:
        ValueError: Параметры не соответствуют типам или делитель равен нулю.

    Returns:
        Natural: Натуральное число, равное a mod b.
    """
    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid value")

    if b.length == 1 and b.digits[0] == 0:
        raise ValueError("Division by zero")

    if COM_NN_D(a, b) == 1:
        return a

    quot = DIV_NN_N(a, b)
    result = a

    for power in range(quot.length):
        digit = quot.digits[power]
        if digit == 0:
            continue
        digit_num = Natural([digit], need_reverse=False)
        divisor_shifted = MUL_Nk_N(b, Natural.from_int(power))
        result = SUB_NDN_N(result, divisor_shifted, digit_num)

    return result
