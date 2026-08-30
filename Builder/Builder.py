import pygame
from Rocket.Rocket import Rocket

class Builder:
    def __init__(self):
        self.rocket = Rocket()
        self.buildArea = pygame.Rect(200, 50, 800, 600)
        self.placedParts = []

    def addPart(self, buildPart):
        if not self.isInsideBuildArea(buildPart):
            return False

        snap = self.findSnap(buildPart)
        if snap is not None:
            self.applySnap(buildPart, snap)
            snapPos, side, placedPart = snap
            self.rocket.addAttachment(placedPart, buildPart)

        self.placedParts.append(buildPart)
        self.rocket.addPart(buildPart)
        self.rocket.updatePositions()

        return True

    def removePart(self, buildPart):
        if buildPart not in self.placedParts:
            return False

        self.placedParts.remove(buildPart)
        self.rocket.removePart(buildPart)
        self.rocket.removePartAttachments(buildPart)

        return True

    def isInsideBuildArea(self, buildPart):
        return self.buildArea.collidepoint(buildPart.x, buildPart.y)

    def getPartAt(self, mouseX, mouseY):
        for buildPart in reversed(self.placedParts):
            if buildPart.containsPoint(mouseX, mouseY):
                return buildPart

        return None

    def canAttach(self, parent, child):
        if parent.getBottomPoint() is None:
            return False
        if child.getTopPoint() is None:
            return False

        return True

    def findSnap(self, buildPart):
        SNAP_DISTANCE = 50

        for placedPart in self.placedParts:
            if placedPart == buildPart:
                continue

            parentPoint = placedPart.getBottomPoint()
            childPoint = buildPart.getTopPoint()

            if parentPoint is not None and childPoint is not None:
                if parentPoint.distance_to(childPoint) <= SNAP_DISTANCE:
                    return parentPoint, "top", placedPart

            parentPoint = placedPart.getTopPoint()
            childPoint = buildPart.getBottomPoint()

            if parentPoint is not None and childPoint is not None:
                if parentPoint.distance_to(childPoint) <= SNAP_DISTANCE:
                    return parentPoint, "bottom", placedPart

        return None

    def snapPart(self, buildPart):
        snap = self.findSnap(buildPart)

        if snap is None:
            return False

        self.applySnap(buildPart, snap)
        return True

    def applySnap(self, buildPart, snap):
        snapPos, side, placedPart = snap

        if side == "top":
            attachment = buildPart.getTopPoint()
        elif side == "bottom":
            attachment = buildPart.getBottomPoint()
        else:
            return None

        if attachment is None:
            return False

        offset = snapPos - attachment
        buildPart.x += offset.x
        buildPart.y += offset.y
        buildPart.rect.center = (buildPart.x, buildPart.y)

        return True