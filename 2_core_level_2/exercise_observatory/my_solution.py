# 1
# a) LoggedService -> ScheduledService -> PlanetTrackingService
# b) LoggedService -> ScheduledService -> DeepSpaceSurveyService
# c) CalibrationService -> MirrorCalibrationService
# d) CalibrationService -> SensorCalibrationService
#
# 2
# a+b: reserve_slot and log
# c+d: calibrate and log
#
# 3
# A change in the ealier classes will implicitly affect the later ones,
#
# 4

from dataclasses import dataclass

@dataclass
class Logger:
    prefix: str
    def log(self, message) -> None:
        print(f"[{self.prefix}] {message}")


@dataclass
class ScheduledService():
    logger: Logger
        
    def reserve_slot(self, telescope_name, hours) -> None:
        self.logger.log(message=f"Reserved {telescope_name} for {hours} hours")


@dataclass
class PlanetTrackingService(ScheduledService):

    logger: Logger
    scheduled_service: ScheduledService
    
    def schedule_tracking(self, telescope_name, planet_name) -> None:
        self.scheduled_service.reserve_slot(telescope_name, hours= 2)
        self.logger.log(message=f"Tracking planet: {planet_name}")

        
@dataclass
class DeepSpaceSurveyService():
    logger: Logger
    scheduled_service: ScheduledService
        
    def schedule_survey(self, telescope_name, region) -> None:
        self.scheduled_service.reserve_slot(telescope_name, hours=6)
        self.logger.log(message=f"Surveying deep-space region: {region}")

@dataclass
class CalibrationService:
    logger: Logger

    def calibrate(self, telescope_name):
        self.logger.log(f"Calibrating {telescope_name}")
        

@dataclass
class MirrorCalibrationService():

    calibration_service: CalibrationService
    logger: Logger

    def calibrate_mirror(self, telescope_name) -> None:
        self.calibration_service.calibrate(telescope_name)
        self.logger.log("Mirror calibration complete")


@dataclass
class SensorCalibrationService(CalibrationService):
    calibration_service: CalibrationService
    logger: Logger
    
    def calibrate_sensor(self, telescope_name:str):
        self.calibration_service.calibrate(telescope_name=telescope_name)
        self.logger.log("Sensor calibration complete")


def main():

    logger = Logger(prefix="LOG")
    scheduled_service = ScheduledService(logger=logger)
        
    planet_service = PlanetTrackingService(logger=logger, scheduled_service=scheduled_service)
    planet_service.schedule_tracking("Hubble", "Mars")

    survey_service = DeepSpaceSurveyService(logger=logger, scheduled_service=scheduled_service)
    survey_service.schedule_survey("James Webb", "Orion Nebula")

    calibration_logger = Logger(prefix="CALIBRATE")
    calibration_service = CalibrationService(logger = calibration_logger)
    mirror_calibration = MirrorCalibrationService(calibration_service=calibration_service, logger=calibration_logger)
    mirror_calibration.calibrate_mirror("Hubble")

    sensor_calibration = SensorCalibrationService(calibration_service=calibration_service,
                                                  logger=calibration_logger)
    sensor_calibration.calibrate_sensor("James Webb")


if __name__ == "__main__":
    main()

#
# 5
# duplication in constructors?? dunno
#
# Reflection questions:
# 
