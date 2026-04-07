from decimal import Decimal

from domain import Room


def calculate_base_price(room: Room, nights: int) -> Decimal:
    return room.price_per_night * nights


def apply_long_stay_discount(
    total: Decimal, nights: int, use_discount: bool
) -> Decimal:
    if use_discount and nights >= 3:
        return total * Decimal("0.90")
    return total


def apply_room_surcharge(total: Decimal, room: Room) -> Decimal:
    if room.room_type == "suite":
        return total + Decimal("40")
    return total


def calculate_total_price(room: Room, nights: int, use_discount: bool) -> Decimal:
    total = calculate_base_price(room, nights)
    total = apply_long_stay_discount(total, nights, use_discount)
    total = apply_room_surcharge(total, room)
    return total
