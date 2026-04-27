from core.base.Integer import Integer

# Чугунников Валерий 5382


def MUL_ZM_Z(n: Integer) -> Integer:
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

    if n.number.length == 1 and n.number.digits[0] == 0:
        return Integer(n.number, sign=0)

    new_sign = 1 if n.sign == 0 else 0
    return Integer(n.number, sign=new_sign)
