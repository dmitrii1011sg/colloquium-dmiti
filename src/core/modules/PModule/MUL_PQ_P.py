from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.QModule.MUL_QQ_Q import MUL_QQ_Q

# Жулин Максим 5381


def MUL_PQ_P(a: Polynom, b: Rational) -> Polynom:
    """
    Умножение многочлена на рациональное число.

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.
        b (Rational): Рациональное число.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Polynom : Произведение многочлена и рационального числа.
    """
    if not (isinstance(a, Polynom) and isinstance(b, Rational)):
        raise ValueError("Invalid value")

    result_coefficients = [MUL_QQ_Q(coef, b) for coef in a.coefficients]
    return Polynom(result_coefficients)
