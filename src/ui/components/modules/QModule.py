import flet as ft
from core.modules.QModule.INT_Q_B import INT_Q_B
from core.modules.QModule.RED_Q_Q import RED_Q_Q
from core.modules.QModule.TRANS_Q_Z import TRANS_Q_Z
from core.modules.QModule.TRANS_Z_Q import TRANS_Z_Q
from ui.components.forms.dynamic_func_form import DynamicFuncForm

# Горшков Дмитрий 5381


class QModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {
            "Q-1: Получение несократимой обыкновенной дроби (RED_Q_Q)": RED_Q_Q,
            "Q-2: Проверка сокращенного дробного на целое (INT_Q_B)": INT_Q_B,
            "Q-3: Преобразование целого в дробное (TRANS_Z_Q)": TRANS_Z_Q,
            "Q-4: Преобразование сокращенного дробного в целое (TRANS_Q_Z)": TRANS_Q_Z,
        }

        self.controls = [
            ft.Text("Рациональные числа (Q)", size=28, weight=ft.FontWeight.BOLD),
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
                            "Дроби через косую черту (напр. -3/4, 7/1).",
                            size=14,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                    spacing=5,
                )
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            DynamicFuncForm(functions_registry=self.registry, module_name="Модуль Q"),
        ]
