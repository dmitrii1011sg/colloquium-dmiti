import flet as ft


class SettingsDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.title = ft.Text("Настройки темы")

        self.colors = [
            ("Синий", ft.Colors.BLUE),
            ("Зеленый", ft.Colors.GREEN),
            ("Красный", ft.Colors.RED),
            ("Фиолетовый", ft.Colors.PURPLE),
            ("Оранжевый", ft.Colors.ORANGE),
        ]

        self.content = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.CIRCLE,
                    icon_color=color_val,
                    icon_size=40,
                    tooltip=color_name,
                    on_click=lambda _, cv=color_val: self._change_theme(cv),
                    mouse_cursor=ft.MouseCursor.CLICK,
                )
                for color_name, color_val in self.colors
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            tight=True,
        )

        self.actions = [ft.TextButton("Закрыть", on_click=lambda _: self._close())]

    def _change_theme(self, color_seed):
        self.page.theme = ft.Theme(color_scheme_seed=color_seed)
        self.page.update()

    def _close(self):
        self.open = False
        self.page.update()
