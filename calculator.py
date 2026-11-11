from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional


def r1(x: float) -> float:
    """Округление до одной цифры после запятой."""
    return round(x, 1)


def parse_float(s: Optional[str]) -> Optional[float]:
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
    a, b, c = r1(a), r1(b), r1(c)
    if a <= 0 or b <= 0 or c <= 0:
        return False
    if r1(a + b) == c or r1(a + c) == b or r1(b + c) == a:
        return False
    if r1(a + b) < c or r1(a + c) < b or r1(b + c) < a:
        return False
    return True


def triangle_type(a: float, b: float, c: float) -> str:
    a, b, c = r1(a), r1(b), r1(c)
    if a == b and b == c:
        return "равносторонний"
    if a == b or b == c or a == c:
        return "равнобедренный"
    return "разносторонний"


def compute_vertices(
    a: float,
    b: float,
    c: float,
    size: int = 100,
    padding: int = 5,
) -> list[tuple[int, int]]:
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
    for px, py in pts:
        nx = (px - minx) * scale + padding
        ny = size - ((py - miny) * scale + padding)
        result.append((int(round(nx)), int(round(ny))))

    return result


@dataclass
class CalculationResult:
    length1: str
    length2: str
    length3: str
    triangle_type: str
    error_message: Optional[str]
    coords: list[tuple[int, int]]


class TriangleCalculator:
    def calculate(self, a_raw: str, b_raw: str, c_raw: str) -> CalculationResult:
        a_s = str(a_raw).strip()
        b_s = str(b_raw).strip()
        c_s = str(c_raw).strip()

        a = parse_float(a_s)
        b = parse_float(b_s)
        c = parse_float(c_s)

        if a is None or b is None or c is None:
            return CalculationResult(
                length1=a_s,
                length2=b_s,
                length3=c_s,
                triangle_type="",
                error_message="НЕЧИСЛОВЫЕ данные",
                coords=[(-2, -2), (-2, -2), (-2, -2)],
            )

        a, b, c = r1(a), r1(b), r1(c)

        if not is_triangle(a, b, c):
            return CalculationResult(
                length1=a_s,
                length2=b_s,
                length3=c_s,
                triangle_type="",
                error_message="не треугольник",
                coords=[(-1, -1), (-1, -1), (-1, -1)],
            )

        ttype = triangle_type(a, b, c)
        coords = compute_vertices(a, b, c)

        return CalculationResult(
            length1=a_s,
            length2=b_s,
            length3=c_s,
            triangle_type=ttype,
            error_message=None,
            coords=coords,
        )