import flet as ft


class ZModule(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.controls = [
            ft.Text("Модуль: Целые числа (Z)", size=28, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Логика для работы с отрицательными числами и модулями.",
                color=ft.Colors.GREY_400,
            ),
        ]
