import flet as ft
from core.modules.QModule.ADD_QQ_Q import ADD_QQ_Q
from core.modules.QModule.DIV_QQ_Q import DIV_QQ_Q
from core.modules.QModule.INT_Q_B import INT_Q_B
from core.modules.QModule.MUL_QQ_Q import MUL_QQ_Q
from core.modules.QModule.RED_Q_Q import RED_Q_Q
from core.modules.QModule.SUB_QQ_Q import SUB_QQ_Q
from core.modules.QModule.TRANS_Q_Z import TRANS_Q_Z
from core.modules.QModule.TRANS_Z_Q import TRANS_Z_Q
from ui.components.forms.dynamic_func_form import DynamicFuncForm


class QModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {
            "Q-1: Получение несократимой обыкновенной дроби (RED_Q_Q)": RED_Q_Q,
            "Q-2: Проверка сокращенного дробного на целое (INT_Q_B)": INT_Q_B,
            "Q-3: Преобразование целого в дробное (TRANS_Z_Q)": TRANS_Z_Q,
            "Q-4: Преобразование сокращенного дробного в целое (TRANS_Q_Z)": TRANS_Q_Z,
            "Q-5: Сложение дробей (ADD_QQ_Q)": ADD_QQ_Q,
            "Q-6: Вычитание дробей (SUB_QQ_Q)": SUB_QQ_Q,
            "Q-7: Умножение дробей (MUL_QQ_Q)": MUL_QQ_Q,
            "Q-8: Деление дробей (DIV_QQ_Q)": DIV_QQ_Q,
        }

        self.controls = [
            ft.Text("Рациональные числа (Q)", size=28, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Выберите функцию из списка ниже для выполнения операции.",
                color=ft.Colors.GREY_400,
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            DynamicFuncForm(functions_registry=self.registry, module_name="Модуль Q"),
        ]
