from core.base.Natural import Natural
from core.base.Polynom import Polynom
from core.base.Rational import Rational

# Жулин Максим 5381


def MUL_Pxk_P(a: Polynom, k: Natural) -> Polynom:
    """
    Умножение многочлена на x^k, k-натуральное или 0.

    Args:
        a (Polynom): Многочлен с рациональными коэффициентами.
        k (Natural): Натуральное число или 0.

    Raises:
        ValueError: Параметр не соответствует типу.

    Returns:
        Polynom : Многочлен, умноженный на x^k.
    """
    if not (isinstance(a, Polynom) and isinstance(k, Natural)):
        raise ValueError("Invalid value")

    k_int = int(str(k))
    zero = Rational.from_str("0")
    max_degree = a.degree + k_int
    result_coefficients = [zero] * (max_degree + 1)

    for i in range(a.degree + 1):
        result_coefficients[i + k_int] = a.coefficients[i]

    return Polynom(result_coefficients)
