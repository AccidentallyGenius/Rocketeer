import pygame
from Rocket.Rocket import Rocket

class Builder:
    def __init__(self):
        self.rocket = Rocket()
        self.buildArea = pygame.Rect(200, 25, 400, 550)
        self.placedParts = []

    def addPart(self, buildPart):
        if not self.isInsideBuildArea(buildPart):
            return False

        if buildPart in self.placedParts:
            return False


        snap = self.findSnap(buildPart)
        if snap is not None:
            self.applySnap(buildPart, snap)
            snapPos, side, placedPart = snap
            self.rocket.addAttachment(placedPart, buildPart)

        self.placedParts.append(buildPart)
        self.rocket.addPart(buildPart)
        self.rocket.updatePositions()
        self.rocket.updateMomentOfInertia()

        return True

    def removePart(self, buildPart):
        if buildPart not in self.placedParts:
            return False

        self.rocket.removePartAttachments(buildPart)
        self.placedParts.remove(buildPart)
        self.rocket.removePart(buildPart)
        self.rocket.updateMomentOfInertia()

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

    def canSideAttach(self, parent, child):
        if parent.getLeftPoint() is None and parent.getRightPoint() is None:
            return False
        if child.getLeftPoint() is None and parent.getRightPoint() is None:
            return False

        return True

    def findSnap(self, buildPart):
        SNAP_DISTANCE = 15
        closestSnap = None
        closestDistance = SNAP_DISTANCE

        for placedPart in self.placedParts:
            if placedPart == buildPart:
                continue

            parentPoint = placedPart.getBottomPoint()
            childPoint = buildPart.getTopPoint()

            if parentPoint is not None and childPoint is not None:
                distance = parentPoint.distance_to(childPoint)

                if distance <= closestDistance:
                    closestSnap = distance
                    closestSnap = parentPoint, "top", placedPart

            parentPoint = placedPart.getTopPoint()
            childPoint = buildPart.getBottomPoint()

            if parentPoint is not None and childPoint is not None:
                distance = parentPoint.distance_to(childPoint)

                if distance <= closestDistance:
                    closestDistance = distance
                    closestSnap = parentPoint, "bottom", placedPart

            if not self.canSideAttach(placedPart, buildPart):
                continue

            parentPoint = placedPart.getLeftPoint()
            childPoint = buildPart.getRightPoint()

            if parentPoint is not None and childPoint is not None:
                distance = parentPoint.distance_to(childPoint)

                if distance <= closestDistance:
                    closestDistance = distance
                    closestSnap = parentPoint, "right", placedPart

            parentPoint = placedPart.getRightPoint()
            childPoint = buildPart.getLeftPoint()

            if parentPoint is not None and childPoint is not None:
                distance = parentPoint.distance_to(childPoint)

                if distance <= closestDistance:
                    closestDistance = distance
                    closestSnap = parentPoint, "left", placedPart

        return closestSnap

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
        elif side == "left":
            attachment = buildPart.getLeftPoint()
        elif side == "right":
            attachment = buildPart.getRightPoint()
        else:
            return None

        if attachment is None:
            return False

        offset = snapPos - attachment
        buildPart.x += offset.x
        buildPart.y += offset.y
        buildPart.rect.center = (buildPart.x, buildPart.y)

        return

    # def attachmentOccupied(self, placedPart, side):
    #     for attachment in self.rocket.attachments:
    #         if attachment.parent != placedPart:
    #             continue
    #
    #         if side == "top" and attachment.child.getBottomPoint() is not None:
    #             return True
    #         if side == "bottom" and attachment.child.getTopPoint() is not None:
    #             return True
    #         if side == "left" and attachment.child.getRightPoint() is not None:
    #             return True
    #         if side == "right" and attachment.child.getLeftPoint() is not None:
    #             return True
    #
    #     return True