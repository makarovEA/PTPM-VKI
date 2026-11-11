from __future__ import annotations

from typing import Optional

from calculator import CalculationResult, TriangleCalculator
from database import TriangleDatabase
from external import ExternalDependency
from user_io import UserInteraction


class Controller:
    def __init__(
        self,
        calculator: TriangleCalculator,
        database: TriangleDatabase,
        user_io: UserInteraction,
        external: ExternalDependency,
    ) -> None:
        self.calculator = calculator
        self.database = database
        self.user_io = user_io
        self.external = external

    def process_one(self) -> Optional[CalculationResult]:
        raw = self.user_io.get_triangle_sides()
        if raw is None:
            return None

        a, b, c = (str(v).strip() for v in raw)

        cached = self.database.get_record(a, b, c)

        if cached is None:
            result = self.calculator.calculate(a, b, c)
            self.database.add_record(result)
        else:
            result = cached

        self.external.send_result(self._format_result(result))
        return result

    @staticmethod
    def _format_result(result: CalculationResult) -> str:
        if result.error_message:
            return f"{result.error_message}; coords={result.coords}"
        return f"{result.triangle_type}; coords={result.coords}"