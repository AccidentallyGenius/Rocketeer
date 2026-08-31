import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.buildArea = pygame.image.load("Images/Menus/Blueprint.png").convert_alpha()

    def drawPart(self, buildPart):
        self.screen.blit(buildPart.image, buildPart.rect)

    def drawInventory(self, inventory):
        for image, rect in zip(inventory.images, inventory.rects):
            self.screen.blit(image, rect)

        pygame.draw.rect(self.screen, (255, 255, 255), (40, 25, 115, 550), 5)
        pygame.draw.rect(self.screen, (24, 71, 147), (40, 0, 115, 25))
        pygame.draw.rect(self.screen, (24, 71, 147), (40, 575, 115, 25))

        # left, top, width, height

    def drawBuildArea(self, builder):
        pygame.draw.rect(self.screen, (255, 255, 255), builder.buildArea, 2)
        self.screen.blit(self.buildArea, (205, 30))

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

        self.screen.blit(massText, (625, 20))
        self.screen.blit(fuelMassText, (625, 50))
        self.screen.blit(thrustText, (625, 80))
        self.screen.blit(TWRText, (625, 110))