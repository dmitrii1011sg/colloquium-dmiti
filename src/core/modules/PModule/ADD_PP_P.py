from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.QModule.ADD_QQ_Q import ADD_QQ_Q

# Жулин Максим 5381


def ADD_PP_P(a: Polynom, b: Polynom) -> Polynom:
    """
    Сложение двух многочленов с рациональными коэффициентами.

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.
        b (Polynom): Многочлен с рациональными коэффициентами.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Polynom : Сумма многочленов.
    """
    if not (isinstance(a, Polynom) and isinstance(b, Polynom)):
        raise ValueError("Invalid value")

    zero = Rational.from_str("0")
    max_degree = max(a.degree, b.degree)
    result_coefficients = []

    for i in range(max_degree + 1):
        coef_a = a.coefficients[i] if i <= a.degree else zero
        coef_b = b.coefficients[i] if i <= b.degree else zero
        result_coefficients.append(ADD_QQ_Q(coef_a, coef_b))

    return Polynom(result_coefficients)
