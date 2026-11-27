from core.base.Formula import FormulaTree
from core.base.FormulaNotation import PostfixFormula
from core.modules.FModule.TRANS_F_S import TRANS_F_S
from core.modules.FModule.TRANS_POST_S import TRANS_POST_S

# Жуков Александр 5381


def _keep_parentheses(operator: str, parent: str | None, _right_child: bool) -> bool:
    """Сохранить скобки вокруг произведения на границе с другой операцией."""
    return operator != "*" or parent not in (None, "*")


def REM_ASSOC_F_S(a: FormulaTree | PostfixFormula) -> str:
    """
    Вывести формулу без скобок между соседними операциями умножения.

    Args:
        a (FormulaTree | PostfixFormula): Дерево формулы или постфиксная запись.

    Raises:
        ValueError: Некорректный тип аргумента или постфиксная запись.

    Returns:
        str: Скобочная запись формулы с раскрытыми цепочками множителей.
    """
    if isinstance(a, FormulaTree):
        text, tree = TRANS_F_S(a), a
    elif isinstance(a, PostfixFormula):
        text, tree = TRANS_POST_S(a), a.to_tree()
    else:
        raise ValueError("Invalid value")

    return tree.rewrite_parentheses(text, _keep_parentheses)
