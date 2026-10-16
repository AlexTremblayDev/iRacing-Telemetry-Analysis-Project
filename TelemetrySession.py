
import math
import numpy as np
from Incident import Incident
from Incident import slideIncident


class TelemetrySession:
    """
    Stores telemetry data from an iRacing session and provides methods
    for calculating vehicle dynamics, lap times, and detecting incidents.
    """

    def __init__(self):
        """Initialize lists for recorded and calculated telemetry data."""
        self.times = []
        self.laps = []
        self.throttles = []
        self.brakes = []
        self.steering = []
        self.rpms = []
        self.gears = []
        self.RRtempsCL = []
        self.RRtempsCM = []
        self.RRtempsCR = []
        self.velocityx = []
        self.velocityy = []
        self.velocityz = []
        self.velocity = []
        self.lateralAccelerations = []
        self.speeds = []
        self.slipAngles = []
        self.pitches = []
        self.rolls = []
        self.yaws = []
        self.yawRates = []
        self.lapDistCompleteds = []
        self.LapDeltaToOptimalLaps = []
        self.LapDeltaToOptimalLap_DDs = []

    def getLapStartTimes(self):
        """Return the session times corresponding to the beginning of each lap."""
        x = 0
        currentLap = 0
        lapStartTimes = []

        # Identify lap boundaries by detecting increases in lap number.
        for i in self.times:
            if self.laps[x] > currentLap:
                lapStartTimes.append(self.times[x])
                currentLap = self.laps[x]
            x += 1
        return lapStartTimes

    def getLapTimes(self):
        """Calculate lap times using the difference between consecutive lap starts."""
        lapStartTimes = self.getLapStartTimes()
        x = 0
        lapTimes = []
        for i in lapStartTimes:
            if x < len(lapStartTimes) - 1:
                lapTimes.append(lapStartTimes[x + 1] - lapStartTimes[x])
            x += 1
        return lapTimes

    def getVelocity(self):
        """Calculate horizontal velocity magnitude from longitudinal and lateral velocities."""
        x = 0
        for i in self.velocityx:
            self.velocity.append(np.sqrt((self.velocityx[x] * self.velocityx[x]) + (self.velocityy[x] * self.velocityy[x])))
            x += 1

    def getSlipAngles(self):
        """Calculate vehicle slip angles in degrees from velocity components."""
        x = 0
        for i in self.times:
            self.slipAngles.append(math.degrees(math.atan2(self.velocityy[x], self.velocityx[x])))
            x += 1

    def getLateralAccelerationDisparities(self):
        """Calculate the absolute difference between measured and expected lateral acceleration."""
        x = 0
        lateralAccelerationDisparities = []
        for i in self.lateralAccelerations:
            lateralAccelerationDisparities.append(abs(self.lateralAccelerations[x] - (self.velocityx[x] * self.yawRates[x])))
            x += 1
        return lateralAccelerationDisparities

    def detectIncidents(self):
        """
        Detect potential incidents using lap time delta changes
        and check whether each incident involved a slide.
        """
        incidents = []
        currentIncident = None
        x = 0

        # Identify incident intervals using a delta rate threshold of 0.075.
        for i in self.LapDeltaToOptimalLap_DDs:
            if self.LapDeltaToOptimalLap_DDs[x] > 0.075 and currentIncident == None:
                currentIncident = Incident(startTime=self.times[x], lapDistPercent=self.lapDistCompleteds[x], lapNumber=self.laps[x])

            elif self.LapDeltaToOptimalLap_DDs[x] <= 0.075 and currentIncident is not None:
                currentIncident.endTime = self.times[x]
                startIndex = self.times.index(currentIncident.startTime)
                endIndex = self.times.index(currentIncident.endTime)
                incidents.append(currentIncident)

                # Previous slide detection implementation (currently disabled).
                # difference of 1 and timeframe of 0.2 seconds is being used as a PLACEHOLDER
                #detectingSlide = False
                #for j in range(startIndex, endIndex):
                #    if abs(self.lateralAccelerations[int(j)] - (self.velocityx[int(j)] * self.yawRates[int(j)])) > 1 and not detectingSlide:
                #        detectingSlide = True
                #        startSlideTime = self.times[j]
                #    elif abs(self.lateralAccelerations[int(j)] - (self.velocityx[int(j)] * self.yawRates[int(j)])) < 1 and detectingSlide:
                #        detectingSlide = False
                #        endSlideTime = self.times[j]
                #        if endSlideTime - startSlideTime > 0.2:
                #            currentIncident = slideIncident(maxSlipAngle=max(abs(self.slipAngles[startIndex:endIndex])), 
                #                                            startTime=startSlideTime, endTime=endSlideTime, 
                #                                            lapDistPercent=currentIncident.lapDistPercent, 
                #                                            lapNumber=currentIncident.lapNumber)
                currentIncident = None

            x += 1
        self.detectSlideIncidents(incidents)
        return incidents

    def getAllIncidents(self):
        """Placeholder for retrieving all detected incidents."""
        return

    def detectSlideIncidents(self, incidentList):
        """
        Identify potential slides using lateral acceleration disparities.

        Uses provisional thresholds of 1 m/s² for acceleration
        disparity and 0.2 seconds for minimum slide duration.
        These values have not yet been validated against known slides.

        Qualifying incidents are replaced with slideIncident objects
        in the provided incident list.
        """
        for index, incident in enumerate(incidentList):
            startIndex = self.times.index(incident.startTime)
            endIndex = self.times.index(incident.endTime)

            detectingSlide = False

            for j in range(startIndex, endIndex):
                # Compare measured lateral acceleration with velocity-based expectation.
                residual = abs(
                    self.lateralAccelerations[j]
                    - (self.velocityx[j] * self.yawRates[j])
                )

                # Start tracking a potential slide above the disparity threshold.
                if residual > 1 and not detectingSlide:
                    detectingSlide = True
                    startSlideTime = self.times[j]

                elif residual < 1 and detectingSlide:
                    detectingSlide = False
                    endSlideTime = self.times[j]

                    # Require a sustained disparity before classifying the incident as a slide.
                    if endSlideTime - startSlideTime > 0.2:
                        incidentList[index] = slideIncident(
                            maxSlipAngle=max(
                                abs(angle)
                                for angle in self.slipAngles[startIndex:endIndex]
                            ),
                            startTime=incident.startTime,
                            endTime=incident.endTime,
                            lapDistPercent=incident.lapDistPercent,
                            lapNumber=incident.lapNumber
                        )
                        break

    def diagnoseIncidents(self):
        """Placeholder for further analysis and diagnosis of detected incidents."""
        incidents = self.detectIncidents()

        for incident in incidents:
            # Locate the incident's start and end positions in the telemetry data.
            startIndex = self.times.index(incident.startTime)
            endIndex = self.times.index(incident.endTime)

            

   # def isInSlipAngle(self):
