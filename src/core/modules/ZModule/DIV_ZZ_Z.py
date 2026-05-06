# Литвиненко Владимир 5381

from core.base.Integer import Integer
from core.modules.NModule.ADD_1N_N import ADD_1N_N
from core.modules.NModule.COM_NN_D import COM_NN_D
from core.modules.NModule.DIV_NN_N import DIV_NN_N
from core.modules.NModule.MUL_NN_N import MUL_NN_N
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
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

    if b.is_zero():
        raise ValueError("Division by zero")

    if a.is_zero():
        return Integer.from_int(0)

    abs_a = ABS_Z_N(a)
    abs_b = ABS_Z_N(b)

    q_nat = DIV_NN_N(abs_a, abs_b)
    product = MUL_NN_N(q_nat, abs_b)
    has_remainder = COM_NN_D(product, abs_a) != 0

    a_sign = POZ_Z_D(a)
    b_sign = POZ_Z_D(b)

    if a_sign == b_sign:
        result = Integer(q_nat, 0)
    else:
        if has_remainder:
            q_nat = ADD_1N_N(q_nat)
        result = Integer(q_nat, 1)

    return result
