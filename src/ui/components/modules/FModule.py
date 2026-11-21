# Горшков Дмитрий 5381

import flet as ft
from ui.components.forms.dynamic_func_form import DynamicFuncForm


class FModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {}

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
