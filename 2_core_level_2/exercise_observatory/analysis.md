> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

The original design used inheritance to share behavior:

- `PlanetTrackingService` and `DeepSpaceSurveyService` inherited scheduling and logging behavior.
- `MirrorCalibrationService` and `SensorCalibrationService` inherited calibration and logging behavior.

The refactored version (see `solution.py`) replaces those inheritance relationships with composition. Services now receive the behavior they need instead of inheriting it.

## Why is this Better?

### Alignment

The dependencies are now explicit. The `PlanetTrackingService` now clearly shows what it depends on.

### Clarity

Reading the dataclass fields immediately tells us what the service needs. There is no need to inspect parent classes to understand where certain behavior comes from.

### Resilience

Changes become more local. For example, calibration services can use a different logger:

```python
calibration_logger = Logger("CALIBRATION")
```

without affecting scheduling services.

## Trade-off

The composition-based design requires a little more setup:

```python
planet_service = PlanetTrackingService(
    observation_logger,
    schedule_policy,
)
```

But in return we get explicit dependencies, less hidden coupling, easier changes, and clearer structure. Well worth the trade off in my opinion!

## Key Takeaway

Inheritance reuses behavior through parent classes. Composition reuses behavior through *collaborators*.

In this example, the services are not special kinds of scheduling or calibration classes. They simply use those capabilities, which makes composition the better fit.