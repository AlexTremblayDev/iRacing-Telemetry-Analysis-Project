
class Incident:
    """
    Base class for telemetry incidents, storing their timing,
    lap position, and severity.
    """

    def __init__(self, startTime, lapDistPercent, lapNumber, endTime=None):
        """Initialize an incident with its timing and lap information."""
        self.startTime = startTime
        self.endTime = endTime
        self.severity = 0
        self.lapDistPercent = lapDistPercent
        self.lapNumber = lapNumber

    def toString(self):
        """Return a formatted description of the incident and its lap position."""
        if isinstance(self, slideIncident):
            return "Slide: Lap " + str(self.lapNumber) + ", " + str(round(self.lapDistPercent * 100, 2)) + "%"
        else:
            return "Lap " + str(self.lapNumber) + ", " + str(round(self.lapDistPercent * 100, 2)) + "%"


class slideIncident(Incident):
    """
    Represents a vehicle slide, storing its maximum slip angle,
    timing, lap position, and severity.
    """

    def __init__(self, maxSlipAngle, startTime, endTime, lapDistPercent, lapNumber):
        """Initialize a slide incident with its recorded telemetry values."""
        super().__init__(startTime, lapDistPercent, lapNumber, endTime)
        self.maxSlipAngle = maxSlipAngle
        self.severity = 0


class wheelLockIncident(Incident):
    """
    Represents a wheel lock incident, storing its timing
    and severity.
    """

    def __init__(self, startTime, endTime):
        """Initialize a wheel lock incident with its start and end times."""
        super().__init__(startTime, endTime)
        self.severity = 0
