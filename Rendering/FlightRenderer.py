import pygame.transform

class FlightRenderer:
    def __init__(self, screen):
        self.screen = screen

    def drawRocket(self, rocket, camera):
        body = rocket.physicsBody

        for buildPart in rocket.parts:
            localPos = buildPart.localPos
            rotatedLocalPos = localPos.rotate(body.angle)
            worldPos = body.pos + rotatedLocalPos
            screenPos = worldPos - camera
            rotatedImage = pygame.transform.rotate(buildPart.image, -body.angle)
            rect = rotatedImage.get_rect(center=screenPos)

            self.screen.blit(rotatedImage, rect)