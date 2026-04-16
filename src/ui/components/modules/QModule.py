import flet as ft


class QModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.controls = [
            ft.Text(
                "Модуль: Рациональные числа (Q)", size=28, weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                "Работа с дробями (числитель и знаменатель).", color=ft.Colors.GREY_400
            ),
        ]
