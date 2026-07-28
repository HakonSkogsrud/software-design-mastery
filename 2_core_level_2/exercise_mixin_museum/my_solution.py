class LoggerService:
    def log(self, message: str):
        print(f"[LOG] {message}")


class AuditService:
    def __init__(self, logger_service: LoggerService):
        self.logger_service = logger_service

    def record_audit_event(self, artifact_id: str, action: str):
        self.logger_service.log(f"Artifact {artifact_id}: {action}")


class HumidityService:

    def __init__(self, allowed_humidity: int):
        self.allowed_humidity=allowed_humidity

    def max_humidity(self) -> int:
        return self.allowed_humidity


class TemperatureService:

    def __init__(self, allowed_temperature: int):
        self.allowed_temperature = allowed_temperature

    def max_temperature(self) -> int:
        return self.allowed_temperature


class PaintingPreservationService():

    def __init__(self, 
                 logger_service: LoggerService, 
                 humidity_service: HumidityService, 
                 temperature_service: TemperatureService,
                 audit_service: AuditService):
        
        self.logger_service: LoggerService = logger_service
        self.humidity_service: HumidityService = humidity_service
        self.temperature_service: TemperatureService = temperature_service
        self.audit_service: AuditService = audit_service

    def inspect(self, artifact_id:str, current_humidity:int, current_temperature:int): 
        self.audit_service.record_audit_event(artifact_id, "Inspecting painting")

        if current_humidity > self.humidity_service.max_humidity():
            self.logger_service.log("Humidity too high for painting")

        if current_temperature > self.temperature_service.max_temperature():
            self.logger_service.log("Temperature too high for painting")


class ManuscriptPreservationService():
    def __init__(self, audit_service: AuditService, logger_service:LoggerService, humidity_service:HumidityService):
        self.audit_service = audit_service
        self.logger_service = logger_service
        self.humidity_service = humidity_service


    def inspect(self, artifact_id:str, current_humidity:int):
        self.audit_service.record_audit_event(artifact_id, "Inspecting manuscript")

        if current_humidity > self.humidity_service.max_humidity():
            self.logger_service.log("Humidity too high for manuscript")



class VibrationService:
    def __init__(self, allowed_vibration:int):
        self.allowed_vibration = allowed_vibration

    def max_vibration(self):
        return self.allowed_vibration


class SculpturePreservationService():
    def __init__(self, audit_service: AuditService, vibration_service:VibrationService, logger_service:LoggerService):
        self.audit_service = audit_service
        self.vibration_service = vibration_service
        self.logger_service = logger_service

    def inspect(self, artifact_id:str, current_vibration:int):
        self.audit_service.record_audit_event(artifact_id, "Inspecting sculpture")

        if current_vibration > self.vibration_service.max_vibration():
            self.logger_service.log("Vibration too high for sculpture")


def main():

    logger_service = LoggerService()
    temperature_service = TemperatureService(allowed_temperature=44)
    humidity_service = HumidityService(allowed_humidity=33)
    audit_service = AuditService(logger_service)

    painting_service = PaintingPreservationService(logger_service=logger_service, 
                                                   temperature_service=temperature_service,
                                                   humidity_service=humidity_service,
                                                   audit_service=audit_service)
    painting_service.inspect(
        artifact_id="P-101",
        current_humidity=55,
        current_temperature=23,
    )

    print()

    manuscript_service = ManuscriptPreservationService(audit_service=audit_service, 
                                                       logger_service=logger_service, 
                                                       humidity_service=humidity_service)
    manuscript_service.inspect(
        artifact_id="M-205",
        current_humidity=45,
    )

    print()

    vibration_service = VibrationService(allowed_vibration=8)
    sculpture_service = SculpturePreservationService(audit_service=audit_service, 
                                                     logger_service=logger_service, 
                                                     vibration_service=vibration_service)
    sculpture_service.inspect(
        artifact_id="S-309",
        current_vibration=10,
    )


if __name__ == "__main__":
    main()
