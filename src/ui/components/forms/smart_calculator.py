from typing import Any, Literal, Union, cast, overload

import flet as ft
from core.base.Integer import Integer
from core.base.Natural import Natural
from core.base.Polynom import Polynom
from core.base.Rational import Rational
from core.modules.NModule.ADD_NN_N import ADD_NN_N
from core.modules.NModule.DIV_NN_N import DIV_NN_N
from core.modules.NModule.MOD_NN_N import MOD_NN_N
from core.modules.NModule.MUL_NN_N import MUL_NN_N
from core.modules.NModule.SUB_NN_N import SUB_NN_N
from core.modules.PModule.ADD_PP_P import ADD_PP_P
from core.modules.PModule.DIV_PP_P import DIV_PP_P
from core.modules.PModule.MOD_PP_P import MOD_PP_P
from core.modules.PModule.MUL_PP_P import MUL_PP_P
from core.modules.PModule.SUB_PP_P import SUB_PP_P
from core.modules.QModule.ADD_QQ_Q import ADD_QQ_Q
from core.modules.QModule.DIV_QQ_Q import DIV_QQ_Q
from core.modules.QModule.MUL_QQ_Q import MUL_QQ_Q
from core.modules.QModule.SUB_QQ_Q import SUB_QQ_Q
from core.modules.QModule.TRANS_Z_Q import TRANS_Z_Q
from core.modules.ZModule.ADD_ZZ_Z import ADD_ZZ_Z
from core.modules.ZModule.DIV_ZZ_Z import DIV_ZZ_Z
from core.modules.ZModule.MOD_ZZ_Z import MOD_ZZ_Z
from core.modules.ZModule.MUL_ZZ_Z import MUL_ZZ_Z
from core.modules.ZModule.SUB_ZZ_Z import SUB_ZZ_Z
from core.modules.ZModule.TRANS_N_Z import TRANS_N_Z

# Горшков Дмитрий 5381

CASObject = Union[Natural, Integer, Rational, Polynom]
CASTypeName = Literal["Natural", "Integer", "Rational", "Polynom"]

TYPE_PRIORITY = [
    Natural.__name__,
    Integer.__name__,
    Rational.__name__,
    Polynom.__name__,
]

ADD_FUNC = {
    Natural.__name__: ADD_NN_N,
    Integer.__name__: ADD_ZZ_Z,
    Rational.__name__: ADD_QQ_Q,
    Polynom.__name__: ADD_PP_P,
}

SUB_FUNC = {
    Natural.__name__: SUB_NN_N,
    Integer.__name__: SUB_ZZ_Z,
    Rational.__name__: SUB_QQ_Q,
    Polynom.__name__: SUB_PP_P,
}

MUL_FUNC = {
    Natural.__name__: MUL_NN_N,
    Integer.__name__: MUL_ZZ_Z,
    Rational.__name__: MUL_QQ_Q,
    Polynom.__name__: MUL_PP_P,
}

DIV_FUNC = {
    Natural.__name__: DIV_NN_N,
    Integer.__name__: DIV_ZZ_Z,
    Rational.__name__: DIV_QQ_Q,
    Polynom.__name__: DIV_PP_P,
}

MOD_FUNC = {
    Natural.__name__: MOD_NN_N,
    Integer.__name__: MOD_ZZ_Z,
    # Rational.__name__: MOD_QQ_Q,
    Polynom.__name__: MOD_PP_P,
}

OPERATIONS_MAP = {
    "+": ADD_FUNC,
    "-": SUB_FUNC,
    "×": MUL_FUNC,
    "÷": DIV_FUNC,
    "mod": MOD_FUNC,
}


