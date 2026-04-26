from core.base.Integer import Integer
from core.base.Natural import Natural

# Чугунников Валерий 5382


def TRANS_Z_N(n : Integer) -> Natural:
    """
    Преобразование целого неотрицательного в натуральное

    Args:
         n (Integer): Целое неотрицательное число

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Natural: Возвращает натуральное число
    """

    if not isinstance(n, Integer):
        raise ValueError("Invalid value")
    if n.sign == 1:
        raise ValueError("Invalid value")

    return n.number