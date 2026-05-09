# Горшков Дмитрий 5381

import ast
import os
import re
import statistics
from collections import Counter

SOURCE_DIR = "src/core/modules"
EXTENSIONS = (".py",)


def get_author(content):
    """Ищет ФИО автора в комментариях (Фамилия Имя Отчество)."""
    match = re.search(r'(?:#|""").*?([А-Я][а-я]+\s+[А-Я][а-я]+(?:\s+[А-Я][а-я]+)?)', content)
    return match.group(1).strip() if match else "Неизвестный автор"


def get_project_map(root_dir):
    """
    Возвращает словарь: имя функции/класса -> относительный путь к модулю.
    Это позволяет определить «чужие» вызовы.
    """
    entity_map = {}
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(EXTENSIONS):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                with open(full_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        entity_map[node.name] = rel_path
    return entity_map


def count_physical_loc(content):
    """
    Считает physical LOC: непустые строки, не являющиеся комментарием.
    Игнорируются строки, которые после отбрасывания пробелов начинаются с '#'.
    """
    lines = content.splitlines()
    loc = 0
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            loc += 1
    return loc


def count_foreign_calls(tree, project_map, current_module_rel):
    """
    Обходит все вызовы в AST и подсчитывает те, которые ссылаются
    на сущности, определённые в других модулях.
    """
    foreign_calls = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr
            if name in project_map and project_map[name] != current_module_rel:
                foreign_calls += 1
    return foreign_calls


def analyze_file(path, project_map, root_dir):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    tree = ast.parse(content)

    author = get_author(content)
    current_module_rel = os.path.relpath(path, root_dir)

    loc = count_physical_loc(content)
    foreign_calls = count_foreign_calls(tree, project_map, current_module_rel)

    return {
        "file": current_module_rel,
        "loc": loc,
        "calls": foreign_calls,
        "author": author,
    }


def print_stats(data, label):
    """Выводит медиану, моду и среднее для набора чисел."""
    if not data:
        print("  Нет данных.")
        return
    mean_v = statistics.mean(data)
    median_v = statistics.median(data)
    counts = Counter(data)
    max_freq = max(counts.values())
    modes = [str(k) for k, v in counts.items() if v == max_freq]

    print(f"  Медиана:  {median_v:.2f}")
    print(f"  Мода:     {', '.join(modes)}")
    print(f"  Среднее:  {mean_v:.2f}")


def main():
    if not os.path.exists(SOURCE_DIR):
        print(f"Папка {SOURCE_DIR} не найдена")
        return

    root_dir = os.path.abspath(SOURCE_DIR)
    project_map = get_project_map(root_dir)
    results = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(EXTENSIONS) and not file.startswith("__"):
                res = analyze_file(os.path.join(root, file), project_map, root_dir)
                results.append(res)

    if not results:
        print("Нет файлов для анализа.")
        return

    results.sort(key=lambda x: x["loc"])
    n_80 = int(len(results) * 0.8)
    subset_80 = results[:n_80]

    print("=" * 100)
    print("СТАТИСТИКА МЕТРИК КОДА core/modules СКА")
    print("=" * 100)
    print(f"\nВсего модулей: {len(results)}")
    print(f"Модулей в выборке 80%: {len(subset_80)}")

    print("\n" + "-" * 100)
    print("МЕТРИКИ ОБЪЕМА КОДА (LOC) - для 80% модулей с наименьшим объемом")
    print("-" * 100)
    print_stats([r["loc"] for r in subset_80], "LOC")

    print("\n" + "-" * 100)
    print("МЕТРИКИ ВЫЗОВОВ ЧУЖИХ МОДУЛЕЙ (для всех модулей)")
    print("-" * 100)
    print_stats([r["calls"] for r in results], "Calls")

    print("\n" + "-" * 100)
    print("САМЫЕ КРУПНЫЕ МОДУЛИ (по вызовам чужих сущностей) — топ-5")
    print("-" * 100)
    top_calls = sorted(results, key=lambda x: x["calls"], reverse=True)[:5]
    print(f"{'№':<5} {'Модуль':<50} {'Вызовов':<10}")
    for i, r in enumerate(top_calls, 1):
        print(f"{i:<5} {r['file']:<50} {r['calls']:<10}")

    print("\n" + "-" * 100)
    print(f"{'№':<5} {'Модуль':<50} {'LOC':<10} {'Внеш.вызовы':<15}")
    print("-" * 100)
    for i, r in enumerate(results, 1):
        print(f"{i:<5} {r['file']:<50} {r['loc']:<10} {r['calls']:<15}")

    author_stats = {}
    for r in results:
        auth = r["author"]
        if auth not in author_stats:
            author_stats[auth] = {"count": 0, "loc": 0}
        author_stats[auth]["count"] += 1
        author_stats[auth]["loc"] += r["loc"]

    # sorted_authors = sorted(author_stats.items(), key=lambda x: x[1]["loc"], reverse=True)
    # print("\n" + "=" * 100)
    # print(f"{'№':<5} | {'Автор':<35} | {'Модулей':<8} | {'Всего строк (LOC)':<15}")
    # print("-" * 100)
    # for i, (name, stat) in enumerate(sorted_authors, 1):
    #     print(f"{i:<5} | {name:<35} | {stat['count']:<8} | {stat['loc']:<15}")


if __name__ == "__main__":
    main()
