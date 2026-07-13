# app.py

import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATABASE_PATH = Path("equipment.db")


class EquipmentRequest(BaseModel):
    id: str
    name: str


class RentalRequest(BaseModel):
    equipment_id: str
    renter_email: str


def create_database() -> None:
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS equipment (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                renter_email TEXT
            )
            """
        )


def send_notification(recipient: str, message: str) -> None:
    print(f"Sending to {recipient}: {message}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    create_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/equipment")
def register_equipment(request: EquipmentRequest) -> dict[str, str]:
    with sqlite3.connect(DATABASE_PATH) as connection:
        existing = connection.execute(
            "SELECT id FROM equipment WHERE id = ?",
            (request.id,),
        ).fetchone()

        if existing is not None:
            raise HTTPException(
                status_code=409,
                detail="Equipment already exists",
            )

        connection.execute(
            """
            INSERT INTO equipment (id, name, renter_email)
            VALUES (?, ?, NULL)
            """,
            (request.id, request.name),
        )

    return {"status": "registered"}


@app.post("/rentals")
def rent_equipment(request: RentalRequest) -> dict[str, str]:
    with sqlite3.connect(DATABASE_PATH) as connection:
        row = connection.execute(
            """
            SELECT id, name, renter_email
            FROM equipment
            WHERE id = ?
            """,
            (request.equipment_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Equipment not found",
            )

        equipment_id, name, renter_email = row

        if renter_email is not None:
            raise HTTPException(
                status_code=409,
                detail="Equipment is already rented",
            )

        connection.execute(
            """
            UPDATE equipment
            SET renter_email = ?
            WHERE id = ?
            """,
            (request.renter_email, equipment_id),
        )

    send_notification(
        request.renter_email,
        f"You have rented {name}.",
    )

    return {"status": "rented"}
