from core.base.Natural import Natural
##ЖуковАлександр5381

def ADD_1N_N(n: Natural) -> Natural:
    """
    Добавление единицы к натуральному числу.

    Args:
        n (Natural): Натуральное число.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        Natural: Натуральное число, равное n + 1.
    """
    if not isinstance(n, Natural):
        raise ValueError("Invalid value")

    result_digits = list(n.digits)
    carry = 1

    for i in range(len(result_digits)):
        total = result_digits[i] + carry
        result_digits[i] = total % 10
        carry = total // 10
        if carry == 0:
            break

    if carry > 0:
        result_digits.append(carry)

    return Natural(result_digits, need_reverse=False)
