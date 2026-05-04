# Литвиненко Владимир 5381

from core.base.Natural import Natural
from core.base.Polynom import Polynom


def DEG_P_N(p: Polynom) -> Natural:
    """
    Нахождение степени многочлена.

    Args:
         p (Polynom): Многочлен.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Natural : Натуральное число, являющееся степенью многочлена.
    """

    if not isinstance(p, Polynom):
        raise ValueError("Invalid value")

    return Natural.from_int(p.degree)
