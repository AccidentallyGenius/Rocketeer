import pygame

class BuildPart:
    def __init__(self, part, x, y):
        self.part = part

        self.x = x
        self.y = y

        self.image = pygame.transform.smoothscale_by(pygame.image.load(part.imagePath).convert_alpha(), 0.5)
        self.rect = self.image.get_rect(center=(x, y))
        self.flipped = False

        self.dragging = False
        self.offsetX = 0
        self.offsetY = 0
        self.localPos = pygame.Vector2(0, 0)

    def containsPoint(self, mouseX, mouseY):
        return self.rect.collidepoint(mouseX, mouseY)

    def startDrag(self, mouseX, mouseY):
        self.dragging = True

        self.offsetX = self.x - mouseX
        self.offsetY = self.y - mouseY

    def drag(self, mouseX, mouseY):
        if self.dragging:
            self.x = mouseX + self.offsetX
            self.y = mouseY + self.offsetY

            self.rect.center = (self.x, self.y)

    def stopDrag(self):
        self.dragging = False

    def getTopPoint(self):
        if not self.part.topAttachment:
            return None

        return pygame.Vector2(self.x, self.y - self.image.get_height() / 2)

    def getBottomPoint(self):
        if not self.part.bottomAttachment:
            return None

        return pygame.Vector2(self.x, self.y + self.image.get_height() / 2)

    def getLeftPoint(self):
        if not self.part.leftAttachment:
            return None

        return pygame.Vector2(self.x - self.image.get_width() / 2, self.y)

    def getRightPoint(self):
        if not self.part.rightAttachment:
            return None

        return pygame.Vector2(self.x + self.image.get_width() / 2, self.y)

    def flipHorizontal(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.flipped = not self.flipped