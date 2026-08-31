import pygame

from Rocket.Attachment import Attachment
from Simulation.PhysicsBody import PhysicsBody

class Rocket:
    def __init__(self):
        self.parts = []
        self.attachments = []
        self.rootPart = None
        self.physicsBody = PhysicsBody(0, 0, 0)
        self.origin = pygame.Vector2(0, 0)

    def addPart(self, part):
        self.parts.append(part)
        if self.rootPart is None:
            self.rootPart = part

        self.physicsBody.mass = self.getMass()

    def removePart(self, part):
        self.parts.remove(part)
        self.updateMass()

        if part == self.rootPart:
            if len(self.parts) > 0:
                self.rootPart = self.parts[0]
            else:
                self.rootPart = None

    def addAttachment(self, parent, child):
        for attachment in self.attachments:
            if attachment.parent == parent and attachment.child == child:
                return

        attachment = Attachment(parent, child)
        self.attachments.append(attachment)

    def getChildren(self, parent):
        children = []

        for attachment in self.attachments:
            if attachment.parent == parent:
                children.append(attachment.child)

        return children

    def getParent(self, child):
        for attachment in self.attachments:
            if attachment.child == child:
                return attachment.parent

        return None

    def getConnectedParts(self, startPart):
        connectedParts = []
        partsToCheck = [startPart]

        while len(partsToCheck) > 0:
            currentPart = partsToCheck.pop()
            if currentPart in connectedParts:
                continue

            connectedParts.append(currentPart)
            parent = self.getParent(currentPart)
            if parent is not None:
                partsToCheck.append(parent)

            children = self.getChildren(currentPart)
            for child in children:
                partsToCheck.append(child)

        return connectedParts

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

    def isEmpty(self):
        return len(self.parts) == 0

    def getRootPosition(self):
        if self.rootPart is None:
            return  pygame.Vector2(0, 0)

        return pygame.Vector2(self.rootPart.x, self. rootPart.y)

    def getTotalHeight(self):
        if len(self.parts) == 0:
            return 0

        top = float("inf")
        bottom = float("-inf")

        for buildPart in self.parts:
            partTop = buildPart.y - buildPart.image.get_height() / 2
            partBottom = buildPart.y + buildPart.image.get_height() / 2

            if partTop < top:
                top = partTop
            if partBottom > bottom:
                bottom = partBottom

        return bottom - top

    def getThrust(self):
        thrust = 0

        for buildPart in self.parts:
            if hasattr(buildPart.part, "thrust") and not getattr(buildPart.part, "rcs", False):
                thrust += buildPart.part.thrust

        return thrust

    def getRCSThrust(self):
        thrust = 0

        for buildPart in self.parts:
            part = buildPart.part
            if getattr(part, "rcs", False):
                thrust += buildPart.part.thrust

        return thrust

    def getEngineFuelNeeded(self, dT):
        fuelNeeded = 0

        for buildPart in self.parts:
            part = buildPart.part
            if hasattr(part, "fuelNeeded"):
                fuelNeeded += part.fuelNeeded(dT)

        return fuelNeeded

    def getRCSFuelNeeded(self, dT):
        fuelNeeded = 0

        for buildPart in self.parts:
            part = buildPart.part
            if getattr(part, "rcs", False):
                fuelNeeded += part.fuelConsumption * dT

        return fuelNeeded

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
        thrustVec = pygame.Vector2(0, -thrust)

        return thrustVec.rotate(-self.physicsBody.angVelo)

    def applyThrustPhys(self):
        body = self.physicsBody
        centerOfMass = self.getCenterOfMass()

        for buildPart in self.parts:
            part = buildPart.part
            if not  hasattr(part, "thrust"):
                continue

            thrust = part.thrust
            localPos = buildPart.localPos - centerOfMass
            localForce = pygame.Vector2(0, -thrust)

            force = localForce.rotate(body.angle)
            body.addForce(force)

            torque = (localPos.x * force.y - localPos.y * force.x)
            body.addTorque(torque)

    def getRCSVec(self, direction):
        thrust = self.getRCSThrust()

        if direction == "left":
            return pygame.Vector2(-thrust, 0)
        if direction == "right":
            return pygame.Vector2(thrust, 0)
        if direction == "down":
            return pygame.Vector2(0, thrust)
        if direction == "up":
            return pygame.Vector2(0, -thrust)

        return pygame.Vector2(0, 0)

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

    def consumeFuel(self, amount):
        remaining = amount
        for buildPart in self.parts:
            part = buildPart.part

            if not hasattr(part, "consumeFuel"):
                continue

            fuelUsed = part.consumeFuel(remaining)
            remaining -= fuelUsed

            if remaining <= 0:
                return amount
        return amount - remaining

    def updateMass(self):
        self.physicsBody.mass = self.getMass()
        self.updateMomentOfInertia()

    def updatePositions(self):
        if len(self.parts) == 0:
            return
        origin = self.rootPart

        for buildPart in self.parts:
            buildPart.localPos = pygame.Vector2(buildPart.x - origin.x, buildPart.y - origin.y)

    def move(self, offset):
        for buildPart in self.parts:
            buildPart.x += offset.x
            buildPart.y += offset.y
            buildPart.rect.center = (buildPart.x, buildPart.y)

    def getCenterPos(self):
        if len(self.parts) == 0:
            return self.physicsBody.pos.copy()

        minX = float("inf")
        maxX = float("-inf")
        minY = float("inf")
        maxY = float("-inf")

        for buildPart in self.parts:
            partX = self.physicsBody.pos.x + buildPart.localPos.x
            partY = self.physicsBody.pos.y + buildPart.localPos.y
            halfWidth = buildPart.image.get_width() / 2
            halfHeight = buildPart.image.get_height() / 2

            minX = min(minX, partX - halfWidth)
            maxX = max(maxX, partX + halfWidth)
            minY = min(minY, partY - halfHeight)
            maxY = max(maxY, partY + halfHeight)

        centerX = (minX + maxX) / 2
        centerY = (minY + maxY) / 2

        return pygame.Vector2(centerX, centerY)

    def getCenterOfMass(self):
        if len(self.parts) == 0:
            return pygame.Vector2(0, 0)

        totalMass = 0
        weightedPos = pygame.Vector2(0, 0)

        for buildPart in self.parts:
            mass = buildPart.part.mass
            if hasattr(buildPart.part, "getFuelMass"):
                mass += buildPart.part.getFuelMass()

            totalMass += mass
            weightedPos += buildPart.localPos * mass

        if totalMass == 0:
            return pygame.Vector2(0, 0)

        return weightedPos / totalMass

    def updateMomentOfInertia(self):
        inertia = 0
        centerOfMass = self.getCenterOfMass()

        for buildPart in self.parts:
            mass = buildPart.part.mass
            if hasattr(buildPart.part, "getFuelMass"):
                mass += buildPart.part.getFuelMass()

            dist = buildPart.localPos.distance_to(centerOfMass)
            inertia += mass * dist ** 2
        self.physicsBody.momentOfInertia = max(inertia, 1)

    def getGroundTorque(self, groundY):
        body = self.physicsBody
        centerOfMass = self.getCenterOfMass()
        lowestPart = None
        lowestY = float("-inf")

        for buildPart in self.parts:
            rotatedLocalPos = buildPart.localPos.rotate(body.angle)
            partY = body.pos.y + rotatedLocalPos.y
            halfHeight = buildPart.image.get_height() / 2
            bottomY = partY + halfHeight

            if bottomY > lowestY:
                lowestY = bottomY
                lowestPart = buildPart

        if lowestPart is None:
            return 0
        if lowestY < groundY:
            return 0

        contactLocal = lowestPart.localPos.rotate(body.angle)
        contactLocal -= centerOfMass.rotate(body.angle)
        groundForce = pygame.Vector2(0, -body.mass * 9.81)
        torque = (contactLocal.x * groundForce.y - contactLocal.y * groundForce.x)

        return torque