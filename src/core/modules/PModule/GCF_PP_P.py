from core.base.Polynom import Polynom
from core.modules.PModule.DIV_PP_P import DIV_PP_P
from core.modules.PModule.MOD_PP_P import MOD_PP_P

# Помаскин Макар 5381


def GCF_PP_P(a: Polynom, b: Polynom) -> Polynom:
    """
    НОД многочленов

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.
        b (Polynom): Многочлен с рациональными коэффициентами.

    Raises:
        ValueError: Параметры не соответствуют типу.

    Returns:
        Polynom : Многочлен являющийся НОД многочленов.
    """
    if not (isinstance(a, Polynom) and isinstance(b, Polynom)):
        raise ValueError("Invalid value")

    if str(a) == "0" and str(b) == "0":
        return a

    if str(a) == "0":
        lead_coeff = Polynom.from_str(str(b.coefficients[-1]))
        return DIV_PP_P(b, lead_coeff)

    if str(b) == "0":
        lead_coeff = Polynom.from_str(str(a.coefficients[-1]))
        return DIV_PP_P(a, lead_coeff)

    while str(b) != "0":
        temp = MOD_PP_P(a, b)
        a = b
        b = temp
    lead_coeff = Polynom.from_str(str(a.coefficients[-1]))
    return DIV_PP_P(a, lead_coeff)
