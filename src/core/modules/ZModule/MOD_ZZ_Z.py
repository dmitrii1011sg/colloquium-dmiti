# Литвиненко Владимир 5381

from core.base.Integer import Integer
from core.modules.ZModule.DIV_ZZ_Z import DIV_ZZ_Z
from core.modules.ZModule.MUL_ZZ_Z import MUL_ZZ_Z
from core.modules.ZModule.POZ_Z_D import POZ_Z_D
from core.modules.ZModule.SUB_ZZ_Z import SUB_ZZ_Z


def MOD_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Остаток от деления целого на целое (делитель отличен от нуля)

    Args:
        a (Integer): Делимое.
        b (Integer): Делитель.

    Raises:
        ValueError: Параметры не соответствуют типам или делитель равен нулю.

    Returns:
        Integer: Остаток от деления чисел.
    """

    if not isinstance(a, Integer) or not isinstance(b, Integer):
        raise ValueError("Invalid Value")

    if POZ_Z_D(b) == 0:
        raise ValueError("Division by zero")

    q = DIV_ZZ_Z(a, b)
    mul_bq = MUL_ZZ_Z(b, q)
    r = SUB_ZZ_Z(a, mul_bq)

    return r
