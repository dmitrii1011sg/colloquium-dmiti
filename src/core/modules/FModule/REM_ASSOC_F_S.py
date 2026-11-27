from core.base.Formula import FormulaTree
from core.modules.FModule.TRANS_F_S import TRANS_F_S

# Жуков Александр 5381


def _keep_parentheses(operator: str, parent: str | None, _right_child: bool) -> bool:
    """Сохранить скобки вокруг произведения на границе с другой операцией."""
    return operator != "*" or parent not in (None, "*")


def REM_ASSOC_F_S(a: FormulaTree) -> str:
    """
    Вывести формулу без скобок между соседними операциями умножения.

    Args:
        a (FormulaTree): Дерево формулы.

    Raises:
        ValueError: Параметр не соответствует типу FormulaTree.

    Returns:
        str: Скобочная запись формулы с раскрытыми цепочками множителей.
    """
    if not isinstance(a, FormulaTree):
        raise ValueError("Invalid value")

    return a.rewrite_parentheses(TRANS_F_S(a), _keep_parentheses)
