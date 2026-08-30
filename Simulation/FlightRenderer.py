import pygame

class FlightRenderer:
    def __init__(self, screen):
        self.screen = screen

    def drawRocket(self, rocket):
        pos = rocket.physicsBody.pos

        for buildPart in rocket.parts:
            localPos = buildPart.localPos

            x = pos.x + localPos.x
            y = pos.y + localPos.y

            rect = buildPart.image.get_rect(center=(x, y))
            self.screen.blit(buildPart.image, rect)

    def drawGround(self):
        pygame.draw.line(self.screen, (100, 100, 100), (0, 600), (1200, 600), 3)