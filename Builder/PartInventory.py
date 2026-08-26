import pygame.image

from Parts.Engine import Engine
from Parts.NoseCone import NoseCone
from Parts.FuelTank import FuelTank

from Builder.BuildPart import BuildPart

class PartInventory:
    def __init__(self):
        self.parts = [Engine("Basic Engine", 100, 100, 100, 100000, 10, "Images/Engines/BasicEngine.png"),
                      FuelTank("Basic Fuel Tank", 500, 100, 200, 2000, "Images/FuelTanks/BasicFuelTank.png"),
                      NoseCone("Basic Nose Cone", 100, 100, 100, "Images/NoseCones/BasicNoseCone.png")
                      ]
        self.rects = []
        self.updateRects()

    def updateRects(self):
        self.rects = []
        x = 100
        y = 150

        for part in self.parts:
            image = pygame.image.load(part.imagePath).convert_alpha()
            rect = image.get_rect(center=(x, y))

            self.rects.append(rect)
            y += 150

    def handleMouseDown(self, mouseX, mouseY):
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(mouseX, mouseY):
                part = self.parts[i]
                return BuildPart(part, mouseX, mouseY)

        return None

