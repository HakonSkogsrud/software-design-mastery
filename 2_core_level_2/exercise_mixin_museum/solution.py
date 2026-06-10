from dataclasses import dataclass


@dataclass
class Logger:
    prefix: str

    def log(self, message):
        print(f"[{self.prefix}] {message}")


@dataclass
class AuditRecorder:
    logger: Logger

    def record_event(self, artifact_id, action):
        self.logger.log(f"Artifact {artifact_id}: {action}")


@dataclass
class HumidityPolicy:
    allowed_humidity: int

    def is_too_humid(self, current_humidity):
        return current_humidity > self.allowed_humidity


@dataclass
class TemperaturePolicy:
    allowed_temperature: int

    def is_too_warm(self, current_temperature):
        return current_temperature > self.allowed_temperature


@dataclass
class VibrationPolicy:
    allowed_vibration: int

    def is_too_much_vibration(self, current_vibration):
        return current_vibration > self.allowed_vibration


@dataclass
class PaintingPreservationService:
    logger: Logger
    audit_recorder: AuditRecorder
    humidity_policy: HumidityPolicy
    temperature_policy: TemperaturePolicy

    def inspect(self, artifact_id, current_humidity, current_temperature):
        self.audit_recorder.record_event(artifact_id, "Inspecting painting")

        if self.humidity_policy.is_too_humid(current_humidity):
            self.logger.log("Humidity too high for painting")

        if self.temperature_policy.is_too_warm(current_temperature):
            self.logger.log("Temperature too high for painting")


@dataclass
class ManuscriptPreservationService:
    logger: Logger
    audit_recorder: AuditRecorder
    humidity_policy: HumidityPolicy

    def inspect(self, artifact_id, current_humidity):
        self.audit_recorder.record_event(artifact_id, "Inspecting manuscript")

        if self.humidity_policy.is_too_humid(current_humidity):
            self.logger.log("Humidity too high for manuscript")


@dataclass
class SculpturePreservationService:
    logger: Logger
    audit_recorder: AuditRecorder
    vibration_policy: VibrationPolicy

    def inspect(self, artifact_id, current_vibration):
        self.audit_recorder.record_event(artifact_id, "Inspecting sculpture")

        if self.vibration_policy.is_too_much_vibration(current_vibration):
            self.logger.log("Vibration too high for sculpture")


def main():
    normal_logger = Logger("LOG")
    audit_logger = Logger("AUDIT")

    audit_recorder = AuditRecorder(audit_logger)

    painting_service = PaintingPreservationService(
        logger=normal_logger,
        audit_recorder=audit_recorder,
        humidity_policy=HumidityPolicy(allowed_humidity=50),
        temperature_policy=TemperaturePolicy(allowed_temperature=21),
    )
    painting_service.inspect(
        artifact_id="P-101",
        current_humidity=55,
        current_temperature=23,
    )

    print()

    manuscript_service = ManuscriptPreservationService(
        logger=normal_logger,
        audit_recorder=audit_recorder,
        humidity_policy=HumidityPolicy(allowed_humidity=40),
    )
    manuscript_service.inspect(
        artifact_id="M-205",
        current_humidity=45,
    )

    print()

    sculpture_service = SculpturePreservationService(
        logger=normal_logger,
        audit_recorder=audit_recorder,
        vibration_policy=VibrationPolicy(allowed_vibration=5),
    )
    sculpture_service.inspect(
        artifact_id="S-309",
        current_vibration=8,
    )


if __name__ == "__main__":
    main()
