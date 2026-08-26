import pygame

class Part:
    def __init__(self, name, mass, height, imagePath):
        self.name = name
        self.mass = mass
        self.height = height
        self.image = pygame.image.load(imagePath)