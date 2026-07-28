class LoggedService:
    def log(self, message):
        print(f"[LOG] {message}")


class ScheduledService(LoggedService):
    def reserve_slot(self, telescope_name, hours):
        self.log(f"Reserved {telescope_name} for {hours} hours")


class PlanetTrackingService(ScheduledService):
    def schedule_tracking(self, telescope_name, planet_name):
        self.reserve_slot(telescope_name, 2)
        self.log(f"Tracking planet: {planet_name}")


class DeepSpaceSurveyService(ScheduledService):
    def schedule_survey(self, telescope_name, region):
        self.reserve_slot(telescope_name, 6)
        self.log(f"Surveying deep-space region: {region}")


class CalibrationService:
    def log(self, message):
        print(f"[CALIBRATION] {message}")
        
    def calibrate(self, telescope_name):
        self.log(f"Calibrating {telescope_name}")


class MirrorCalibrationService(CalibrationService):
    def calibrate_mirror(self, telescope_name):
        self.calibrate(telescope_name)
        self.log("Mirror calibration complete")


class SensorCalibrationService(CalibrationService):
    def calibrate_sensor(self, telescope_name):
        self.calibrate(telescope_name)
        self.log("Sensor calibration complete")


def main():
    planet_service = PlanetTrackingService()
    planet_service.schedule_tracking("Hubble", "Mars")

    survey_service = DeepSpaceSurveyService()
    survey_service.schedule_survey("James Webb", "Orion Nebula")

    mirror_calibration = MirrorCalibrationService()
    mirror_calibration.calibrate_mirror("Hubble")

    sensor_calibration = SensorCalibrationService()
    sensor_calibration.calibrate_sensor("James Webb")


if __name__ == "__main__":
    main()
