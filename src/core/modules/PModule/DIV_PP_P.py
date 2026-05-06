from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.NModule.COM_NN_D import COM_NN_D
from core.modules.NModule.SUB_NN_N import SUB_NN_N
from core.modules.PModule.DEG_P_N import DEG_P_N
from core.modules.PModule.LED_P_Q import LED_P_Q
from core.modules.PModule.MUL_PP_P import MUL_PP_P
from core.modules.PModule.SUB_PP_P import SUB_PP_P
from core.modules.QModule.DIV_QQ_Q import DIV_QQ_Q

# Кацеба Андрей 5381


def DIV_PP_P(a: Polynom, b: Polynom) -> Polynom:
    """
    Частное от деления многочлена на многочлен.

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.
        b (Polynom): Многочлен с рациональными коэффициентами.

    Raises:
        ValueError: Параметр не соответствует типу.
        ZeroDivisionError: делитель равен нулю.

    Returns:
        Polynom :  Частное от деления многочлена на многочлен.
    """

    if not (isinstance(a, Polynom) and isinstance(b, Polynom)):
        raise ValueError("Invalid value")

    if (
        b.coefficients[-1].numer.number.digits[0] == 0
        and b.coefficients[-1].numer.number.length == 1
    ):
        raise ZeroDivisionError("invalid value")

    temp_pol = a

    fin_coeffs = []

    if COM_NN_D(DEG_P_N(temp_pol), DEG_P_N(b)) == 1:
        return Polynom.from_str("0")

    current_k = int(SUB_NN_N(DEG_P_N(a), DEG_P_N(b)))

    while COM_NN_D(DEG_P_N(temp_pol), DEG_P_N(b)) != 1:
        lead = LED_P_Q(temp_pol)
        if lead == Rational.from_str("0") or str(lead) in ("0", "0/1"):
            break

        lead = LED_P_Q(temp_pol)
        if lead == Rational.from_str("0") or str(lead) in ("0", "0/1"):
            break

        k = SUB_NN_N(DEG_P_N(temp_pol), DEG_P_N(b))
        c = DIV_QQ_Q(LED_P_Q(temp_pol), LED_P_Q(b))

        while current_k > int(k):
            fin_coeffs.append(Rational.from_str("0"))
            current_k -= 1

        fin_coeffs.append(c)
        current_k -= 1

        t = [Rational.from_str("0")] * int(k) + [c]
        temp_pol = SUB_PP_P(temp_pol, MUL_PP_P(b, Polynom(t)))

    while current_k >= 0:
        fin_coeffs.append(Rational.from_str("0"))
        current_k -= 1

    return Polynom(fin_coeffs[::-1])
