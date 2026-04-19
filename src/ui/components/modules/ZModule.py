import flet as ft
from ui.components.forms.dynamic_func_form import DynamicFuncForm


class ZModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.registry = {}

        self.controls = [
            ft.Text("Модуль: Целые числа (Z)", size=28, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Выберите функцию из списка ниже для выполнения операции.",
                color=ft.Colors.GREY_400,
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            DynamicFuncForm(functions_registry=self.registry, module_name="Модуль Z"),
        ]
