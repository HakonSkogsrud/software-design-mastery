from dataclasses import dataclass


@dataclass(frozen=True)
class Equipment:
    id: str
    name: str
    renter_email: str | None = None

    @property
    def is_rented(self) -> bool:
        return self.renter_email is not None

    def rent_to(self, renter_email: str) -> "Equipment":
        if self.is_rented:
            raise ValueError("Equipment is already rented")

        return Equipment(
            id=self.id,
            name=self.name,
            renter_email=renter_email,
        )
