import flet as ft
from core.modules.ADD_1N_N import ADD_1N_N
from core.modules.ADD_NN_N import ADD_NN_N
from core.modules.COM_NN_D import COM_NN_D
from core.modules.DIV_NN_Dk import DIV_NN_Dk
from core.modules.MUL_ND_N import MUL_ND_N
from core.modules.MUL_Nk_N import MUL_Nk_N
from core.modules.MUL_NN_N import MUL_NN_N
from core.modules.NZER_N_B import NZER_N_B
from core.modules.SUB_NDN_N import SUB_NDN_N
from core.modules.SUB_NN_N import SUB_NN_N
from ui.components.forms.dynamic_func_form import DynamicFuncForm


class NModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {
            "N-1: Сравнение чисел (COM_NN_D)": COM_NN_D,
            "N-2: Проверка на ноль (NZER_N_B)": NZER_N_B,
            "N-3: Добавить 1 числу (ADD_1N_N)": ADD_1N_N,
            "N-4: Сложение чисел (ADD_NN_N)": ADD_NN_N,
            "N-5: Вычитание из большего меньшее (SUB_NN_N)": SUB_NN_N,
            "N-6: Умножение на цифру (MUL_ND_N)": MUL_ND_N,
            "N-7: Умножение на 10^k (MUL_Nk_N)": MUL_Nk_N,
            "N-8: Умножение натуральных чисел (MUL_NN_N)": MUL_NN_N,
            "N-9: Вычитание числа, умноженного на цифру (SUB_NDN_N)": SUB_NDN_N,
            "N-10: Вычисление первой цифры деления (DIV_NN_Dk)": DIV_NN_Dk,
        }

        self.controls = [
            ft.Text(
                "Модуль: Натуральные числа (N)", size=28, weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                "Выберите функцию из списка ниже для выполнения операции.",
                color=ft.Colors.GREY_400,
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            DynamicFuncForm(functions_registry=self.registry, module_name="Модуль N"),
        ]
