from dataclasses import dataclass


@dataclass
class Animal:
    id: str
    name: str
    species: str


@dataclass
class AppointmentRequest:
    animal_id: str
    owner_email: str
    reason: str
    duration_minutes: int


@dataclass
class Appointment:
    animal_id: str
    owner_email: str
    reason: str
    duration_minutes: int


class AppointmentRepository:
    def __init__(self, animals: list[Animal]) -> None:
        self._animals = {animal.id: animal for animal in animals}
        self._appointments: list[Appointment] = []

    def get_animal(self, animal_id: str) -> Animal | None:
        return self._animals.get(animal_id)

    def save_appointment(self, appointment: Appointment) -> None:
        self._appointments.append(appointment)

    def list_appointments(self) -> list[Appointment]:
        return list(self._appointments)


class AppointmentService:
    def __init__(self, repository: AppointmentRepository) -> None:
        self.repository = repository

    def schedule_appointment(self, request: AppointmentRequest) -> Appointment | None:
        animal = self.repository.get_animal(request.animal_id)

        if animal is None:
            print("Animal not found")
            return None

        if request.duration_minutes <= 0:
            print("Invalid appointment duration")
            return None

        appointment = Appointment(
            animal_id=request.animal_id,
            owner_email=request.owner_email,
            reason=request.reason,
            duration_minutes=request.duration_minutes,
        )

        self.repository.save_appointment(appointment)

        print(f"Scheduled appointment for {animal.name}")
        return appointment


def main() -> None:
    repository = AppointmentRepository(
        animals=[
            Animal(id="A100", name="Milo", species="cat"),
            Animal(id="A200", name="Boris", species="dog"),
        ]
    )
    service = AppointmentService(repository)

    print("=== Scenario 1: Successful appointment ===")
    appointment = service.schedule_appointment(
        AppointmentRequest(
            animal_id="A100",
            owner_email="owner@example.com",
            reason="Annual check-up",
            duration_minutes=30,
        )
    )
    print(f"Appointment result: {appointment}")
    print()

    print("=== Scenario 2: Unknown animal ===")
    appointment = service.schedule_appointment(
        AppointmentRequest(
            animal_id="A999",
            owner_email="owner@example.com",
            reason="Vaccination",
            duration_minutes=20,
        )
    )
    print(f"Appointment result: {appointment}")
    print()

    print("=== Saved appointments ===")
    for saved_appointment in repository.list_appointments():
        print(saved_appointment)


if __name__ == "__main__":
    main()
