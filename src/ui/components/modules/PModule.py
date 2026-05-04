import flet as ft
from core.modules.PModule.ADD_PP_P import ADD_PP_P
from core.modules.PModule.MUL_PQ_P import MUL_PQ_P
from core.modules.PModule.MUL_Pxk_P import MUL_Pxk_P
from core.modules.PModule.SUB_PP_P import SUB_PP_P
from ui.components.forms.dynamic_func_form import DynamicFuncForm

# Горшков Дмитрий 5381


class PModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {
            "P-1: Cложение многочленов (ADD_PP_P)": ADD_PP_P,
            "P-2: Вычитание многочленов (SUB_PP_P)": SUB_PP_P,
            "P-3: Умножение многочлена на рациональное число (MUL_PQ_P)": MUL_PQ_P,
            "P-4: Умножение многочлена на x^k (MUL_Pxk_P)": MUL_Pxk_P,
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
