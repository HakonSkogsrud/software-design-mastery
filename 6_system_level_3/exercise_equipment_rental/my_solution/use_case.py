from domain import Equipment
from ports import EquipmentRepository
from errors import EquipmentAlreadyExistsError, EquipmentAlreadyRentedError, EquipmentNotFoundError


def register_equipment(equipment: Equipment, equipment_repository: EquipmentRepository) -> None:

    existing = equipment_repository.get(equipment.id)
    if existing is not None:
        raise EquipmentAlreadyExistsError() # add id

    equipment_repository.add(equipment)

def rent_equipment(equipment_wanted: Equipment, equipment_repository: EquipmentRepository):

    equipment = equipment_repository.get(equipment_wanted.id)

    if equipment is None:
        raise EquipmentNotFoundError()

    if equipment.is_rented:
        raise EquipmentAlreadyRentedError()

    rented_equipment = equipment.rent_to(equipment_wanted.renter_email)

    equipment_repository.update(rented_equipment)

    
    
