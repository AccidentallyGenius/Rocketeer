import pygame

class StatsRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 30)

    def drawStats(self, rocket):
        mass = rocket.getMass()
        thrust = rocket.getThrust()
        TWR = rocket.getTWR()
        parts = len(rocket.parts)

        massText = self.font.render(f"Mass: {mass:.1f}kg", True, (255, 255, 255))
        thrustText = self.font.render(f"Thrust: {thrust:.1f}N", True, (255, 255, 255))
        TWRText = self.font.render(f"Thrust:Weight: {TWR:.1f}", True, (255, 255, 255))
        partsText = self.font.render(f"Parts: {parts}", True, (255, 255, 255))

        self.screen.blit(massText, (20, 20))
        self.screen.blit(thrustText, (20, 50))
        self.screen.blit(TWRText, (20, 80))
        self.screen.blit(partsText, (20, 110))

    def drawControls(self):
        controls = [
            "ROCKET BUILDER",
            "",
            "[1] Add Engine",
            "[2] Add Fuel Tank",
            "[3] Add Nose Cone",
            "[Backspace] Remove Part",
        ]

        y = 500

        for control in controls:
            textSurface = self.font.render(control, True, (255, 255, 255))
            self.screen.blit(textSurface, (20, y))
            y += 30