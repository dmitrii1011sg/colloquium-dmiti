from core.base.Formula import FormulaNode, FormulaTree, NodeType
from core.base.FormulaLexer import OPERATOR_PRECEDENCE

# Жуков Александр 5381


def _render(node: FormulaNode, parent: str | None = None, right_child: bool = False) -> str:
    """Сохранить скобки, отделяющие произведение от других операций."""
    if node.node_type == NodeType.VARIABLE:
        return str(node)
    if node.node_type == NodeType.NUMBER:
        value = str(node)
        if parent is None:
            return value

        # В инфиксной записи дробь разбирается как деление, а знак минус как оператор.
        precedence = OPERATOR_PRECEDENCE[parent]
        if "/" in value:
            division = OPERATOR_PRECEDENCE["/"]
            if precedence > division or (precedence == division and right_child):
                return f"({value})"
        elif value.startswith("-") and precedence > OPERATOR_PRECEDENCE["u-"]:
            return f"({value})"
        return value
    if node.node_type == NodeType.FUNCTION:
        args = ", ".join(_render(child) for child in node.children)
        return f"{node.value}({args})"

    operator = str(node.value)
    if operator == "u-":
        return f"(-{_render(node.children[0], operator, right_child=True)})"

    left = _render(node.children[0], operator)
    right = _render(node.children[1], operator, right_child=True)
    expression = f"{left} {operator} {right}"
    if operator == "*" and parent in (None, "*"):
        return expression
    return f"({expression})"


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

    return _render(a.root)
