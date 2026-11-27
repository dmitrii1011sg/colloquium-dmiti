from core.base.Formula import FormulaNode, FormulaTree, NodeType
from core.base.FormulaLexer import OPERATOR_PRECEDENCE, RIGHT_ASSOCIATIVE

# Жуков Александр 5381


def _needs_parentheses(operator: str, parent: str, right_child: bool) -> bool:
    """Проверить, как парсер свяжет соседние операции без скобок."""
    precedence = OPERATOR_PRECEDENCE[operator]
    parent_precedence = OPERATOR_PRECEDENCE[parent]
    if precedence != parent_precedence:
        return precedence < parent_precedence

    if parent in RIGHT_ASSOCIATIVE:
        return not right_child
    return right_child


def _render(node: FormulaNode, parent: str | None = None, right_child: bool = False) -> str:
    """Вывести узел с учётом его позиции относительно родительской операции."""
    if node.node_type == NodeType.VARIABLE:
        return str(node)
    if node.node_type == NodeType.FUNCTION:
        args = ", ".join(_render(child) for child in node.children)
        return f"{node.value}({args})"

    if node.node_type == NodeType.NUMBER:
        expression = str(node)
        # При повторном разборе дробь и отрицательное число становятся операциями.
        if "/" in expression:
            operator = "/"
        elif expression.startswith("-"):
            operator = "u-"
        else:
            return expression
    else:
        operator = str(node.value)
        if operator == "u-":
            expression = f"-{_render(node.children[0], operator, right_child=True)}"
        else:
            left = _render(node.children[0], operator)
            right = _render(node.children[1], operator, right_child=True)
            expression = f"{left} {operator} {right}"

    if parent is not None and _needs_parentheses(operator, parent, right_child):
        return f"({expression})"
    return expression


def REM_PRIOR_F_S(a: FormulaTree) -> str:
    """
    Вывести формулу со скобками, необходимыми для сохранения порядка операций.

    Args:
        a (FormulaTree): Дерево формулы.

    Raises:
        ValueError: Параметр не соответствует типу FormulaTree.

    Returns:
        str: Запись формулы с учётом приоритета и ассоциативности операций.
    """
    if not isinstance(a, FormulaTree):
        raise ValueError("Invalid value")

    return _render(a.root)
