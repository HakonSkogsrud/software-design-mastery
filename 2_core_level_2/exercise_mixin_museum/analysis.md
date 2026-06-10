> Don't read any further until you tried coming up with a solution yourself!


# Solution & Analysis

The original design uses mixins to share behavior between preservation services. That looks convenient at first, but it hides important dependencies.

The services depend on behavior that is not visible in their constructor. For example:
```python
class PaintingPreservationService(
    LoggingMixin,
    AuditMixin,
    HumidityRulesMixin,
    TemperatureRulesMixin,
):
    ...
```

This class depends on logging, audit recording, humidity rules, and temperature rules. But those dependencies are hidden in the inheritance list.

Also, some mixins assume that certain attributes exist.

```python
class HumidityRulesMixin:
    def max_humidity(self):
        return self.allowed_humidity
```

This mixin silently requires the service to define `self.allowed_humidity`.

AuditMixin calls `self.log()`:

```python
class AuditMixin:
    def record_audit_event(self, artifact_id, action):
        self.log(f"Artifact {artifact_id}: {action}")
```

That means `AuditMixin` depends on some other mixin or parent class providing `log()`. This is another hidden contract.

## Refactored Design

The solution replaces mixins with explicit collaborators. Each service receives only the collaborators it actually needs.

For example, the painting service depends on:

```python
@dataclass
class PaintingPreservationService:
    logger: Logger
    audit_recorder: AuditRecorder
    humidity_policy: HumidityPolicy
    temperature_policy: TemperaturePolicy
```

This is clearer than inheriting from four mixins.

## Why This is Better

### Alignment

The dependencies now point toward the actual collaborators.

Before:

```python
class PaintingPreservationService(LoggingMixin, AuditMixin, ...)
```

After:

```python
PaintingPreservationService(
    logger=normal_logger,
    audit_recorder=audit_recorder,
    humidity_policy=HumidityPolicy(allowed_humidity=50),
    temperature_policy=TemperaturePolicy(allowed_temperature=21),
)
```

The design now says: "This service uses logging, auditing, and policies." That's a more accurate relationship than inheritance.


### Clarity

The required state is no longer hidden.

Before, `HumidityRulesMixin` required `allowed_humidity`, but that was only visible if you inspected the mixin.

After, the humidity limit is part of an explicit policy:

```python
HumidityPolicy(allowed_humidity=50)
```

That makes the rule easier to find and easier to change.

### Resilience

Changes become more local. For example, audit logging can use one logger:

```python
audit_logger = Logger("AUDIT")
```

while normal preservation warnings use another:

```python
normal_logger = Logger("LOG")
```

Changing audit formatting no longer requires changing mixins or inheritance order.

## Trade-off

The composition-based version has more setup code. Instead of just creating a service, we create and pass collaborators:

```python
painting_service = PaintingPreservationService(
    logger=normal_logger,
    audit_recorder=audit_recorder,
    humidity_policy=HumidityPolicy(allowed_humidity=50),
    temperature_policy=TemperaturePolicy(allowed_temperature=21),
)
```

But that does mean we have more control when we create the service. We can patch everything up in one place. This also makes it easier to write tests later on and replace some of these loggers and policies with dummy objects.


## Key Takeaway

Mixins can reduce duplication, but they often hide structure. In this example, the services did not need to inherit logging, auditing, or preservation rules. They needed to use those things.Composition makes that relationship explicit.

