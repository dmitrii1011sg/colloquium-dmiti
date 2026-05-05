from core.base.Natural import Natural
from core.base.Polynom import Polynom
from core.modules.PModule.ADD_PP_P import ADD_PP_P
from core.modules.PModule.MUL_PQ_P import MUL_PQ_P
from core.modules.PModule.MUL_Pxk_P import MUL_Pxk_P

# Кацеба Андрей 5381


def MUL_PP_P(a: Polynom, b: Polynom) -> Polynom:
    """
    Умножение многочлена на многочлен.

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.
        b (Polynom): Многочлен с рациональными коэффициентами.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Polynom : Произведение многочлена и многочлена числа.
    """

    if not (isinstance(a, Polynom) and isinstance(b, Polynom)):
        raise ValueError("Invalid value")

    bcoeffs = b.coefficients

    sumparts = []

    for i in range(len(bcoeffs)):
        sumparts.append(MUL_Pxk_P(MUL_PQ_P(a, bcoeffs[i]), Natural.from_int(i)))

    result = Polynom.from_str("0")
    for i in sumparts:
        result = ADD_PP_P(result, i)

    return result
