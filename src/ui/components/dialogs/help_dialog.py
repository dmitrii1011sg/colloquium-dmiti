import flet as ft

# Горшков Дмитрий 5381

FUNCTIONS_DATA = {
    "N (Натуральные)": [
        {"id": "N-1", "name": "COM_NN_D", "desc": "Сравнение натуральных чисел"},
        {"id": "N-2", "name": "NZER_N_B", "desc": "Проверка на ноль"},
    ],
    "Z (Целые)": [
        {"id": "Z-1", "name": "ABS_Z_N", "desc": "Абсолютная величина числа"},
        {"id": "Z-2", "name": "POZ_Z_D", "desc": "Определение знака числа"},
    ],
    # TODO: остальные функции
}


class HelpDialog(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.title = ft.Row(
            [
                ft.Icon(ft.Icons.HELP_OUTLINE, color=ft.Colors.PRIMARY),
                ft.Text("Справочник"),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

        self.search_field = ft.TextField(
            label="Поиск",
            prefix_icon=ft.Icons.SEARCH,
            on_change=self._on_search_change,
            border_radius=5,
            text_size=14,
        )

        self.results_container = ft.Column(
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        self.content = ft.Container(
            content=ft.Column(
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
                        url="https://github.com/dmitrii1011sg/colloquium-dmiti",
                        style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
                    ),
                    self.search_field,
                    ft.Divider(),
                    self.results_container,
                ],
                tight=True,
                width=600,
            ),
            padding=10,
        )

        self.actions = [ft.TextButton("Закрыть", on_click=lambda _: self._close())]

        self._filter_functions("")

    def _create_table(self, title, functions):
        return ft.Column(
            [
                ft.Text(
                    title, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY
                ),
                ft.DataTable(
                    heading_row_color="surfacevariant",
                    border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=10,
                    columns=[
                        ft.DataColumn(label=ft.Text("ID")),
                        ft.DataColumn(label=ft.Text("Функция")),
                        ft.DataColumn(label=ft.Text("Описание")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f["id"])),
                                ft.DataCell(
                                    ft.Text(f["name"], weight=ft.FontWeight.W_500)
                                ),
                                ft.DataCell(ft.Text(f["desc"])),
                            ]
                        )
                        for f in functions
                    ],
                    width=float("inf"),
                ),
            ],
        )

    def _filter_functions(self, query):
        query = query.lower()
        self.results_container.controls.clear()

        for module, functions in FUNCTIONS_DATA.items():
            filtered = [
                f
                for f in functions
                if query in f["name"].lower()
                or query in f["desc"].lower()
                or query in f["id"].lower()
            ]

            if filtered:
                self.results_container.controls.append(
                    self._create_table(module, filtered)
                )

        if not self.results_container.controls:
            self.results_container.controls.append(
                ft.Container(
                    content=ft.Text(
                        "Ничего не найдено", italic=True, color=ft.Colors.GREY_500
                    ),
                    alignment=ft.Alignment.CENTER,
                    padding=20,
                )
            )

    def _on_search_change(self, e):
        self._filter_functions(e.control.value)
        self.update()

    def _close(self):
        self.open = False
        self.page.update()
