import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)

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

    def drawRocketStats(self, rocket):
        mass = rocket.getMass()
        fuelMass = rocket.getFuelMass()
        thrust = rocket.getThrust()
        twr = rocket.getTWR()

        massText = self.font.render(f"Mass: {mass:.1f}kg", True, (255, 255, 255))
        fuelMassText = self.font.render(f"Fuel Mass: {fuelMass:.1f}kg", True, (255, 255, 255))
        thrustText = self.font.render(f"Thrust: {thrust:.1f}N", True, (255, 255, 255))
        TWRText = self.font.render(f"TWR: {twr:.1f}", True, (255, 255, 255))

        self.screen.blit(massText, (1050, 20))
        self.screen.blit(fuelMassText, (1050, 50))
        self.screen.blit(thrustText, (1050, 80))
        self.screen.blit(TWRText, (1050, 110))