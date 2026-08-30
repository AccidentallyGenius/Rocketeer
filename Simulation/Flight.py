import pygame
from Simulation.Physics import applyGravity, applyThrust, updateBody

class Flight:
    def __init__(self, rocket):
        self.rocket = rocket
        self.running = False

    def launch(self, x ,y):
        self.rocket.physicsBody.pos = pygame.Vector2(x, y)
        self.rocket.physicsBody.velo = pygame.Vector2(0, 0)
        self.rocket.updateMass()
        self.running = True

    def update(self, dt):
        if not self.running:
            return

        body = self.rocket.physicsBody
        body.clearForces()
        applyGravity(body)
        thrust = self.rocket.getThrustVec()
        applyThrust(body, thrust)
        updateBody(body, dt)