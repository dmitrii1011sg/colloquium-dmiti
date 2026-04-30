import flet as ft
from core.modules.ZModule.ABS_Z_N import ABS_Z_N
from core.modules.ZModule.MUL_ZM_Z import MUL_ZM_Z
from core.modules.ZModule.POZ_Z_D import POZ_Z_D
from core.modules.ZModule.TRANS_N_Z import TRANS_N_Z
from core.modules.ZModule.TRANS_Z_N import TRANS_Z_N
from ui.components.forms.dynamic_func_form import DynamicFuncForm


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
        }

        self.controls = [
            ft.Text("Целые числа (Z)", size=28, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Выберите функцию из списка ниже для выполнения операции.",
                color=ft.Colors.GREY_400,
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            DynamicFuncForm(functions_registry=self.registry, module_name="Модуль Z"),
        ]
