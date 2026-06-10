from dataclasses import dataclass


@dataclass
class Logger:
    prefix: str

    def log(self, message):
        print(f"[{self.prefix}] {message}")


class SchedulePolicy:
    def reserve_slot(self, telescope_name, hours, logger):
        logger.log(f"Reserved {telescope_name} for {hours} hours")


@dataclass
class CalibrationRunner:
    logger: Logger

    def calibrate(self, telescope_name):
        self.logger.log(f"Calibrating {telescope_name}")


@dataclass
class PlanetTrackingService:
    logger: Logger
    schedule_policy: SchedulePolicy

    def schedule_tracking(self, telescope_name, planet_name):
        self.schedule_policy.reserve_slot(telescope_name, 2, self.logger)
        self.logger.log(f"Tracking planet: {planet_name}")


@dataclass
class DeepSpaceSurveyService:
    logger: Logger
    schedule_policy: SchedulePolicy

    def schedule_survey(self, telescope_name, region):
        self.schedule_policy.reserve_slot(telescope_name, 6, self.logger)
        self.logger.log(f"Surveying deep-space region: {region}")


@dataclass
class MirrorCalibrationService:
    logger: Logger
    calibration_runner: CalibrationRunner

    def calibrate_mirror(self, telescope_name):
        self.calibration_runner.calibrate(telescope_name)
        self.logger.log("Mirror calibration complete")


@dataclass
class SensorCalibrationService:
    logger: Logger
    calibration_runner: CalibrationRunner

    def calibrate_sensor(self, telescope_name):
        self.calibration_runner.calibrate(telescope_name)
        self.logger.log("Sensor calibration complete")


def main():
    observation_logger = Logger("LOG")
    calibration_logger = Logger("CALIBRATION")

    schedule_policy = SchedulePolicy()
    calibration_runner = CalibrationRunner(calibration_logger)

    planet_service = PlanetTrackingService(observation_logger, schedule_policy)
    planet_service.schedule_tracking("Hubble", "Mars")

    survey_service = DeepSpaceSurveyService(observation_logger, schedule_policy)
    survey_service.schedule_survey("James Webb", "Orion Nebula")

    mirror_calibration = MirrorCalibrationService(
        calibration_logger,
        calibration_runner,
    )
    mirror_calibration.calibrate_mirror("Hubble")

    sensor_calibration = SensorCalibrationService(
        calibration_logger,
        calibration_runner,
    )
    sensor_calibration.calibrate_sensor("James Webb")


if __name__ == "__main__":
    main()
