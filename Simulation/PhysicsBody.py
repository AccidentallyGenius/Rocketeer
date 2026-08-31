import pygame

class PhysicsBody:
    def __init__(self, x, y, mass):
        self.pos = pygame.Vector2(x, y)
        self.velo = pygame.Vector2(0, 0)
        self.accl = pygame.Vector2(0, 0)
        self.mass = mass
        self.force = pygame.Vector2(0, 0)
        self.angle = 0
        self.angVelo = 0
        self.torque = 0
        self.momentOfInertia = 1

    def addForce(self, force):
        self.force += force

    def clearForce(self):
        self.force = pygame.Vector2(0, 0)

    def addTorque(self, torque):
        self.torque += torque

    def clearTorque(self):
        self.torque = 0