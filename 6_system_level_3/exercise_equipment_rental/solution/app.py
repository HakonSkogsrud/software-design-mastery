from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from console_notifier import ConsoleRentalNotifier
from domain import Equipment
from errors import (
    EquipmentAlreadyExistsError,
    EquipmentAlreadyRentedError,
    EquipmentNotFoundError,
)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlite_repository import SQLiteEquipmentRepository
from use_cases import register_equipment, rent_equipment

DATABASE_PATH = Path("equipment.db")

repository = SQLiteEquipmentRepository(DATABASE_PATH)
notifier = ConsoleRentalNotifier()


class EquipmentRequest(BaseModel):
    id: str
    name: str


class RentalRequest(BaseModel):
    equipment_id: str
    renter_email: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    repository.create_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/equipment")
def register_equipment_endpoint(
    request: EquipmentRequest,
) -> dict[str, str]:
    equipment = Equipment(
        id=request.id,
        name=request.name,
    )

    try:
        register_equipment(
            equipment,
            repository,
        )
    except EquipmentAlreadyExistsError as error:
        raise HTTPException(
            status_code=409,
            detail="Equipment already exists",
        ) from error

    return {"status": "registered"}


@app.post("/rentals")
def rent_equipment_endpoint(
    request: RentalRequest,
) -> dict[str, str]:
    try:
        rent_equipment(
            equipment_id=request.equipment_id,
            renter_email=request.renter_email,
            repository=repository,
            notifier=notifier,
        )
    except EquipmentNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found",
        ) from error
    except EquipmentAlreadyRentedError as error:
        raise HTTPException(
            status_code=409,
            detail="Equipment is already rented",
        ) from error

    return {"status": "rented"}
