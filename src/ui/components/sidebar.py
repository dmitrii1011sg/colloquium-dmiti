import flet as ft
from ui.components.dialogs.help_dialog import HelpDialog
from ui.components.dialogs.settings_dialog import SettingsDialog

# Горшков Дмитрий 5381


class Sidebar(ft.Container):
    def __init__(self, initial_index: int, on_change_tab):
        super().__init__()
        self.extended = True
        self.selected_index = initial_index
        self.on_change_tab = on_change_tab

        self.width = 200
        self.bgcolor = "surfacevariant"
        self.padding = ft.padding.all(10)
        self.animate = ft.Animation(250, ft.AnimationCurve.DECELERATE)

        self.nav_buttons = []
        self.text_elements = []
        self.row_elements = []

        self.content = self._build_ui()

    def _build_ui(self):
        self.menu_icon = ft.Icon(ft.Icons.MENU_OPEN)
        self.menu_text = ft.Text("Свернуть", visible=True)

        self.header_row = ft.Row(
            controls=[self.menu_icon, self.menu_text],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )

        header_btn = ft.TextButton(
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                color=ft.Colors.ON_SURFACE,
                padding=ft.padding.all(10),
                mouse_cursor=ft.MouseCursor.CLICK,
            ),
            content=ft.Container(
                content=self.header_row, alignment=ft.Alignment.CENTER_LEFT
            ),
            on_click=self.toggle_sidebar,
        )

        nav_items = [
            ("Натуральные (N)", ft.Icons.NUMBERS, 0),
            ("Целые (Z)", ft.Icons.EXPOSURE, 1),
            ("Рациональные (Q)", ft.Icons.PERCENT, 2),
            ("Многочлены (P)", ft.Icons.FUNCTIONS, 3),
            ("Калькулятор", ft.Icons.CALCULATE, 4),
        ]

        buttons_column = ft.Column(spacing=10)
        for text, icon, idx in nav_items:
            btn = self._create_nav_button(text, icon, idx)
            buttons_column.controls.append(btn)
            self.nav_buttons.append(btn)

        settings_btn = self._create_nav_button("Настройки", ft.Icons.SETTINGS, 98)
        help_btn = self._create_nav_button("Справка", ft.Icons.HELP_OUTLINE, 99)

        return ft.Column(
            controls=[
                header_btn,
                ft.Divider(height=10, thickness=1),
                buttons_column,
                ft.Container(expand=True),
                settings_btn,
                help_btn,
            ],
            tight=True,
        )

    def _create_nav_button(self, text, icon, index):
        is_selected = self.selected_index == index

        text_element = ft.Text(text, visible=self.extended)
        self.text_elements.append(text_element)

        row_element = ft.Row(
            controls=[ft.Icon(icon), text_element],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )
        self.row_elements.append(row_element)

        return ft.TextButton(
            tooltip=text,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                bgcolor=ft.Colors.PRIMARY if is_selected else None,
                color=ft.Colors.ON_PRIMARY if is_selected else ft.Colors.ON_SURFACE,
                padding=ft.padding.all(10),
                mouse_cursor=ft.MouseCursor.CLICK,
            ),
            content=ft.Container(
                content=row_element,
                alignment=ft.Alignment.CENTER_LEFT,
            ),
            on_click=lambda _: self._handle_click(index),
        )

    def _handle_click(self, index):
        if index == 98:
            self._show_dialog(SettingsDialog())
            return
        if index == 99:
            self._show_dialog(HelpDialog())
            return

        self.selected_index = index
        self._update_selection()

        if self.on_change_tab:

            class Event:
                def __init__(self, idx):
                    self.control = type("obj", (object,), {"selected_index": idx})

            self.on_change_tab(Event(index))

    def _show_dialog(self, dialog):
        self.page.show_dialog(dialog)
        dialog.open = True
        self.page.update()

    def _update_selection(self):
        for idx, btn in enumerate(self.nav_buttons):
            is_selected = self.selected_index == idx
            btn.style.bgcolor = ft.Colors.PRIMARY if is_selected else None
            btn.style.color = (
                ft.Colors.ON_PRIMARY if is_selected else ft.Colors.ON_SURFACE
            )
        self.update()

    def toggle_sidebar(self, e):
        self.extended = not self.extended
        self.width = 200 if self.extended else 70

        self.menu_icon.icon = ft.Icons.MENU_OPEN if self.extended else ft.Icons.MENU
        self.menu_text.visible = self.extended
        self.header_row.alignment = (
            ft.MainAxisAlignment.START if self.extended else ft.MainAxisAlignment.CENTER
        )
        self.header_row.spacing = 10 if self.extended else 0

        for txt, row in zip(self.text_elements, self.row_elements, strict=False):
            txt.visible = self.extended
            row.alignment = (
                ft.MainAxisAlignment.START
                if self.extended
                else ft.MainAxisAlignment.CENTER
            )
            row.spacing = 10 if self.extended else 0

        self.update()
