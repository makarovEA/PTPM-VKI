from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class UserInteraction(ABC):
    @abstractmethod
    def get_triangle_sides(self) -> Optional[tuple[str, str, str]]:
        raise NotImplementedError


class ConsoleUserInteraction(UserInteraction):
    def get_triangle_sides(self) -> Optional[tuple[str, str, str]]:
        try:
            a = input("Введите a: ")
            if a.strip() == "":
                return None
            b = input("Введите b: ")
            c = input("Введите c: ")
        except (EOFError, KeyboardInterrupt):
            return None
        return a, b, c