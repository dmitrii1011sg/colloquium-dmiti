from core.base.Polynom import Polynom
from core.modules.PModule.DIV_PP_P import DIV_PP_P
from core.modules.PModule.MUL_PP_P import MUL_PP_P
from core.modules.PModule.SUB_PP_P import SUB_PP_P

# Кацеба Андрей 5381


def MOD_PP_P(a: Polynom, b: Polynom) -> Polynom:
    """
    Остаток от деления многочлена на многочлен.

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.
        b (Polynom): Многочлен с рациональными коэффициентами.

    Raises:
        ValueError: Параметр не соответствует типу.
        ZeroDivisionError: делитель равен нулю.

    Returns:
        Polynom :  Остаток от деления многочлена на многочлен.
    """

    if not (isinstance(a, Polynom) and isinstance(b, Polynom)):
        raise ValueError("Invalid value")

    if (
        b.coefficients[-1].numer.number.digits[0] == 0
        and b.coefficients[-1].numer.number.length == 1
    ):
        raise ZeroDivisionError("invalid value")

    temp = DIV_PP_P(a, b)

    return SUB_PP_P(a, MUL_PP_P(temp, b))
