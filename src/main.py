import flet as ft
from ui.views.app_layout import AppLayout


def main(page: ft.Page):
    page.title = "СКА"
    page.theme_mode = ft.ThemeMode.DARK

    page.window.min_width = 700
    page.window.min_height = 800
    page.window.max_width = 800
    page.window.max_height = 900

    page.window.width = 700
    page.window.height = 800

    page.padding = 0
    page.spacing = 0

    page.add(AppLayout(initial_index=0))


if __name__ == "__main__":
    ft.app(target=main)
