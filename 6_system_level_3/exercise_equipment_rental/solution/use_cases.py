from domain import Equipment
from errors import (
    EquipmentAlreadyExistsError,
    EquipmentAlreadyRentedError,
    EquipmentNotFoundError,
)
from ports import EquipmentRepository, RentalNotifier


def register_equipment(
    equipment: Equipment,
    repository: EquipmentRepository,
) -> None:
    existing = repository.get(equipment.id)

    if existing is not None:
        raise EquipmentAlreadyExistsError(equipment.id)

    repository.add(equipment)


def rent_equipment(
    equipment_id: str,
    renter_email: str,
    repository: EquipmentRepository,
    notifier: RentalNotifier,
) -> None:
    equipment = repository.get(equipment_id)

    if equipment is None:
        raise EquipmentNotFoundError(equipment_id)

    if equipment.is_rented:
        raise EquipmentAlreadyRentedError(equipment_id)

    rented_equipment = equipment.rent_to(renter_email)

    repository.update(rented_equipment)

    notifier.rental_confirmed(
        rented_equipment,
        renter_email,
    )
