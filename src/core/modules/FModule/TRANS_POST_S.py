from core.base.Formula import PostfixFormula

# Помаскин Макар 5381


def TRANS_POST_S(a: str) -> str:
    """
    Построение полной скобочной записи формулы по постфиксной записи.

    Args:
        a (str): Постфиксная запись формулы с пробелами между элементами.

    Raises:
        ValueError: Параметр не является строкой или запись некорректна.

    Returns:
        str: Полная скобочная запись формулы.
    """
    if not isinstance(a, str):
        raise ValueError("Invalid value")

    return str(PostfixFormula.from_str(a).to_tree())
