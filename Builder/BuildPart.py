import pygame

class BuildPart:
    def __init__(self, part, x, y):
        self.part = part

        self.x = x
        self.y = y
        self.rotation = 0

        self.image = pygame.image.load(part.imagePath).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        self.dragging = False
        self.offsetX = 0
        self.offsetY = 0

    def containsPoint(self, mouseX, mouseY):
        return self.rect.collidepoint(mouseX, mouseY)

    def startDrag(self, mouseX, mouseY):
        self.dragging = True

        self.x = mouseX + self.offsetX
        self.y = mouseY + self.offsetY

    def drag(self, mouseX, mouseY):
        if self.dragging:
            self.x = mouseX + self.offsetX
            self.y = mouseY + self.offsetY

            self.rect.center = (self.x, self.y)

    def stopDrag(self):
        self.dragging = False

    def getTopPoint(self):
        return self.x, self.rect.top

    def getBottomPoint(self):
        return self.x, self.rect.bottom