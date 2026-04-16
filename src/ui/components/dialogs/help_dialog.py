import flet as ft


class HelpDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.title = ft.Text("Справочная информация")

        self.content = ft.Column(
            [
                ft.Text("О системе СКА", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Система Компьютерной Алгебры для работы с модулями N, Z, Q, P."
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Text("Репозиторий", weight=ft.FontWeight.BOLD),
                ft.TextButton(
                    "Открыть GitHub",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://github.com/",
                    style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Text("Модули", weight=ft.FontWeight.BOLD),
                ft.ExpansionTile(
                    title=ft.Text("Натуральные числа (N)"),
                    controls=[ft.Text("N1-N14: ...", size=14)],
                ),
                ft.ExpansionTile(
                    title=ft.Text("Целые числа (Z)"),
                    controls=[ft.Text("Z1-Z10: ...", size=14)],
                ),
                ft.ExpansionTile(
                    title=ft.Text("Рациональные числа (Q)"),
                    controls=[ft.Text("Q1-Q8: ...", size=14)],
                ),
                ft.ExpansionTile(
                    title=ft.Text("Многочлены (P)"),
                    controls=[ft.Text("P1-P13: ...", size=14)],
                ),
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
            height=400,
        )

        self.actions = [ft.TextButton("Понятно", on_click=lambda _: self._close())]

    def _close(self):
        self.open = False
        self.page.update()
