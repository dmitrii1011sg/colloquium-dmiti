#!/usr/bin/env python3
import argparse
import importlib
import inspect
import pkgutil
from typing import Callable, Dict

# TODO: посмотреть откуда rich, возможно стоит добавить в requirements
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from core.base.Integer import Integer
from core.base.Natural import Natural
from core.base.Polynom import Polynom
from core.base.Rational import Rational

# Горшков Дмитрий 5381

MODULES_PACKAGES = [
    "core.modules.NModule",
    "core.modules.ZModule",
    "core.modules.QModule",
    "core.modules.PModule",
]

console = Console() if RICH_AVAILABLE else None


def discover_functions() -> Dict[str, Callable]:
    functions = {}
    for package_name in MODULES_PACKAGES:
        try:
            package = importlib.import_module(package_name)
            for _, module_name, _ in pkgutil.walk_packages(package.__path__):
                full_module_name = f"{package_name}.{module_name}"
                module = importlib.import_module(full_module_name)
                if hasattr(module, module_name):
                    func = getattr(module, module_name)
                    if callable(func):
                        functions[module_name] = func
        except ModuleNotFoundError:
            print(f"[WARN] Пакет {package_name} не найден, пропускаю.")
    return functions


AVAILABLE_FUNCTIONS = discover_functions()


def cast_argument(value_str: str, target_type):
    if target_type == inspect.Parameter.empty:
        return value_str
    if target_type in (int, str, float):
        return target_type(value_str)
    if target_type in (Natural, Integer, Rational, Polynom) and hasattr(target_type, "from_str"):
        return target_type.from_str(value_str)
    raise TypeError(f"Неизвестный тип для конвертации: {target_type}")


def execute_function(func_name: str, args_list: list):
    if func_name not in AVAILABLE_FUNCTIONS:
        raise ValueError(f"Функция '{func_name}' не зарегистрирована в AVAILABLE_FUNCTIONS.")

    func = AVAILABLE_FUNCTIONS[func_name]
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    if len(args_list) != len(params):
        raise ValueError(
            f"{func_name} ожидает {len(params)} аргументов, получено {len(args_list)}."
        )

    casted_args = []
    for arg_str, param in zip(args_list, params, strict=False):
        try:
            casted_val = cast_argument(arg_str, param.annotation)
            casted_args.append(casted_val)
        except Exception as e:
            raise ValueError(
                f"Ошибка обработки '{arg_str}' для параметра '{param.name}': {e}"
            ) from e

    return func(*casted_args)


def pretty_print_result(result, func_name: str = ""):
    header = f"Результат: {func_name}" if func_name else "Результат"
    if RICH_AVAILABLE:
        panel = Panel(
            Text(str(result), style="bold bright_white"),
            title=header,
            title_align="left",
            border_style="green",
            expand=False,
        )
        console.print(panel)  # type: ignore
    else:
        print(f"--- {header} ---")
        print(result)
        print("-" * (len(header) + 8))


def pretty_print_error(error_msg: str):
    if RICH_AVAILABLE:
        panel = Panel(
            Text(str(error_msg), style="bold red"),
            title="Ошибка",
            title_align="left",
            border_style="red",
            expand=False,
        )
        console.print(panel)  # type: ignore
    else:
        print(f"Ошибка: {error_msg}")


def repl_prompt():
    if RICH_AVAILABLE:
        return Text(">>> ", style="bold cyan")
    else:
        return ">>> "


def main():
    parser = argparse.ArgumentParser(description="СКА CLI")
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Запустить интерактивный режим (REPL)",
    )
    parser.add_argument("command", nargs="?", help="Имя функции (например, ADD_NN_N)")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Аргументы для функции")

    args = parser.parse_args()

    if args.interactive:
        run_repl()
    elif args.command:
        try:
            result = execute_function(args.command, args.args)
            pretty_print_result(result, args.command)
        except Exception as e:
            pretty_print_error(str(e))
    else:
        parser.print_help()


def run_repl():
    welcome = (
        "[bold magenta]СКА: Интерактивный режим[/bold magenta]\n"
        "Ввод: ИМЯ_ФУНКЦИИ арг1 арг2 ... (например: [bold]ADD_NN_N 123 456[/bold])\n"
        "Введите [bold red]exit[/bold red] для выхода."
    )
    if RICH_AVAILABLE:
        console.print(Panel(welcome, border_style="magenta", expand=False))  # type: ignore
    else:
        print("=" * 60)
        print("СКА: Интерактивный режим.")
        print("Формат ввода: ИМЯ_ФУНКЦИИ арг1 арг2 ... (например: ADD_NN_N 123 456)")
        print("Введите 'exit' для выхода.")
        print("=" * 60)

    while True:
        try:
            if RICH_AVAILABLE:
                cmd_line = console.input(repl_prompt()).strip().split()  # type: ignore
            else:
                cmd_line = input(">>> ").strip().split()

            if not cmd_line:
                continue

            func_name = cmd_line[0]
            if func_name.lower() == "exit":
                if RICH_AVAILABLE:
                    console.print("[yellow]Выход из СКА.[/yellow]")  # type: ignore
                else:
                    print("Выход из СКА.")
                break

            func_args = cmd_line[1:]
            result = execute_function(func_name, func_args)
            if RICH_AVAILABLE:
                panel = Panel(
                    Text(str(result), style="bold bright_green"),
                    title=f"Ответ: {func_name}",
                    title_align="left",
                    border_style="green",
                    expand=False,
                )
                console.print(panel)  # type: ignore
            else:
                print(f"Ответ: {result}")

        except Exception as e:
            if RICH_AVAILABLE:
                console.print(
                    Panel(  # type: ignore
                        Text(str(e), style="bold red"),
                        title="Ошибка",
                        border_style="red",
                        expand=False,
                    )
                )
            else:
                print(f"Ошибка: {e}")
        except EOFError:  # type: ignore
            if RICH_AVAILABLE:
                console.print("\n[yellow]Выход из СКА (EOF).[/yellow]")  # type: ignore
            else:
                print("\nВыход из СКА.")
            break


if __name__ == "__main__":
    main()
