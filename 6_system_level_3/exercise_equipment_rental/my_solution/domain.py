from dataclasses import dataclass

@dataclass(frozen=True)
class Equipment:
    id: str
    name: str
    renter_email: str = ""

    @property
    def is_rented(self) -> bool:
        return self.renter_email is not None

    def rent_to(self, email: str) -> Equipment:
        return Equipment(
            self.id,
            self.name,
            renter_email=email)
    
