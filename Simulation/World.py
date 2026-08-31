import pygame

class World:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.width = 5000
        self.height = 5000
        self.camera = pygame.Vector2(0, 0)

        self.groundY = screenHeight - 50
        self.skyColor = (130, 200, 229)
        self.groundColor = (65, 65, 65)

    def draw(self, screen, camera):
        screen.fill(self.skyColor)
        screenGroundY = self.groundY - camera.y
        pygame.draw.rect(screen, self.groundColor, (0, screenGroundY, self.screenWidth, self.screenHeight - screenGroundY))

    def updateCamera(self, rocket):
        rocketCenter = rocket.getCenterPos()
        self.camera.y = rocketCenter.y - self.screenHeight / 2
        self.camera.x = rocketCenter.x - self.screenWidth / 2