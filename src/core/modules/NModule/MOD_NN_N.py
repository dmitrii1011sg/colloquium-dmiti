from core.base.Natural import Natural
from core.modules.NModule.COM_NN_D import COM_NN_D
from core.modules.NModule.DIV_NN_N import DIV_NN_N
from core.modules.NModule.MUL_NN_N import MUL_NN_N
from core.modules.NModule.SUB_NN_N import SUB_NN_N

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

    res_div = DIV_NN_N(a, b)
    res_mul = MUL_NN_N(b, res_div)
    result = SUB_NN_N(a, res_mul)

    return result
