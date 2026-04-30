# Литвиненко Владимир 5381

from core.base.Integer import Integer
from core.modules.NModule.MUL_NN_N import MUL_NN_N
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
from core.modules.ZModule.MUL_ZM_Z import MUL_ZM_Z
from core.modules.ZModule.POZ_Z_D import POZ_Z_D


def MUL_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Умножение целых чисел

    Args:
        a (Integer): Первый множитель.
        b (Integer): Второй множитель.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Integer: Произведение чисел.
    """

    if not isinstance(a, Integer) or not isinstance(b, Integer):
        raise ValueError("Invalid Value")

    if POZ_Z_D(a) == 0 or POZ_Z_D(b) == 0:
        return Integer.from_int(0)

    abs_a = ABS_Z_N(a)
    abs_b = ABS_Z_N(b)
    sign_a = POZ_Z_D(a)
    sign_b = POZ_Z_D(b)

    result = Integer(MUL_NN_N(abs_a, abs_b), 0)
    return result if sign_a == sign_b else MUL_ZM_Z(result)
