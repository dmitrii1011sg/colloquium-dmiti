from core.base.Natural import Natural
# Жуков Александр 5381

def NZER_N_B(n: Natural) -> bool:
    """
    Проверка натурального числа на неравенство нулю.

    Args:
        n (Natural): Натуральное число.

    Raises:
        ValueError: Параметры не соответствуют типам.

    Returns:
        bool: True, если число не равно нулю; False, если равно.
    """
    if not isinstance(n, Natural):
        raise ValueError("Invalid value")

    return not (n.length == 1 and n.digits[0] == 0)
