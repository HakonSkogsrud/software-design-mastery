import sqlite3
from pathlib import Path

from domain import Equipment


class SQLiteEquipmentRepository:
    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def create_database(self) -> None:
        with sqlite3.connect(self._database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS equipment (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    renter_email TEXT
                )
                """
            )

    def add(self, equipment: Equipment) -> None:
        with sqlite3.connect(self._database_path) as connection:
            connection.execute(
                """
                INSERT INTO equipment (id, name, renter_email)
                VALUES (?, ?, ?)
                """,
                (
                    equipment.id,
                    equipment.name,
                    equipment.renter_email,
                ),
            )

    def get(self, equipment_id: str) -> Equipment | None:
        with sqlite3.connect(self._database_path) as connection:
            row = connection.execute(
                """
                SELECT id, name, renter_email
                FROM equipment
                WHERE id = ?
                """,
                (equipment_id,),
            ).fetchone()

        if row is None:
            return None

        equipment_id, name, renter_email = row

        return Equipment(
            id=equipment_id,
            name=name,
            renter_email=renter_email,
        )

    def update(self, equipment: Equipment) -> None:
        with sqlite3.connect(self._database_path) as connection:
            connection.execute(
                """
                UPDATE equipment
                SET name = ?, renter_email = ?
                WHERE id = ?
                """,
                (
                    equipment.name,
                    equipment.renter_email,
                    equipment.id,
                ),
            )
