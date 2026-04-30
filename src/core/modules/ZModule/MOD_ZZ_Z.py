# Литвиненко Владимир 5381

from core.base.Integer import Integer
from core.modules.ZModule.DIV_ZZ_Z import DIV_ZZ_Z
from core.modules.ZModule.MUL_ZZ_Z import MUL_ZZ_Z
from core.modules.ZModule.SUB_ZZ_Z import SUB_ZZ_Z


def MOD_ZZ_Z(a: Integer, b: Integer) -> Integer:
    """
    Остаток от деления целого на целое (делитель отличен от нуля)

    Результат удовлетворяет: a = b * q + r, где 0 <= r < |b|

    Args:
        a (Integer): Делимое.
        b (Integer): Делитель.

    Raises:
        ValueError: Параметры не соответствуют типам или делитель равен нулю.

    Returns:
        Integer: Неотрицательный остаток от деления чисел.
    """

    if not isinstance(a, Integer) or not isinstance(b, Integer):
        raise ValueError("Invalid Value")

    if b.number.length == 1 and b.number.digits[0] == 0:
        raise ValueError("Division by zero")

    if a.number.length == 1 and a.number.digits[0] == 0:
        return Integer.from_int(0)

    q = DIV_ZZ_Z(a, b)
    mul = MUL_ZZ_Z(b, q)
    r = SUB_ZZ_Z(a, mul)

    return r
