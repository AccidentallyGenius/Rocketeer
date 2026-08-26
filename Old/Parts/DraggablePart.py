import pygame

class DraggablePart:
    def __init__(self, partType, imagePath, x, y):
        self.partType = partType
        self.image = pygame.image.load(imagePath)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.startX = x
        self.startY = y
        self.dragging = False
        self.offsetX = 0
        self.offsetY = 0

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.dragging = True
                self.offsetX = self.rect.x - event.pos[0]
                self.offsetY = self.rect.y - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.rect.x = event.pos[0] - self.offsetX
                self.rect.y = event.pos[1] - self.offsetY