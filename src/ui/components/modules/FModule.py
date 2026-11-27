# Горшков Дмитрий 5381

import flet as ft
from core.modules.FModule.DER_F_F import DER_F_F
from core.modules.FModule.TRANS_F_POST import TRANS_F_POST
from core.modules.FModule.TRANS_F_PREF import TRANS_F_PREF
from core.modules.FModule.TRANS_F_S import TRANS_F_S
from core.modules.FModule.TRANS_POST_F import TRANS_POST_F
from core.modules.FModule.TRANS_POST_S import TRANS_POST_S
from ui.components.forms.dynamic_func_form import DynamicFuncForm


class FModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {
            "TO-1: Перевод формул в префиксную запись (TRANS_F_PREF)": TRANS_F_PREF,
            "TO-2: Построение дерева формулы по постфиксной записи (TRANS_POST_F)": TRANS_POST_F,
            "TO-3: Построение дерева формулы по постфиксной записи (DER_F_F)": DER_F_F,
            "TO-4: Постфиксная запись по дереву (TRANS_F_POST)": TRANS_F_POST,
            "TO-5: Скобочная запись по постфиксу (TRANS_POST_S)": TRANS_POST_S,
            "TO-6: Скобочная запись по дереву (TRANS_F_S)": TRANS_F_S,
        }

        self.controls = [
            ft.Text("Символьные формулы (F)", size=28, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Формат ввода данных:",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.PRIMARY,
                        ),
                        ft.Text(
                            "Инфикс: sin(x^2) + 3*x - log(2, y). "
                            "Постфикс/префикс: токены через пробел (напр. x 2 ^ sin).",
                            size=14,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                    spacing=5,
                )
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            DynamicFuncForm(functions_registry=self.registry, module_name="Модуль F"),
        ]
