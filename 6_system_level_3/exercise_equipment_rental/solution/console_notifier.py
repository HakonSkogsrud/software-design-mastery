from domain import Equipment


class ConsoleRentalNotifier:
    def rental_confirmed(
        self,
        equipment: Equipment,
        recipient: str,
    ) -> None:
        print(f"Sending to {recipient}: You have rented {equipment.name}.")
