import flet as ft


class NModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.controls = [
            ft.Text(
                "Модуль: Натуральные числа (N)", size=28, weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                "Здесь будет логика сложения, вычитания, умножения и т.д.",
                color=ft.Colors.GREY_400,
            ),
        ]
