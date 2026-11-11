from __future__ import annotations

import json
import sqlite3
from typing import Optional

from calculator import CalculationResult


class TriangleDatabase:
    def __init__(self, db_path: str = ":memory:") -> None:
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS triangles (
                length1 TEXT NOT NULL,
                length2 TEXT NOT NULL,
                length3 TEXT NOT NULL,
                triangle_type TEXT NOT NULL,
                error_message TEXT,
                coords TEXT NOT NULL,
                PRIMARY KEY (length1, length2, length3)
            )
            """
        )
        self.connection.commit()

    def add_record(self, result: CalculationResult) -> None:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO triangles
                (length1, length2, length3, triangle_type, error_message, coords)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                result.length1,
                result.length2,
                result.length3,
                result.triangle_type,
                result.error_message,
                json.dumps(result.coords, ensure_ascii=False),
            ),
        )
        self.connection.commit()

    def get_record(
        self, length1: str, length2: str, length3: str
    ) -> Optional[CalculationResult]:
        row = self.connection.execute(
            """
            SELECT length1, length2, length3, triangle_type, error_message, coords
            FROM triangles
            WHERE length1 = ? AND length2 = ? AND length3 = ?
            """,
            (length1, length2, length3),
        ).fetchone()

        if row is None:
            return None

        coords = [tuple(p) for p in json.loads(row["coords"])]

        return CalculationResult(
            length1=row["length1"],
            length2=row["length2"],
            length3=row["length3"],
            triangle_type=row["triangle_type"],
            error_message=row["error_message"],
            coords=coords,
        )

    def delete_record(self, length1: str, length2: str, length3: str) -> bool:
        cursor = self.connection.execute(
            """
            DELETE FROM triangles
            WHERE length1 = ? AND length2 = ? AND length3 = ?
            """,
            (length1, length2, length3),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self) -> None:
        self.connection.close()