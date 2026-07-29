#
# 1
# stored in global variable
#
# 2
# animals and appointments introduce global coupling
# 
# 3 & 4

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


@dataclass
class AppointmentService:

    appointment_registry: AppointmentRegistry
    animal_registry: AnimalRegistry

    def schedule_appointment(self, request: AppointmentRequest):
        animal = self.animal_registry.get_animal(request.animal_id)

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

        self.appointment_registry.appointments.append(appointment)

        print(f"Scheduled appointment for {animal.name}")
        return appointment


class AppointmentRegistry:
    appointments: list[Appointment]
    

class AnimalRegistry:
    animals: list[Animal]

    def get_animal(self, id):
        return next((animal for animal in self.animals if animal.id == id), None)
    
    def add_animal(self, Animal):
        self.animals.append(Animal)

    
def main() -> None:

    animal_registry = AnimalRegistry()
    animal_registry.add_animal(Animal(id="A100", name="Milo", species="cat"))
    animal_registry.add_animal(Animal(id="A200", name="Boris", species="dog"))
    
    
    appointment_registry = AppointmentRegistry()
    service = AppointmentService(appointment_registry, animal_registry)
    

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
    for saved_appointment in  appointment_registry.appointments:
        print(saved_appointment)


if __name__ == "__main__":
    main()


# 5
# improves separation because persistence concerns are separated from logic 
# improves resilience because changes to storage is less likely to affect appointments
