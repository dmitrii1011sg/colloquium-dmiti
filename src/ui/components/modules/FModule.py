# Горшков Дмитрий 5381

import flet as ft
from core.modules.FModule.REM_ASSOC_F_S import REM_ASSOC_F_S
from core.modules.FModule.REM_PRIOR_F_S import REM_PRIOR_F_S
from core.modules.FModule.SIMP_01_F_F import SIMP_01_F_F
from core.modules.FModule.TRANS_F_POST import TRANS_F_POST
from core.modules.FModule.TRANS_F_S import TRANS_F_S
from core.modules.FModule.TRANS_POST_S import TRANS_POST_S
from ui.components.forms.dynamic_func_form import DynamicFuncForm


class FModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {
            "TO-4: Постфиксная запись по дереву (TRANS_F_POST)": TRANS_F_POST,
            "TO-5: Скобочная запись по постфиксу (TRANS_POST_S)": TRANS_POST_S,
            "TO-6: Скобочная запись по дереву (TRANS_F_S)": TRANS_F_S,
            "TO-7: Скобки в цепочках умножения (REM_ASSOC_F_S)": REM_ASSOC_F_S,
            "TO-8: Скобки по приоритету операций (REM_PRIOR_F_S)": REM_PRIOR_F_S,
            "T-9: Упрощение нулей и единиц (SIMP_01_F_F)": SIMP_01_F_F,
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
