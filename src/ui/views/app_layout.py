import flet as ft
from ui.components.modules.NModule import NModule
from ui.components.modules.PModule import PModule
from ui.components.modules.QModule import QModule
from ui.components.modules.ZModule import ZModule
from ui.components.sidebar import Sidebar


class AppLayout(ft.Row):
    def __init__(self, initial_index: int):
        super().__init__()
        self.expand = True
        self.spacing = 0

        self.sidebar = Sidebar(
            initial_index=initial_index,
            on_change_tab=self._handle_nav_change,
        )

        self.modules_map = {
            0: NModule(),
            1: ZModule(),
            2: QModule(),
            3: PModule(),
        }

        self.content_area = ft.Container(
            content=self.modules_map[initial_index],
            expand=True,
            padding=30,
            bgcolor="background",
        )

        self.controls = [
            self.sidebar,
            ft.VerticalDivider(width=1, color=ft.Colors.OUTLINE_VARIANT),
            self.content_area,
        ]

    def _handle_nav_change(self, e):
        selected_idx = e.control.selected_index
        self.content_area.content = self.modules_map.get(
            selected_idx, ft.Text("Раздел в разработке")
        )
        self.update()
