class LoggingMixin:
    def log(self, message):
        print(f"[LOG] {message}")


class AuditMixin:
    def record_audit_event(self, artifact_id, action):
        self.log(f"Artifact {artifact_id}: {action}")


class HumidityRulesMixin:
    def max_humidity(self):
        return self.allowed_humidity


class TemperatureRulesMixin:
    def max_temperature(self):
        return self.allowed_temperature


class PaintingPreservationService(
    LoggingMixin,
    AuditMixin,
    HumidityRulesMixin,
    TemperatureRulesMixin,
):
    def __init__(self):
        self.allowed_humidity = 50
        self.allowed_temperature = 21

    def inspect(self, artifact_id, current_humidity, current_temperature):
        self.record_audit_event(artifact_id, "Inspecting painting")

        if current_humidity > self.max_humidity():
            self.log("Humidity too high for painting")

        if current_temperature > self.max_temperature():
            self.log("Temperature too high for painting")


class ManuscriptPreservationService(
    LoggingMixin,
    AuditMixin,
    HumidityRulesMixin,
):
    def __init__(self):
        self.allowed_humidity = 40

    def inspect(self, artifact_id, current_humidity):
        self.record_audit_event(artifact_id, "Inspecting manuscript")

        if current_humidity > self.max_humidity():
            self.log("Humidity too high for manuscript")


class VibrationRulesMixin:
    def max_vibration(self):
        return self.allowed_vibration


class AuditLoggingMixin:
    def log(self, message):
        print(f"[AUDIT] {message}")


class SculpturePreservationService(
    AuditLoggingMixin,
    AuditMixin,
    VibrationRulesMixin,
):
    def __init__(self):
        self.allowed_vibration = 5

    def inspect(self, artifact_id, current_vibration):
        self.record_audit_event(artifact_id, "Inspecting sculpture")

        if current_vibration > self.max_vibration():
            self.log("Vibration too high for sculpture")


def main():
    painting_service = PaintingPreservationService()
    painting_service.inspect(
        artifact_id="P-101",
        current_humidity=55,
        current_temperature=23,
    )

    print()

    manuscript_service = ManuscriptPreservationService()
    manuscript_service.inspect(
        artifact_id="M-205",
        current_humidity=45,
    )

    print()

    sculpture_service = SculpturePreservationService()
    sculpture_service.inspect(
        artifact_id="S-309",
        current_vibration=8,
    )


if __name__ == "__main__":
    main()