class SmartCalculator(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.padding = ft.padding.all(24)
        self.bgcolor = "surfacevariant"
        self.border_radius = 20
        self.border = ft.border.all(1, "outlinevariant")
        self.animate = ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT)

        self.operand1: CASObject | None = None
        self.operator: str | None = None
        self.new_operand = True

        self.display = ft.Text(
            value="0",
            size=40,
            weight=ft.FontWeight.W_300,
            text_align=ft.TextAlign.RIGHT,
            color="onsurfacevariant",
            selectable=True,
            no_wrap=True,
        )

        self.info_icon = ft.Icon(ft.Icons.INFO_OUTLINE, size=14, color="outline", visible=False)
        self.info_text = ft.Text("", size=12, color="outline", italic=True)
        self.log_row = ft.Row(
            [self.info_icon, self.info_text],
            spacing=6,
            alignment=ft.MainAxisAlignment.START,
        )

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            self.display,
                            ft.Divider(height=1, color="outlinevariant"),
                            self.log_row,
                        ],
                        spacing=8,
                    ),
                    padding=ft.padding.only(bottom=16),
                ),
                self._build_keypad(),
            ],
            spacing=0,
            expand=True,
        )

    def _build_keypad(self) -> ft.Control:
        """Сборка резиновой клавиатуры из строк и колонок"""
        rows_data = [
            [
                ("C", "error", None, "C"),
                ("⌫", "surfacevariant", ft.Icons.BACKSPACE_OUTLINED, "BACK"),
                ("x", "tertiary", None, "x"),
                ("^", "tertiary", None, "^"),
            ],
            [
                ("(", "surfacevariant", None, "("),
                (")", "surfacevariant", None, ")"),
                ("/", "tertiary", None, "/"),
                ("mod", "tertiary", None, "mod"),
            ],
            [
                ("7", "surfacevariant", None, "7"),
                ("8", "surfacevariant", None, "8"),
                ("9", "surfacevariant", None, "9"),
                ("÷", "tertiary", None, "÷"),
            ],
            [
                ("4", "surfacevariant", None, "4"),
                ("5", "surfacevariant", None, "5"),
                ("6", "surfacevariant", None, "6"),
                ("×", "tertiary", ft.Icons.CLOSE, "×"),
            ],
            [
                ("1", "surfacevariant", None, "1"),
                ("2", "surfacevariant", None, "2"),
                ("3", "surfacevariant", None, "3"),
                ("−", "tertiary", ft.Icons.REMOVE, "-"),
            ],
            [
                ("±", "tertiary", ft.Icons.EXPOSURE, "±"),
                ("0", "surfacevariant", None, "0"),
                ("=", "primary", ft.CupertinoIcons.EQUAL, "="),
                ("+", "tertiary", ft.Icons.ADD, "+"),
            ],
        ]

        keypad = ft.Column(expand=True, spacing=6)

        for row in rows_data:
            btn_row = ft.Row(expand=True, spacing=6)
            for spec in row:
                btn_row.controls.append(self._create_btn(*spec))
            keypad.controls.append(btn_row)

        return keypad

    def _create_btn(self, tooltip: str, bg: str, icon: ft.IconData | None, data: str):
        on_bg = (
            ft.Colors.ON_PRIMARY
            if bg == "primary"
            else ft.Colors.ON_TERTIARY
            if bg == "tertiary"
            else ft.Colors.ON_SURFACE_VARIANT
            if bg == "surfacevariant"
            else ft.Colors.ON_ERROR
        )

        content = (
            ft.Icon(icon, size=20) if icon else ft.Text(data, size=18, weight=ft.FontWeight.W_500)
        )

        return ft.ElevatedButton(
            content=content,
            data=data,
            tooltip=tooltip,
            bgcolor=bg,
            color=on_bg,
            expand=True,
            aspect_ratio=1.0,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding.all(2),
                elevation=0,
                mouse_cursor=ft.MouseCursor.CLICK,
                animation_duration=200,
            ),
            on_click=self.on_button_click,
        )

    @overload
    def cast_to_type(self, obj: CASObject, target_type_name: Literal["Natural"]) -> Natural: ...
    @overload
    def cast_to_type(self, obj: CASObject, target_type_name: Literal["Integer"]) -> Integer: ...
    @overload
    def cast_to_type(self, obj: CASObject, target_type_name: Literal["Rational"]) -> Rational: ...
    @overload
    def cast_to_type(self, obj: CASObject, target_type_name: Literal["Polynom"]) -> Polynom: ...

    def cast_to_type(self, obj: CASObject, target_type_name: str) -> CASObject:
        current_type = type(obj).__name__
        if current_type == target_type_name:
            return obj

        if target_type_name == Integer.__name__ and isinstance(obj, Natural):
            return TRANS_N_Z(obj)

        if target_type_name == "Rational":
            if current_type == "Natural" and isinstance(obj, Natural):
                return TRANS_Z_Q(TRANS_N_Z(obj))
            if current_type == "Integer" and isinstance(obj, Integer):
                return TRANS_Z_Q(obj)

        return obj

    def to_common_type(self, a: CASObject, b: CASObject) -> tuple[CASObject, CASObject]:
        name_a = type(a).__name__
        name_b = type(b).__name__

        if name_a not in TYPE_PRIORITY or name_b not in TYPE_PRIORITY:
            return a, b

        idx_a = TYPE_PRIORITY.index(name_a)
        idx_b = TYPE_PRIORITY.index(name_b)

        target_name = TYPE_PRIORITY[max(idx_a, idx_b)]

        return (
            self.cast_to_type(a, cast(Any, target_name)),
            self.cast_to_type(b, cast(Any, target_name)),
        )

    def smart_add(self, a: CASObject, b: CASObject):
        a_c, b_c = self.to_common_type(a, b)
        return ADD_FUNC[type(a_c).__name__](a_c, b_c)

    def smart_calculate(self, a: CASObject, b: CASObject, op: str) -> CASObject:
        a_c, b_c = self.to_common_type(a, b)
        target_type = type(a_c).__name__

        func_dict = OPERATIONS_MAP.get(op, {})
        func = func_dict.get(target_type)

        if not func:
            raise NotImplementedError(f"Операция '{op}' для типа {target_type} пока не подключена.")
        return func(a_c, b_c)

    def parse_input(self, val: str) -> CASObject:
        val = val.strip()
        if not val:
            raise ValueError("Пустое поле ввода")

        if "x" in val or "^" in val:
            return Polynom.from_str(val)
        elif "/" in val:
            return Rational.from_str(val)
        elif val.startswith("-") or val.startswith("+"):
            return Integer.from_str(val)
        else:
            return Natural.from_str(val)

    def on_button_click(self, e):
        data = e.control.data
        try:
            if data in tuple("0123456789x^/(") or data == ")":
                if self.new_operand:
                    self.display.value = data if data != "/" else "0/"
                    self.new_operand = False
                    self.info_text.value = ""
                    self.info_icon.visible = False
                else:
                    if self.display.value == "0":
                        self.display.value = data
                    else:
                        self.display.value += data

            elif data == "±":
                if self.display.value.startswith("-"):
                    self.display.value = self.display.value[1:]
                elif self.display.value != "0":
                    self.display.value = "-" + self.display.value

            elif data == "BACK":
                if len(self.display.value) > 1:
                    self.display.value = self.display.value[:-1]
                else:
                    self.display.value = "0"
                    self.new_operand = True

            elif data in OPERATIONS_MAP.keys():
                self.operand1 = self.parse_input(self.display.value)
                self.operator = data
                self.new_operand = True

                op1_type = type(self.operand1).__name__
                self.info_text.value = f"[{op1_type}] {self.operand1} {data} ..."
                self.info_icon.visible = True

            elif data == "=":
                if self.operator and self.operand1 is not None:
                    operand2 = self.parse_input(self.display.value)
                    op1_type = type(self.operand1).__name__
                    op2_type = type(operand2).__name__
                    old_op1_str = str(self.operand1)

                    res = self.smart_calculate(self.operand1, operand2, self.operator)
                    res_type = type(res).__name__

                    self.display.value = str(res)

                    self.info_text.value = (
                        f"[{op1_type}] {old_op1_str} {self.operator}"
                        f"[{op2_type}] {operand2} ➔ [{res_type}] {res}"
                    )
                    self.info_icon.visible = True

                    self.operand1 = res
                    self.operator = None
                    self.new_operand = True

            elif data == "C":
                self.display.value = "0"
                self.operand1 = None
                self.operator = None
                self.new_operand = True
                self.info_text.value = "Очищено"
                self.info_icon.visible = True

            else:
                self.info_text.value = f"Кнопка '{data}' пока не поддерживается"
                self.info_icon.visible = True

        except Exception as ex:
            self.info_text.value = f"Ошибка: {str(ex)}"
            self.info_icon.visible = True
            self.new_operand = True

        self.update()
