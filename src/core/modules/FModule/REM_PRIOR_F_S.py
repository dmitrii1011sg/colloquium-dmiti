from core.base.Formula import FormulaTree, needs_parentheses
from core.base.FormulaNotation import PostfixFormula
from core.modules.FModule.TRANS_F_S import TRANS_F_S
from core.modules.FModule.TRANS_POST_S import TRANS_POST_S

# Жуков Александр 5381


def REM_PRIOR_F_S(a: FormulaTree | PostfixFormula) -> str:
    """
    Вывести формулу со скобками, необходимыми для сохранения порядка операций.

    Args:
        a (FormulaTree | PostfixFormula): Дерево формулы или постфиксная запись.

    Raises:
        ValueError: Некорректный тип аргумента или постфиксная запись.

    Returns:
        str: Запись формулы с учётом приоритета и ассоциативности операций.
    """
    if isinstance(a, FormulaTree):
        text, tree = TRANS_F_S(a), a
    elif isinstance(a, PostfixFormula):
        text, tree = TRANS_POST_S(a), a.to_tree()
    else:
        raise ValueError("Invalid value")

    return tree.rewrite_parentheses(text, needs_parentheses)
