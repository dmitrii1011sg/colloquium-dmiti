from core.base.FormulaNotation import PostfixFormula

# Помаскин Макар 5381


def TRANS_POST_S(a: PostfixFormula) -> str:
    """
    Построение полной скобочной записи формулы по постфиксной записи.

    Args:
        a (PostfixFormula): Формула в постфиксной записи.

    Raises:
        ValueError: Параметр не соответствует типу или запись некорректна.

    Returns:
        str: Полная скобочная запись формулы.
    """
    if not isinstance(a, PostfixFormula):
        raise ValueError("Invalid value")

    return str(a.to_tree())
