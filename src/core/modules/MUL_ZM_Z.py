from core.base.Integer import Integer

# Чугунников Валерий 5382


def MUL_ZM_Z(n : Integer) -> Integer:
    """
    Умножение целого числа на -1

    Args:
         n (Integer): Целое число

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Integer: Возвращает целое число, умноженное на -1
    """

    if not isinstance(n, Integer):
        raise ValueError("Invalid value")

    if n.sign == 1:
        return Integer(n.number, sign = 0)
    else:
        return Integer(n.number, sign = 1)