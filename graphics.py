
import pandas as pd


class TelemetryGraph:
    """
    Handles graphing telemetry data from an iRacing session.
    Each graph displays data over time with markers for lap boundaries.
    """

    def __init__(self, session):
        """Initialize the graph with a telemetry session."""
        self.session = session

    def addLapLines(self, ax):
        """Mark the beginning of each lap on the graph."""
        startTimes = self.session.getLapStartTimes()

        for startTime in startTimes:
            ax.axvline(
                x=startTime,
                color="black",
                linestyle="--",
                alpha=0.5
            )

    def graphPedals(self, ax):
        """Graph throttle and brake inputs over time."""
        ax.clear()

        ax.plot(
            self.session.times,
            self.session.throttles,
            label="Throttle"
        )

        ax.plot(
            self.session.times,
            self.session.brakes,
            label="Brake"
        )

        self.addLapLines(ax)

        ax.set_xlabel("Time")
        ax.set_ylabel("Pedal Input")
        ax.set_title("Throttle / Brake")
        ax.legend()
        ax.grid(True)

    def graphSteering(self, ax):
        """Graph steering wheel angle over time."""
        ax.clear()

        ax.plot(
            self.session.times,
            self.session.steering,
            label="Steering"
        )

        self.addLapLines(ax)

        ax.set_xlabel("Time")
        ax.set_ylabel("Steering Angle")
        ax.set_title("Steering Wheel Angle")
        ax.grid(True)

    def graphSlipAngles(self, ax):
        """Graph vehicle slip angle over time."""
        ax.clear()

        ax.plot(
            self.session.times,
            self.session.slipAngles,
            label="Slip Angle"
        )

        self.addLapLines(ax)

        ax.set_xlabel("Time")
        ax.set_ylabel("Slip Angle")
        ax.set_title("Slip Angle")
        ax.grid(True)

    def graphLateralAccelerationDisparities(self, ax):
        """Graph calculated lateral acceleration disparities over time."""
        ax.clear()

        # Retrieve disparity values calculated from session telemetry.
        lateralAccelerationDisparities = self.session.getLateralAccelerationDisparities()

        ax.plot(
            self.session.times,
            lateralAccelerationDisparities,
            label="Lateral Acceleration Disparity"
        )

        self.addLapLines(ax)

        ax.set_xlabel("Time")
        ax.set_ylabel("Lateral Acceleration Disparity")
        ax.set_title("Lateral Acceleration Disparity")
        ax.grid(True)
