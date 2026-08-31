import pygame.image

from Parts.Engine import Engine
from Parts.NoseCone import NoseCone
from Parts.FuelTank import FuelTank
from Parts.Fairing import Fairing
from Builder.BuildPart import BuildPart

class PartInventory:
    def __init__(self):
        self.parts = [Engine("Large Engine", 100, 100, 100, 1000000, 10, "Images/Engines/LargeEngine.png"),
                      Engine("Small Engine", 75, 100, 100, 500000, 8, "Images/Engines/SmallEngine.png"),
                      Engine("RCS Engine", 15, 100, 100, 50000, 2, "Images/Engines/RCSEngine.png", True),
                      FuelTank("Small Fuel Tank", 500, 100, 200, 2000, "Images/FuelTanks/SmallFuelTank.png"),
                      FuelTank("Large Fuel Tank", 800, 100, 200, 4000, "Images/FuelTanks/LargeFuelTank.png"),
                      FuelTank("Wide Small Fuel Tank", 1200, 100, 200, 2000, "Images/FuelTanks/WideSmallFuelTank.png"),
                      FuelTank("Wide Large Fuel Tank", 1500, 100, 200, 4000, "Images/FuelTanks/WideLargeFuelTank.png"),
                      Fairing("Fairing", 150, 100, 150, "Images/Fairing.png"),
                      NoseCone("Capsule", 100, 100, 100, "Images/NoseCones/NoseCone.png")
                      ]
        self.categories = ["All", "Engine", "Fuel Tanks", "Capsules"]
        self.selectedCategories = "All"

        self.rects = []
        self.images = []


        self.area = pygame.Rect(40, 25, 115, 550)
        self.scrollOffset = 0
        self.scrollSpeed = 30

        self.updateRects()

    def updateRects(self):
        self.rects = []
        self.images = []

        x = 98
        y = 100 + self.scrollOffset

        for part in self.parts:
            image = pygame.transform.smoothscale_by(pygame.image.load(part.imagePath).convert_alpha(), 0.75)
            rect = image.get_rect(center=(x, y))

            self.images.append(image)
            self.rects.append(rect)
            y += 120

    def handleMouseDown(self, mouseX, mouseY):
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(mouseX, mouseY):
                part = self.parts[i]
                return BuildPart(part, mouseX, mouseY)

        return None

    def scroll(self, amount):
        self.scrollOffset += amount * self.scrollSpeed
        if self.scrollOffset > 0:
            self.scrollOffset = 0

        maxScroll = -(len(self.parts) * 120 - 550)
        if self.scrollOffset < maxScroll:
            self.scrollOffset = maxScroll

        self.updateRects()