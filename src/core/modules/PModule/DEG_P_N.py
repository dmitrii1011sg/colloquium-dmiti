# Литвиненко Владимир 5381

from core.base.Polynom import Polynom


def DEG_P_N(p: Polynom) -> int:
    """
    Нахождение степени многочлена.

    Args:
         p (Polynom): Многочлен.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Int : Целое число, являющееся степенью многочлена.
    """

    if not isinstance(p, Polynom):
        raise ValueError("Invalid value")

    return p.degree
