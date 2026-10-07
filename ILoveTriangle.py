import math
import os
from datetime import datetime

LOG_FILE = "triangle_log.txt"


def log(message: str) -> None:
    """Записывает сообщение в лог-файл с отметкой времени."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def log_separator() -> None:
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write("-" * 60 + "\n")


def parse_float(s: str):
    """Возвращает float или None, если строка не является числом."""
    if s is None:
        return None
    s = s.strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def r1(x: float) -> float:
    """Округление до одной цифры после запятой."""
    return round(x, 1)


def is_triangle(a: float, b: float, c: float) -> bool:
    """
    Проверка, образуют ли a, b, c невырожденный треугольник.
    Все значения округляются до 1 знака после запятой.
    """
    a, b, c = r1(a), r1(b), r1(c)
    if a <= 0 or b <= 0 or c <= 0:
        return False
    # Вырожденный случай: сумма двух сторон (с округлением) равна третьей
    if r1(a + b) == c or r1(a + c) == b or r1(b + c) == a:
        return False
    # Строгое нарушение неравенства треугольника
    if r1(a + b) < c or r1(a + c) < b or r1(b + c) < a:
        return False
    return True


def triangle_type(a: float, b: float, c: float) -> str:
    """Определяет вид треугольника (предполагается, что это треугольник)."""
    a, b, c = r1(a), r1(b), r1(c)
    if a == b and b == c:
        return "равносторонний"
    if a == b or b == c or a == c:
        return "равнобедренный"
    return "разносторонний"


def compute_vertices(a: float, b: float, c: float, size: int = 100, padding: int = 5):
    """
    Возвращает список из трёх вершин (int, int) для отрисовки в поле size x size.
    Вершины: A = (0,0), B = (c,0), C = (x,y).
    |AC| = b, |BC| = a.
    """
    a, b, c = r1(a), r1(b), r1(c)

    x = (b * b - a * a + c * c) / (2.0 * c)
    y2 = b * b - x * x
    if y2 < 0:
        y2 = 0.0
    y = math.sqrt(y2)

    pts = [(0.0, 0.0), (c, 0.0), (x, y)]

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    w = maxx - minx
    h = maxy - miny

    avail = size - 2 * padding
    scale = 1.0
    if w > 0:
        scale = min(scale, avail / w)
    if h > 0:
        scale = min(scale, avail / h)

    result = []
    for (px, py) in pts:
        nx = (px - minx) * scale + padding
        # Инверсия по Y (экранная ось Y направлена вниз)
        ny = size - ((py - miny) * scale + padding)
        result.append((int(round(nx)), int(round(ny))))

    return result


def main():
    # Инициализация лога
    if not os.path.exists(LOG_FILE):
        log("=== Запуск программы ===")
    else:
        log("=== Новый запуск программы ===")

    print("Введите a,b,c (для выхода введите пустую строку в поле 'a')")
    log("Программа запущена, ожидание ввода пользователя")

    while True:
        try:
            a_str = input("Введите a: ")
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            log("Получен сигнал завершения (EOF/KeyboardInterrupt). Выход.")
            break

        if a_str.strip() == "":
            print("Выход.")
            log("Пользователь ввёл пустую строку. Выход.")
            break

        try:
            b_str = input("Введите b: ")
            c_str = input("Введите c: ")
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            log("Получен сигнал завершения (EOF/KeyboardInterrupt). Выход.")
            break

        log(f"Ввод: a='{a_str}', b='{b_str}', c='{c_str}'")

        values = [parse_float(a_str), parse_float(b_str), parse_float(c_str)]

        # Нечисловые данные
        if any(v is None for v in values):
            print("")
            print([(-2, -2), (-2, -2), (-2, -2)])
            log("Результат: НЕЧИСЛОВЫЕ данные -> тип='', "
                "координаты=[(-2,-2),(-2,-2),(-2,-2)]")
        else:
            a, b, c = values
            if not is_triangle(a, b, c):
                print("не треугольник")
                print([(-1, -1), (-1, -1), (-1, -1)])
                log("Результат: не треугольник -> "
                    "координаты=[(-1,-1),(-1,-1),(-1,-1)]")
            else:
                ttype = triangle_type(a, b, c)
                coords = compute_vertices(a, b, c)
                print(ttype)
                print(coords)
                log(f"Результат: тип='{ttype}', координаты={coords}")

        print("-" * 40)
        log_separator()


if __name__ == "__main__":
    main()