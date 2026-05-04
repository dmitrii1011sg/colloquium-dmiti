# Литвиненко Владимир 5381

from core.base.Polynom import Polynom
from core.base.Rational import Rational


def LED_P_Q(p: Polynom) -> Rational:
    """
    Нахождение старшего коэффициента многочлена.

    Args:
         p (Polynom): Многочлен.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Rational : Рациональное число, являющееся старшим коэффициентом многочлена.
    """

    if not isinstance(p, Polynom):
        raise ValueError("Invalid value")

    return p.coefficients[-1]
