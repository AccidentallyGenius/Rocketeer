import pygame
from Rocket.Rocket import Rocket

class Builder:
    def __init__(self):
        self.rocket = Rocket()
        self.buildArea = pygame.Rect(200, 50, 900, 600)
        self.placedParts = []

    def addPart(self, buildPart):
        self.snapPart(buildPart)
        self.placedParts.append(buildPart)

    def isInsideBuildArea(self, buildPart):
        return self.buildArea.collidepoint(buildPart.x, buildPart.y)

    def snapPart(self, buildPart):
        SNAP_DISTANCE = 30

        for placedPart in self.placedParts:
            topX, topY = placedPart.getTopPoint()
            bottomX, bottomY = placedPart.getBottomPoint()

            newX, newY = buildPart.getTopPoint()

            distX = abs(newX - bottomX)
            distY = abs(newY - bottomY)

            if distX < SNAP_DISTANCE and distY < SNAP_DISTANCE:
                buildPart.x = bottomX
                buildPart.y = bottomY - buildPart.rect.height / 2
                buildPart.rect.center = (buildPart.x, buildPart.y)

                return True
        return False