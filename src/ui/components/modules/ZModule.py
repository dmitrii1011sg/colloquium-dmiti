import flet as ft
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
from core.modules.ZModule.DIV_ZZ_Z import DIV_ZZ_Z
from core.modules.ZModule.MOD_ZZ_Z import MOD_ZZ_Z
from core.modules.ZModule.MUL_ZM_Z import MUL_ZM_Z
from core.modules.ZModule.MUL_ZZ_Z import MUL_ZZ_Z
from core.modules.ZModule.POZ_Z_D import POZ_Z_D
from core.modules.ZModule.SUB_ZZ_Z import SUB_ZZ_Z
from core.modules.ZModule.TRANS_N_Z import TRANS_N_Z
from core.modules.ZModule.TRANS_Z_N import TRANS_Z_N
from ui.components.forms.dynamic_func_form import DynamicFuncForm

# Горшков Дмитрий 5381


class ZModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {
            "Z-1: Вычисление абсолютной величины (ABS_Z_N)": ABS_Z_N,
            "Z-2: Определение положительности (POZ_Z_D)": POZ_Z_D,
            "Z-3: Умножение целого на (-1) (MUL_ZM_Z)": MUL_ZM_Z,
            "Z-4: Преобразование натурального в целое (TRANS_N_Z)": TRANS_N_Z,
            "Z-5: Преобразование целого неотриц. в натуральное (TRANS_Z_N)": TRANS_Z_N,
            "Z-7: Вычитание целых чисел (SUB_ZZ_Z)": SUB_ZZ_Z,
            "Z-8: Умножение целых чисел (MUL_ZZ_Z)": MUL_ZZ_Z,
            "Z-9: Частное от деления целого на целое (DIV_ZZ_Z)": DIV_ZZ_Z,
            "Z-10: Остаток от деления целого на целое (MOD_ZZ_Z)": MOD_ZZ_Z,
        }

        self.controls = [
            ft.Text("Целые числа (Z)", size=28, weight=ft.FontWeight.BOLD),
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
                            "Числа со знаком или без (напр. -42, 58).",
                            size=14,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                    spacing=5,
                ),
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            DynamicFuncForm(functions_registry=self.registry, module_name="Модуль Z"),
        ]
