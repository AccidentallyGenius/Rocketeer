import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def drawPart(self, buildPart):
        self.screen.blit(buildPart.image, buildPart.rect)

    def drawInventory(self, inventory):
        for part, rect in zip(inventory.parts, inventory.rects):
            image = pygame.image.load(part.imagePath).convert_alpha()

            self.screen.blit(image, rect)

    def drawBuildArea(self, builder):
        pygame.draw.rect(self.screen, (60, 60, 60), builder.buildArea, 2)

        for buildPart in builder.placedParts:
            self.drawPart(buildPart)