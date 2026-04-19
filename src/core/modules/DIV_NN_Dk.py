from core.base.Natural import Natural
from core.modules.COM_NN_D import COM_NN_D
#Лопатин Дмитрий 5381

def DIV_NN_Dk(a: Natural, b: Natural, k: int) -> Natural:
    """
    Деление натуральных чисел.

    Args:
        a (Natural): Делимое.
        b (Natural): Делитель.
        k (int): Номер цифры частного (начиная с 0).

    Raises:
        ValueError: Параметры не соответствуют типам или k < 0.
        ZeroDivisionError: Деление на ноль.

    Returns:
        Natural: k-я цифра частного от деления большего числа на меньшее.
    """
    if not isinstance(a, Natural) or not isinstance(b, Natural):
        raise ValueError("Invalid value")

    if k < 0:
        raise ValueError("Invalid value")
    
    if int(a) == 0:
        return Natural([0])

    if (int(b) == 0):
        raise ZeroDivisionError("Division by zero")
        
    if COM_NN_D(a, b) == 1:
        a, b = b, a

    remainder = 0
    res = []
    a_cpy = list(reversed(a.digits.copy()))

    for i in range(k + 1):
        a_cpy.append(0)

    divider = int(b)

    for digit in a_cpy:
        current = remainder * 10 + digit
        quotient = current // divider
        remainder = current % divider
        res.append(quotient)
    
    while len(res) > 1 and res[0] == 0:
        res.pop(0)

    if k >= len(res):
        return Natural([0])

    return Natural([res[k]], need_reverse=False)