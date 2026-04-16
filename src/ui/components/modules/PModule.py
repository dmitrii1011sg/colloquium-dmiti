import flet as ft


class PModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.controls = [
            ft.Text("Модуль: Многочлены (P)", size=28, weight=ft.FontWeight.BOLD),
            ft.Text("Коэффициенты, степени, производные.", color=ft.Colors.GREY_400),
        ]
