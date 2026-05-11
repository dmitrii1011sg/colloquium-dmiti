import inspect
import time
import asyncio
import multiprocessing

import flet as ft
from core.base.Integer import Integer
from core.base.Natural import Natural
from core.base.Polynom import Polynom
from core.base.Rational import Rational

# Горшков Дмитрий 5381

def worker_func(func, kwargs, result_queue):
    try:
        res = func(**kwargs)
        result_queue.put(("success", res))
    except Exception as e:
        result_queue.put(("error", str(e)))

class DynamicFuncForm(ft.Column):
    """
    Компонент динамической формы для вызова математических функций.

    Позволяет выбрать функцию из реестра, динамически построить поля ввода
    на основе сигнатуры функции, выполнить вычисление в отдельном потоке
    и отобразить результат с метриками.
    """

    def __init__(self, functions_registry: dict, module_name: str = "Модуль"):
        """
        Инициализирует форму.

        Args:
            functions_registry (dict): Словарь вида {"Название в UI": функция}
            module_name (str): Название модуля для заголовка.
        """
        super().__init__()
        self.expand = True
        self.spacing = 20
        self.functions_registry = functions_registry

        self.active_function = None
        self.input_fields = {}
        self.compute_process = None

        self.dropdown = ft.Dropdown(
            label="Выберите функцию",
            hint_text="Например: COM_NN_D",
            options=[ft.dropdown.Option(key) for key in self.functions_registry.keys()],
            on_select=self._on_function_select,
            border_color=ft.Colors.OUTLINE,
            border_radius=10,
            expand=True,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_500),
            menu_height=250,
        )

        self.title_text = ft.Text(
            f"{module_name}",
            size=14,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.PRIMARY,
        )

        self.placeholder = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        ft.Icons.FUNCTIONS_ROUNDED,
                        size=80,
                        color=ft.Colors.OUTLINE_VARIANT,
                    ),
                    ft.Text(
                        "Выберите функцию из списка выше,\nчтобы начать работу",
                        size=16,
                        color=ft.Colors.OUTLINE_VARIANT,
                        text_align=ft.TextAlign.CENTER,
                        weight=ft.FontWeight.W_300,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
            alignment=ft.Alignment.CENTER,
            visible=True,
        )

        self.inputs_container = ft.Column(spacing=12)

        self.loader = ft.ProgressBar(
            width=600,
            visible=False,
            color=ft.Colors.PRIMARY,
            bgcolor="SURFACE_CONTAINER_HIGHEST",
        )

        self.stop_button = ft.FilledButton(
            content=ft.Text("Стоп"),
            icon=ft.Icons.STOP_ROUNDED,
            on_click=self._on_stop_click,
            visible=False,
            bgcolor=ft.Colors.ERROR_CONTAINER,
            color=ft.Colors.ERROR,
            style=ft.ButtonStyle(
                mouse_cursor=ft.MouseCursor.CLICK,
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
        )

        self.calc_button = ft.FilledButton(
            content="Запустить вычисление",
            icon=ft.Icons.PLAY_ARROW_ROUNDED,
            on_click=self._on_calculate,
            visible=False,
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.ON_PRIMARY,
            style=ft.ButtonStyle(
                mouse_cursor=ft.MouseCursor.CLICK,
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )

        self.metric_refs = {}
        self.stats_row = ft.Row(
            visible=False,
            spacing=20,
            controls=[
                self._create_metric_item(ft.Icons.TIMER_OUTLINED, "Время", "0 ms", "time"),
                self._create_metric_item(ft.Icons.NUMBERS_ROUNDED, "Разрядность", "0", "size"),
                self._create_metric_item(ft.Icons.DATA_OBJECT_ROUNDED, "Тип", "-", "type"),
            ],
        )

        self.result_text = ft.Text(size=16, selectable=True)

        self.result_scroll_area = ft.Column(
            [self.result_text],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        self.result_card = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.INFO_OUTLINE,
                                color=ft.Colors.ON_SURFACE,
                                size=20,
                            ),
                            ft.Text("Результат вычисления:", weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.IconButton(
                                ft.Icons.COPY_ALL_ROUNDED,
                                icon_size=20,
                                on_click=self._copy_result,
                                style=ft.ButtonStyle(mouse_cursor=ft.MouseCursor.CLICK),
                            ),
                        ]
                    ),
                    self.result_scroll_area,
                ]
            ),
            padding=ft.Padding(top=15, bottom=15, left=20, right=20),
            border_radius=15,
            bgcolor="SURFACE_VARIANT",
            visible=False,
            expand=True,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
        )

        self.controls = [
            self.title_text,
            ft.Row([self.dropdown]),
            ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
            self.placeholder,
            self.inputs_container,
            self.loader,
            ft.Row([self.stop_button, self.calc_button], alignment=ft.MainAxisAlignment.END),
            self.result_card,
            self.stats_row,
        ]

    def _on_stop_click(self, _):
        if self.compute_process and self.compute_process.is_alive():
            self.compute_process.terminate()
            self.compute_process.join()
            
        self.loader.visible = False
        self.stop_button.visible = False
        self.calc_button.disabled = False
        self.result_text.value = "Процесс прерван пользователем"
        self.result_text.color = ft.Colors.ORANGE_700
        self.result_card.visible = True
        self.stats_row.visible = False
        self.update()

    def _create_metric_item(self, icon, label, value, key):
        """
        Создаёт виджет для отображения одной метрики.
        """
        value_text = ft.Text(value, size=12, weight=ft.FontWeight.W_500)
        self.metric_refs[key] = value_text

        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, size=16, color=ft.Colors.PRIMARY),
                    ft.Column(
                        [
                            ft.Text(
                                label,
                                size=10,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                                weight=ft.FontWeight.BOLD,
                            ),
                            value_text,
                        ],
                        spacing=0,
                    ),
                ]
            ),
        )

    def _update_metrics(self, exec_time, result):
        """
        Обновляет значения метрик после выполнения вычисления.
        """
        time_str = (
            f"{exec_time*1000:.3f} ms" if exec_time > 0.001 else f"{exec_time*1000000:.0f} μs"
        )

        size_val = "-"
        if hasattr(result, "length"):
            size_val = str(result.length)
        elif isinstance(result, Integer):
            size_val = str(result.number.length)
        elif isinstance(result, (int, str)):
            size_val = str(len(str(result)))

        self.metric_refs["time"].value = time_str
        self.metric_refs["size"].value = size_val
        self.metric_refs["type"].value = type(result).__name__

        self.stats_row.visible = True

    def _on_function_select(self, e):
        """
        Обработчик выбора функции из выпадающего списка.
        """
        func_name = self.dropdown.value
        if not func_name:
            self.placeholder.visible = True
            self.inputs_container.visible = False
            self.calc_button.visible = False
            self.update()
            return

        self.active_function = self.functions_registry[func_name]

        self.placeholder.visible = False
        self.inputs_container.visible = True
        self.inputs_container.controls.clear()
        self.input_fields.clear()
        self.title_text.value = func_name

        sig = inspect.signature(self.active_function)

        for param_name, param in sig.parameters.items():
            type_hint = param.annotation
            type_str = type_hint.__name__ if hasattr(type_hint, "__name__") else str(type_hint)

            display_type = type_str if type_str != "_empty" else "Any"

            tf = ft.TextField(
                label=f"Аргумент '{param_name}' (Тип: {display_type})",
                width=600,
                border_color=ft.Colors.OUTLINE,
            )
            self.inputs_container.controls.append(tf)
            self.input_fields[param_name] = tf

        self.calc_button.visible = True
        self.stop_button.visible = False
        self.update()

    def _parse_value(self, value: str, expected_type):
        """
        Умный парсинг введенной строки в нужный тип данных
        """
        if expected_type == Natural:
            return Natural.from_str(value)
        elif expected_type == Integer:
            return Integer.from_str(value)
        elif expected_type == Rational:
            return Rational.from_str(value)
        elif expected_type == Polynom:
            return Polynom.from_str(value)
        elif expected_type == int:
            return int(value)

        return value

    def _on_calculate(self, _):
        """
        Обработчик нажатия кнопки вычисления.
        """
        if not self.active_function:
            return

        for tf in self.input_fields.values():
            if not tf.value.strip():
                tf.error_text = "Поле пустое"
                self.update()
                return
            tf.error_text = None

        self.loader.visible = True
        self.calc_button.disabled = True
        self.stop_button.visible = True
        self.result_card.visible = False
        self.update()

        self.page.run_task(self._background_compute_task)  # type: ignore

    async def _background_compute_task(self):
        if not self.active_function: return

        sig = inspect.signature(self.active_function)
        kwargs = {}
        
        try:
            for param_name, tf in self.input_fields.items():
                expected_type = sig.parameters[param_name].annotation
                kwargs[param_name] = self._parse_value(tf.value.strip(), expected_type)

            result_queue = multiprocessing.Queue()
            start_time = time.perf_counter()

            self.compute_process = multiprocessing.Process(
                target=worker_func, 
                args=(self.active_function, kwargs, result_queue)
            )
            self.compute_process.start()

            while self.compute_process.is_alive():
                if result_queue.empty():
                    await asyncio.sleep(0.1)
                else:
                    break

            if not self.compute_process.is_alive() and result_queue.empty():
                return 

            status, result = result_queue.get()
            duration = time.perf_counter() - start_time

            if status == "success":
                self.result_text.value = str(result)
                self.result_text.color = ft.Colors.ON_SURFACE
                self._update_metrics(duration, result)
            else:
                raise Exception(result)

            self.result_card.visible = True

        except Exception as ex:
            self.result_text.value = f"Ошибка: {ex}"
            self.result_text.color = ft.Colors.ERROR
            self.result_card.visible = True
            self.stats_row.visible = False

        finally:
            self.loader.visible = False
            self.calc_button.disabled = False
            self.stop_button.visible = False
            self.page.update()

    async def _copy_result(self, _):
        await ft.Clipboard().set(self.result_text.value)
        self.page.show_dialog(ft.SnackBar("Text copied to clipboard"))
