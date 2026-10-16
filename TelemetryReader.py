
import irsdk
from TelemetrySession import TelemetrySession


class TelemetryReader:
    """
    Handles reading telemetry data from iRacing IBT files
    and storing it in a TelemetrySession object.
    """

    def loadFile(self, filePath):
        """Load telemetry data from an IBT file and return a TelemetrySession."""
        ibt = irsdk.IBT()
        ibt.open(filePath)

        session = TelemetrySession()

        # Retrieve recorded telemetry channels.
        session.times = ibt.get_all("SessionTime")
        session.laps = ibt.get_all("Lap")
        session.throttles = ibt.get_all("Throttle")
        session.brakes = ibt.get_all("Brake")
        session.steering = ibt.get_all("SteeringWheelAngle")
        session.rpms = ibt.get_all("RPM")
        session.gears = ibt.get_all("Gear")
        session.RRtempsCL = ibt.get_all("RRtempCL")
        session.RRtempsCM = ibt.get_all("RRtempCM")
        session.RRtempsCR = ibt.get_all("RRtempCR")
        session.velocityx = ibt.get_all("VelocityX")
        session.velocityy = ibt.get_all("VelocityY")
        session.velocityz = ibt.get_all("VelocityZ")
        session.getVelocity()
        session.lateralAccelerations = ibt.get_all("LatAccel")
        session.speeds = ibt.get_all("Speed")
        session.getSlipAngles()
        session.pitches = ibt.get_all("Pitch")
        session.rolls = ibt.get_all("Roll")
        session.yaws = ibt.get_all("Yaw")
        session.yawRates = ibt.get_all("YawRate")
        session.lapDistCompleteds = ibt.get_all("LapDistPct")
        session.LapDeltaToOptimalLaps = ibt.get_all("LapDeltaToOptimalLap")
        session.LapDeltaToOptimalLap_DDs = ibt.get_all("LapDeltaToOptimalLap_DD")

        return session
