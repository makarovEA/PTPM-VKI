from __future__ import annotations

from calculator import TriangleCalculator
from controller import Controller
from database import TriangleDatabase
from external import EmailServerStub
from user_io import ConsoleUserInteraction


def main() -> None:
    database = TriangleDatabase("triangles.db")
    controller = Controller(
        calculator=TriangleCalculator(),
        database=database,
        user_io=ConsoleUserInteraction(),
        external=EmailServerStub(),
    )

    try:
        while True:
            result = controller.process_one()
            if result is None:
                break
            print(Controller._format_result(result))
    finally:
        database.close()