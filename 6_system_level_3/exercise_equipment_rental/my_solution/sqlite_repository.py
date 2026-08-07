from pathlib import Path
from domain import Equipment
import sqlite3
from pathlib import Path


class SqliteEquipmentRepository:

    def __init__(self, path: Path):
        self.database_path = path
        
    
    def create_database(self) -> None:
        with sqlite3.connect(self.database_path) as connection:
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
        
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO equipment (id, name, renter_email)
                VALUES (?, ?, NULL)
                """,
                (equipment.id, equipment.name),
            )
            
        
    def get(self, equipment_id: str) -> Equipment | None:
        with sqlite3.connect(self.database_path) as connection:
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
                equipment_id, name, renter_email)
            


    
    def update(self, equipment: Equipment) -> None:
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                UPDATE equipment
                SET renter_email = ?
                WHERE id = ?
                """,
                (equipment.renter_email, equipment.id),
            )
            
