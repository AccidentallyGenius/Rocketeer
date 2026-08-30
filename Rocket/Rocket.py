import pygame

from Rocket.Attachment import Attachment
from Simulation.PhysicsBody import PhysicsBody

class Rocket:
    def __init__(self):
        self.parts = []
        self.attachments = []
        self.physicsBody = PhysicsBody(0, 0, 0)
        self.origin = pygame.Vector2(0, 0)

    def addPart(self, part):
        self.parts.append(part)
        self.physicsBody.mass = self.getMass()

    def removePart(self, part):
        self.parts.remove(part)
        self.updateMass()

    def addAttachment(self, parent, child):
        attachment = Attachment(parent, child)
        self.attachments.append(attachment)

    def removeAttachment(self, parent, child):
        for attachment in self.attachments:
            if attachment.parent == parent and attachment.child == child:
                self.attachments.remove(attachment)

                return

    def removePartAttachments(self, part):
        for attachment in self.attachments[:]:
            if attachment.parent == part or attachment.child == part:
                self.attachments.remove(attachment)

    def getMass(self):
        mass = 0

        for buildPart in self.parts:
            mass += buildPart.part.mass

            if hasattr(buildPart.part, "getFuelMass"):
                mass += buildPart.part.getFuelMass()

        return mass

    def getThrust(self):
        thrust = 0

        for buildPart in self.parts:
            if hasattr(buildPart.part, "thrust"):
                thrust += buildPart.part.thrust

        return thrust

    def getFuelMass(self):
        fuelMass = 0

        for buildPart in self.parts:
            part = buildPart.part

            if hasattr(part, "getFuelMass"):
                fuelMass += part.getFuelMass()

        return fuelMass

    def getTWR(self):
        mass = self.getMass()
        weight = mass * 9.81

        if mass <= 0:
            return 0

        return self.getThrust() / weight

    def getThrustVec(self):
        thrust = self.getThrust()

        return pygame.Vector2(0, -thrust)

    def burnFuel(self, dT):
        for buildPart in self.parts:
            part = buildPart.part

            if not hasattr(part, "fuelNeeded"):
                continue

            fuelNeeded = part.fuelNeeded(dT)

            for tankBuildPart in self.parts:
                tank = tankBuildPart.part

                if not hasattr(tank, "consumeFuel"):
                    continue

                fuelUsed = tank.consumeFuel(fuelNeeded)
                fuelNeeded -= fuelUsed

                if fuelNeeded <= 0:
                    break

    def updateMass(self):
        self.physicsBody.mass = self.getMass()

    def updatePositions(self):
        if len(self.parts) == 0:
            return
        origin = self.parts[0]

        for buildPart in self.parts:
            buildPart.localPos = pygame.Vector2(buildPart.x - origin.x, buildPart.y - origin.y)