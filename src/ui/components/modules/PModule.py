import flet as ft
from core.modules.PModule.DEG_P_N import DEG_P_N
from core.modules.PModule.LED_P_Q import LED_P_Q
from ui.components.forms.dynamic_func_form import DynamicFuncForm

# Горшков Дмитрий 5381


class PModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {
            "P-5: Старший коэффициент многочлена (LED_P_Q)": LED_P_Q,
            "P-6: Степень многочлена (DEG_P_N)": DEG_P_N,
        }

        self.controls = [
            ft.Text("Многочлены (P)", size=28, weight=ft.FontWeight.BOLD),
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
                            "TODO: сделать описание",
                            size=14,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                    spacing=5,
                )
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            DynamicFuncForm(functions_registry=self.registry, module_name="Модуль P"),
        ]
