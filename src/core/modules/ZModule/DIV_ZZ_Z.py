# Литвиненко Владимир 5381

from core.base.Integer import Integer
from core.modules.NModule.DIV_NN_N import DIV_NN_N
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
from core.modules.ZModule.MUL_ZM_Z import MUL_ZM_Z
from core.modules.ZModule.POZ_Z_D import POZ_Z_D


def DIV_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Частное от деления целого на целое (делитель отличен от нуля)

    Args:
        a (Integer): Делимое.
        b (Integer): Делитель.

    Raises:
        ValueError: Параметры не соответствуют типам или делитель равен нулю.

    Returns:
        Integer: Частное от деления чисел.
    """

    if not isinstance(a, Integer) or not isinstance(b, Integer):
        raise ValueError("Invalid Value")

    abs_a = ABS_Z_N(a)
    abs_b = ABS_Z_N(b)
    sign_a = POZ_Z_D(a)
    sign_b = POZ_Z_D(b)

    if sign_b == 0:
        raise ValueError("Division by zero")

    result = Integer(DIV_NN_N(abs_a, abs_b), 0)
    return result if sign_a == sign_b else MUL_ZM_Z(result)
