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
        self.last_ans: CASObject | None = None

        self.history_list = ft.ListView(
            expand=True,
            spacing=8,
            height=140,
        )

        self.display = ft.TextField(
            value="0",
            width=600,
            text_size=32,
            text_align=ft.TextAlign.RIGHT,
            color=ft.Colors.ON_SURFACE,
            border=ft.InputBorder.NONE,
            cursor_color=ft.Colors.PRIMARY,
            content_padding=ft.padding.symmetric(vertical=15, horizontal=10),
            multiline=False,
            on_change=self.on_input_change,
            on_submit=lambda e: self.calculate_result(),
        )

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=self.history_list,
                                padding=10,
                                border_radius=12,
                                bgcolor="surfacevariant",
                            ),
                            ft.Container(
                                content=self.display,
                                border=ft.border.only(
                                    bottom=ft.border.BorderSide(2, ft.Colors.PRIMARY)
                                ),
                                margin=ft.Margin.only(top=8, bottom=16),
                                expand=True,
                            ),
                        ],
                        spacing=0,
                    ),
                ),
                self._build_keypad(),
            ],
            spacing=0,
            expand=True,
        )

    def log_action(self, text: str, is_error: bool = False, is_system: bool = False):
        if is_error:
            bg_color = ft.Colors.ERROR_CONTAINER
            text_color = ft.Colors.ON_ERROR_CONTAINER
            icon = ft.Icons.ERROR_OUTLINE
            align = ft.MainAxisAlignment.START
        elif is_system:
            bg_color = ft.Colors.TRANSPARENT
            text_color = ft.Colors.OUTLINE
            icon = ft.Icons.INFO_OUTLINE
            align = ft.MainAxisAlignment.START
        else:
            bg_color = ft.Colors.SECONDARY_CONTAINER
            text_color = ft.Colors.ON_SECONDARY_CONTAINER
            icon = ft.Icons.CALCULATE_OUTLINED
            align = ft.MainAxisAlignment.END

        log_item = ft.Row(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(icon, size=16, color=text_color),
                            ft.Text(
                                text,
                                size=14,
                                color=text_color,
                                selectable=True,
                                font_family="monospace",
                            ),
                        ],
                        alignment=align,
                        spacing=8,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    border_radius=12,
                    bgcolor=bg_color,
                )
            ],
            alignment=align,
        )

        if len(self.history_list.controls) > 50:
            self.history_list.controls.pop(-1)

        self.history_list.controls.insert(0, log_item)
        self.history_list.update()
        self.update()

    def _build_keypad(self) -> ft.Control:
        rows_data = [
            [
                ("C", "error", None, "C"),
                ("Ans", "tertiary", None, "Ans"),
                ("⌫", "surfacevariant", ft.Icons.BACKSPACE_OUTLINED, "BACK"),
                ("÷", "tertiary", None, "÷"),
            ],
            # [
            #     ("x", "surfacevariant", None, "x"),
            #     ("^", "surfacevariant", None, "^"),
            #     ("(", "surfacevariant", None, "("),
            #     (")", "surfacevariant", None, ")"),
            # ],
            [
                ("7", "surfacevariant", None, "7"),
                ("8", "surfacevariant", None, "8"),
                ("9", "surfacevariant", None, "9"),
                ("×", "tertiary", ft.Icons.CLOSE, "×"),
            ],
            [
                ("4", "surfacevariant", None, "4"),
                ("5", "surfacevariant", None, "5"),
                ("6", "surfacevariant", None, "6"),
                ("−", "tertiary", ft.Icons.REMOVE, "-"),
            ],
            [
                ("1", "surfacevariant", None, "1"),
                ("2", "surfacevariant", None, "2"),
                ("3", "surfacevariant", None, "3"),
                ("+", "tertiary", ft.Icons.ADD, "+"),
            ],
            [
                ("±", "surfacevariant", ft.Icons.EXPOSURE, "±"),
                ("0", "surfacevariant", None, "0"),
                ("/", "surfacevariant", None, "/"),
                ("=", "primary", ft.CupertinoIcons.EQUAL, "="),
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

    def on_input_change(self, e):
        self.new_operand = False

    def on_button_click(self, e):
        data = e.control.data
        try:
            if data in tuple("0123456789x^/(") or data == ")":
                if self.new_operand:
                    self.display.value = data if data != "/" else "0/"
                    self.new_operand = False
                else:
                    if self.display.value == "0" and data not in ("/", "x", "^"):
                        self.display.value = data
                    else:
                        self.display.value += data

            elif data == "Ans":
                if self.last_ans is not None:
                    ans_str = str(self.last_ans)
                    if type(self.last_ans).__name__ == "Polynom":
                        ans_str = f"({ans_str})"

                    if self.new_operand or self.display.value == "0":
                        self.display.value = ans_str
                        self.new_operand = False
                    else:
                        self.display.value += ans_str
                else:
                    self.log_action("Память Ans пуста", is_system=True)

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
                self.log_action(f"[{op1_type}] {self.operand1} {data} ...", is_system=True)

            elif data == "=":
                self.calculate_result()

            elif data == "C":
                self.display.value = "0"
                self.operand1 = None
                self.operator = None
                self.new_operand = True
                self.history_list.controls.clear()
                self.log_action("Память очищена", is_system=True)

        except Exception as ex:
            self.log_action(f"Ошибка: {str(ex)}", is_error=True)
            self.new_operand = True

        self.update()

    def calculate_result(self):
        if self.operator and self.operand1 is not None:
            try:
                operand2 = self.parse_input(self.display.value)
                # op1_type = type(self.operand1).__name__
                # op2_type = type(operand2).__name__
                old_op1_str = str(self.operand1)

                res = self.smart_calculate(self.operand1, operand2, self.operator)
                # res_type = type(res).__name__
                self.last_ans = res
                self.display.value = str(res)
                self.log_action(f"{old_op1_str} {self.operator} {operand2} = {res}")

                self.operand1 = res
                self.operator = None
                self.new_operand = True
            except Exception as ex:
                self.log_action(f"Ошибка вычисления: {str(ex)}", is_error=True)
                self.new_operand = True
        self.update()

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
