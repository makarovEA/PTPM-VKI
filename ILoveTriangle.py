import math
import sys
import logging

# --- Настройка логирования ---
LOG_FILE = "triangle_log.txt"

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")

logger = logging.getLogger("triangle")


def r1(x: float) -> float:
    """Округление до одной цифры после запятой."""
    return round(x, 1)


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


def is_triangle(a: float, b: float, c: float) -> bool:
    """
    Проверка, образуют ли a, b, c невырожденный треугольник.
    Все значения округляются до 1 знака после запятой.
    """
    a, b, c = r1(a), r1(b), r1(c)
    if a <= 0 or b <= 0 or c <= 0:
        return False
    if r1(a + b) == c or r1(a + c) == b or r1(b + c) == a:
        return False
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
    logger.info("Логгер успешно сконфигурирован")
    logger.info("Приложение запущено")

    print("Введите a,b,c (для выхода введите пустую строку в поле 'a')")
    logger.debug("Ожидание ввода пользователя")

    while True:
        try:
            a_str = input("Введите a: ")
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            logger.info("Получен сигнал завершения (EOF/KeyboardInterrupt). Выход.")
            break

        if a_str.strip() == "":
            print("Выход.")
            logger.info("Пользователь ввёл пустую строку. Выход.")
            break

        try:
            b_str = input("Введите b: ")
            c_str = input("Введите c: ")
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            logger.info("Получен сигнал завершения (EOF/KeyboardInterrupt). Выход.")
            break

        logger.debug(f"Ввод: a='{a_str}', b='{b_str}', c='{c_str}'")

        values = [parse_float(a_str), parse_float(b_str), parse_float(c_str)]

        # Нечисловые данные
        if any(v is None for v in values):
            print("")
            print([(-2, -2), (-2, -2), (-2, -2)])
            logger.warning(
                "Результат: НЕЧИСЛОВЫЕ данные -> тип='', "
                "координаты=[(-2,-2),(-2,-2),(-2,-2)]"
            )
        else:
            a, b, c = values
            if not is_triangle(a, b, c):
                print("не треугольник")
                print([(-1, -1), (-1, -1), (-1, -1)])
                logger.info(
                    "Результат: не треугольник -> "
                    "координаты=[(-1,-1),(-1,-1),(-1,-1)]"
                )
            else:
                ttype = triangle_type(a, b, c)
                coords = compute_vertices(a, b, c)
                print(ttype)
                print(coords)
                logger.info(f"Результат: тип='{ttype}', координаты={coords}")

        print("-" * 40)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Непредвиденная ошибка")
        raise
    finally:
        logger.info("Приложение завершено")