import flet as ft

# Горшков Дмитрий 5381
# Жулин Максим 5381

FUNCTIONS_DATA = {
    "N (Натуральное числа с 0)": [
        {
            "id": "N-1",
            "name": "COM_NN_D",
            "desc": "Сравнение натуральных",
            "args": ("a: Натуральное (с 0), b: Натуральное (с 0)"),
        },
        {
            "id": "N-2",
            "name": "NZER_N_B",
            "desc": "Проверка на ноль",
            "args": "n: Натуральное (с 0)",
        },
        {
            "id": "N-3",
            "name": "ADD_1N_N",
            "desc": "Прибавить единицу",
            "args": "n: Натуральное (с 0)",
        },
        {
            "id": "N-4",
            "name": "ADD_NN_N",
            "desc": "Сложение натуральных",
            "args": ("a: Натуральное (с 0), b: Натуральное (с 0)"),
        },
        {
            "id": "N-5",
            "name": "SUB_NN_N",
            "desc": "Вычитание (первое не меньше)",
            "args": ("a: Натуральное (с 0), b: Натуральное (с 0)"),
        },
        {
            "id": "N-6",
            "name": "MUL_ND_N",
            "desc": "Умножение на цифру",
            "args": "n: Натуральное (с 0), d: Цифра",
        },
        {
            "id": "N-7",
            "name": "MUL_Nk_N",
            "desc": "Умножение на 10^k",
            "args": ("n: Натуральное (с 0), k: Натуральное (с 0)"),
        },
        {
            "id": "N-8",
            "name": "MUL_NN_N",
            "desc": "Умножение натуральных",
            "args": ("a: Натуральное (с 0), b: Натуральное (с 0)"),
        },
        {
            "id": "N-9",
            "name": "SUB_NDN_N",
            "desc": ("Вычитание b * d из a без отрицательного результата"),
            "args": ("a: Натуральное (с 0), b: Натуральное (с 0), n: Цифра"),
        },
        {
            "id": "N-10",
            "name": "DIV_NN_Dk",
            "desc": ("Определение первой цифры частного и степени 10^k"),
            "args": ("a: Натуральное (с 0), b: Натуральное (с 0)"),
        },
        {
            "id": "N-11",
            "name": "DIV_NN_N",
            "desc": "Неполное частное",
            "args": ("a: Натуральное (с 0), b: Натуральное (не 0)"),
        },
        {
            "id": "N-12",
            "name": "MOD_NN_N",
            "desc": "Остаток от деления",
            "args": ("a: Натуральное (с 0), b: Натуральное (не 0)"),
        },
        {
            "id": "N-13",
            "name": "GCF_NN_N",
            "desc": "Наибольший общий делитель",
            "args": ("a: Натуральное (не 0), b: Натуральное (не 0)"),
        },
        {
            "id": "N-14",
            "name": "LCM_NN_N",
            "desc": "Наименьшее общее кратное",
            "args": ("a: Натуральное (не 0), b: Натуральное (не 0)"),
        },
    ],
    "Z (Целые числа)": [
        {
            "id": "Z-1",
            "name": "ABS_Z_N",
            "desc": "Модуль числа",
            "args": "n: Целое",
        },
        {
            "id": "Z-2",
            "name": "POZ_Z_D",
            "desc": "Определение знака",
            "args": "n: Целое",
        },
        {
            "id": "Z-3",
            "name": "MUL_ZM_Z",
            "desc": "Умножение на минус один",
            "args": "n: Целое",
        },
        {
            "id": "Z-4",
            "name": "TRANS_N_Z",
            "desc": "Преобразование в целое",
            "args": "n: Натуральное (с 0)",
        },
        {
            "id": "Z-5",
            "name": "TRANS_Z_N",
            "desc": "Преобразование в натуральное",
            "args": "n: Целое",
        },
        {
            "id": "Z-6",
            "name": "ADD_ZZ_Z",
            "desc": "Сложение целых",
            "args": ("a: Целое, b: Целое"),
        },
        {
            "id": "Z-7",
            "name": "SUB_ZZ_Z",
            "desc": "Вычитание целых",
            "args": ("a: Целое, b: Целое"),
        },
        {
            "id": "Z-8",
            "name": "MUL_ZZ_Z",
            "desc": "Умножение целых",
            "args": ("a: Целое, b: Целое"),
        },
        {
            "id": "Z-9",
            "name": "DIV_ZZ_Z",
            "desc": "Частное от деления",
            "args": ("a: Целое, b: Целое (не 0)"),
        },
        {
            "id": "Z-10",
            "name": "MOD_ZZ_Z",
            "desc": "Остаток от деления",
            "args": ("a: Целое, b: Целое (не 0)"),
        },
    ],
    "Q (Рациональные числа)": [
        {
            "id": "Q-1",
            "name": "RED_Q_Q",
            "desc": "Сокращение дроби",
            "args": "q: Рациональное",
        },
        {
            "id": "Q-2",
            "name": "INT_Q_B",
            "desc": "Проверка на целое",
            "args": "q: Рациональное",
        },
        {
            "id": "Q-3",
            "name": "TRANS_Z_Q",
            "desc": "Преобразование в дробь",
            "args": "z: Целое",
        },
        {
            "id": "Q-4",
            "name": "TRANS_Q_Z",
            "desc": ("Преобразование сокращенной дроби в целое"),
            "args": "q: Рациональное",
        },
        {
            "id": "Q-5",
            "name": "ADD_QQ_Q",
            "desc": "Сложение дробей",
            "args": ("a: Рациональное, b: Рациональное"),
        },
        {
            "id": "Q-6",
            "name": "SUB_QQ_Q",
            "desc": "Вычитание дробей",
            "args": ("a: Рациональное, b: Рациональное"),
        },
        {
            "id": "Q-7",
            "name": "MUL_QQ_Q",
            "desc": "Умножение дробей",
            "args": ("a: Рациональное, b: Рациональное"),
        },
        {
            "id": "Q-8",
            "name": "DIV_QQ_Q",
            "desc": "Деление дробей",
            "args": ("a: Рациональное, b: Рациональное (не 0)"),
        },
    ],
    "P (Многочлены)": [
        {
            "id": "P-1",
            "name": "ADD_PP_P",
            "desc": "Сложение многочленов",
            "args": ("a: Многочлен, b: Многочлен"),
        },
        {
            "id": "P-2",
            "name": "SUB_PP_P",
            "desc": "Вычитание многочленов",
            "args": ("a: Многочлен, b: Многочлен"),
        },
        {
            "id": "P-3",
            "name": "MUL_PQ_P",
            "desc": "Умножение на число",
            "args": ("p: Многочлен, q: Рациональное"),
        },
        {
            "id": "P-4",
            "name": "MUL_Pxk_P",
            "desc": "Умножение на степень x",
            "args": ("p: Многочлен, k: Натуральное (с 0)"),
        },
        {
            "id": "P-5",
            "name": "LED_P_Q",
            "desc": "Старший коэффициент",
            "args": "p: Многочлен",
        },
        {
            "id": "P-6",
            "name": "DEG_P_N",
            "desc": "Степень многочлена",
            "args": "p: Многочлен",
        },
        {
            "id": "P-7",
            "name": "FAC_P_Q",
            "desc": "Вынести общий множитель",
            "args": "p: Многочлен",
        },
        {
            "id": "P-8",
            "name": "MUL_PP_P",
            "desc": "Умножение многочленов",
            "args": ("a: Многочлен, b: Многочлен"),
        },
        {
            "id": "P-9",
            "name": "DIV_PP_P",
            "desc": "Частное при делении",
            "args": ("a: Многочлен, b: Многочлен(не 0)"),
        },
        {
            "id": "P-10",
            "name": "MOD_PP_P",
            "desc": "Остаток при делении",
            "args": ("a: Многочлен, b: Многочлен(не 0)"),
        },
        {
            "id": "P-11",
            "name": "GCF_PP_P",
            "desc": "Наибольший общий делитель",
            "args": ("a: Многочлен(не 0), b: Многочлен(не 0)"),
        },
        {
            "id": "P-12",
            "name": "DER_P_P",
            "desc": "Производная многочлена",
            "args": "p: Многочлен",
        },
        {
            "id": "P-13",
            "name": "NMR_P_P",
            "desc": "Упростить кратные корни",
            "args": "p: Многочлен",
        },
    ],
    "F (Символьные формулы)": [],
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
                    ft.Text("Система Компьютерной Алгебры для работы с модулями N, Z, Q, P."),
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
        id_width = 35
        name_width = 90
        args_width = 160
        desc_width = 190

        def cell(value, width, bold=False, monospace=False, is_args=False):
            return ft.DataCell(
                ft.Container(
                    content=ft.Text(
                        value,
                        size=11,
                        weight=ft.FontWeight.W_500 if bold else ft.FontWeight.NORMAL,
                        font_family="Roboto Mono" if monospace else None,
                    ),
                    width=width,
                    padding=ft.padding.symmetric(vertical=10),
                    alignment=ft.Alignment.TOP_LEFT,
                )
            )

        data_table = ft.DataTable(
            data_row_min_height=40,
            data_row_max_height=float("inf"),
            heading_row_height=40,
            column_spacing=15,
            divider_thickness=0.5,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
            columns=[
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text("ID", size=12, weight=ft.FontWeight.BOLD), width=id_width
                    )
                ),
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text("Функция", size=12, weight=ft.FontWeight.BOLD), width=name_width
                    )
                ),
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text("Аргументы", size=12, weight=ft.FontWeight.BOLD), width=args_width
                    )
                ),
                ft.DataColumn(
                    label=ft.Container(
                        ft.Text("Описание", size=12, weight=ft.FontWeight.BOLD), width=desc_width
                    )
                ),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        cell(f["id"], id_width, monospace=True),
                        cell(f["name"], name_width, bold=True),
                        cell(f["args"].replace(", ", "\n"), args_width, is_args=True),
                        cell(f["desc"], desc_width),
                    ],
                )
                for f in functions
            ],
        )

        return ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        title, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY
                    ),
                    margin=ft.margin.only(top=10, bottom=5),
                ),
                ft.Row(
                    [data_table],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            spacing=0,
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
                self.results_container.controls.append(self._create_table(module, filtered))

        if not self.results_container.controls:
            self.results_container.controls.append(
                ft.Container(
                    content=ft.Text("Ничего не найдено", italic=True, color=ft.Colors.GREY_500),
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
