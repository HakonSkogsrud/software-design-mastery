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


animals = {
    "A100": Animal(id="A100", name="Milo", species="cat"),
    "A200": Animal(id="A200", name="Boris", species="dog"),
}

appointments: list[Appointment] = []


class AppointmentService:
    def schedule_appointment(self, request: AppointmentRequest):
        animal = animals.get(request.animal_id)

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

        appointments.append(appointment)

        print(f"Scheduled appointment for {animal.name}")
        return appointment


def main() -> None:
    service = AppointmentService()

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
    for saved_appointment in appointments:
        print(saved_appointment)


if __name__ == "__main__":
    main()
