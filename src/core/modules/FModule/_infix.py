from core.base.Formula import FormulaNode, NodeType
from core.base.FormulaLexer import OPERATOR_PRECEDENCE, RIGHT_ASSOCIATIVE


def _needs_parentheses(operator: str, parent: str, right_child: bool) -> bool:
    """Проверить, как парсер свяжет соседние операции без скобок."""
    precedence = OPERATOR_PRECEDENCE[operator]
    parent_precedence = OPERATOR_PRECEDENCE[parent]
    if precedence != parent_precedence:
        return precedence < parent_precedence

    if parent in RIGHT_ASSOCIATIVE:
        return not right_child
    return right_child


def render_infix(root: FormulaNode, *, by_precedence: bool) -> str:
    """Вывести поддерево с учётом приоритетов или только ассоциативности умножения."""

    def render(node: FormulaNode, parent: str | None = None, right_child: bool = False) -> str:
        """Вывести узел с учётом его позиции относительно родительской операции."""
        if node.node_type == NodeType.NUMBER:
            value = str(node)
            if parent is None:
                return value

            # При повторном разборе дробь и отрицательное число становятся операциями.
            if "/" in value:
                operator = "/"
            elif value.startswith("-"):
                operator = "u-"
            else:
                return value
            return f"({value})" if _needs_parentheses(operator, parent, right_child) else value

        if node.node_type == NodeType.VARIABLE:
            return str(node.value)
        if node.node_type == NodeType.FUNCTION:
            args = ", ".join(render(child) for child in node.children)
            return f"{node.value}({args})"

        operator = str(node.value)
        if operator == "u-":
            operand = render(node.children[0], operator, right_child=True)
            expression = f"-{operand}"
        else:
            left = render(node.children[0], operator)
            right = render(node.children[1], operator, right_child=True)
            expression = f"{left} {operator} {right}"

        if by_precedence:
            wrap = parent is not None and _needs_parentheses(operator, parent, right_child)
        else:
            wrap = operator != "*" or parent not in (None, "*")
        return f"({expression})" if wrap else expression

    return render(root)
