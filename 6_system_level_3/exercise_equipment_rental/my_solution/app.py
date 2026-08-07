
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from use_case import register_equipment, rent_equipment
from domain import Equipment
from pathlib import Path
from errors import EquipmentAlreadyExistsError
from sqlite_repository import SqliteEquipmentRepository

DATABASE_PATH = Path("equipment.db")
repository = SqliteEquipmentRepository(DATABASE_PATH)




class EquipmentRequest(BaseModel):
    id: str
    name: str


class RentalRequest(BaseModel):
    equipment_id: str
    renter_email: str





def send_notification(recipient: str, message: str) -> None:
    print(f"Sending to {recipient}: {message}")

    
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    repository.create_database()
    yield

app = FastAPI(lifespan=lifespan)



@app.post("/equipment")
def register_equipment_endpoint(request: EquipmentRequest) -> dict[str, str]:

    equipment = Equipment(
        id=request.id,
        name= request.name,
        )

    try:
        register_equipment(equipment, repository)
    except EquipmentAlreadyExistsError:
        raise HTTPException(status_code=409, detail="whatever")



@app.post("/rentals")
def rent_equipment(request: RentalRequest) -> dict[str, str]:

    equipment = Equipment(request.equipment_id, request.renter_email)

    try:
        rent_equipment(equipment, equipment_repository, notifier)
    
