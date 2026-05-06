from core.base.Integer import Integer
from core.base.Natural import Natural
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.PModule.DEG_P_N import DEG_P_N
from core.modules.QModule.MUL_QQ_Q import MUL_QQ_Q

# Помаскин Макар 5381


def DER_P_P(a: Polynom) -> Polynom:
    """
    Производная многочлена

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Polynom : Первая производная многочлена.
    """
    if not (isinstance(a, Polynom)):
        raise ValueError("Invalid value")

    lead = DEG_P_N(a)

    if str(lead) == "0":
        return Polynom([Rational.from_str("0")])

    a_coeffs = a.coefficients
    derivative = []
    for i in range(1, len(a_coeffs)):
        degree = Rational(Integer.from_int(i), Natural.from_int(1))
        derivative_coeff = MUL_QQ_Q(a_coeffs[i], degree)
        derivative.append(derivative_coeff)
    return Polynom(derivative)
