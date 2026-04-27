from core.base.Integer import Integer
from core.base.Natural import Natural

# Чугунников Валерий 5382


def TRANS_N_Z(n: Natural) -> Integer:
    """
    Преобразование натурального в целое

    Args:
         n (Natural): Натуральное число

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Integer: Возвращает целое число
    """

    if not isinstance(n, Natural):
        raise ValueError("Invalid value")

    return Integer(n, sign=0)
