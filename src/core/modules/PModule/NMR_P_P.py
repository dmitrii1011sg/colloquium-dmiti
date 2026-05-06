from core.base.Polynom import Polynom
from core.modules.PModule.DEG_P_N import DEG_P_N
from core.modules.PModule.DER_P_P import DER_P_P
from core.modules.PModule.DIV_PP_P import DIV_PP_P
from core.modules.PModule.GCF_PP_P import GCF_PP_P

# Помаскин Макар 5381


def NMR_P_P(a: Polynom) -> Polynom:
    """
    Преобразование многочлена - кратные корни в простые

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Polynom : Многочлен с теми же корнями,
        но каждый корень встречается ровно один раз.
    """
    if not (isinstance(a, Polynom)):
        raise ValueError("Invalid value")

    if str(a) == "0":
        return 0

    derivative = DER_P_P(a)
    gcd = GCF_PP_P(a, derivative)

    if str(DEG_P_N(gcd)) == "0":
        return a

    return DIV_PP_P(a, gcd)
