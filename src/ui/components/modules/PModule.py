import flet as ft
from core.modules.PModule.ADD_PP_P import ADD_PP_P
from core.modules.PModule.DEG_P_N import DEG_P_N
from core.modules.PModule.DER_P_P import DER_P_P
from core.modules.PModule.DIV_PP_P import DIV_PP_P
from core.modules.PModule.GCF_PP_P import GCF_PP_P
from core.modules.PModule.LED_P_Q import LED_P_Q
from core.modules.PModule.MOD_PP_P import MOD_PP_P
from core.modules.PModule.MUL_PP_P import MUL_PP_P
from core.modules.PModule.MUL_PQ_P import MUL_PQ_P
from core.modules.PModule.MUL_Pxk_P import MUL_Pxk_P
from core.modules.PModule.NMR_P_P import NMR_P_P
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
            "P-5: Старший коэффициент многочлена (LED_P_Q)": LED_P_Q,
            "P-6: Степень многочлена (DEG_P_N)": DEG_P_N,
            "P-8: Умножение многочленов (MUL_PP_P)": MUL_PP_P,
            "P-9: Частное от деления многочленов (DIV_PP_P)": DIV_PP_P,
            "P-10: Остаток от деления многочленов (MOD_PP_P)": MOD_PP_P,
            "P-11: НОД многочленов (GCF_PP_P)": GCF_PP_P,
            "P-12: Производная многочлена (DER_P_P)": DER_P_P,
            "P-13: Преобразование многочлена к простым корням (NMR_P_P)": NMR_P_P,
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
