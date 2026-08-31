import pygame
from Simulation.Physics import applyGravity, applyThrust, updateBody

class Flight:
    def __init__(self, rocket):
        self.rocket = rocket
        self.running = False
        self.engineActive = False
        self.rcsDirections = {"left": False,
                              "right": False,
                              "up": False,
                              "down": False
                              }

    def launch(self, x ,y):
        self.rocket.physicsBody.pos = pygame.Vector2(x, y)
        self.rocket.physicsBody.velo = pygame.Vector2(0, 0)
        self.rocket.updateMass()
        self.running = True

    def setRCSDirection(self, direction, active):
        if direction in self.rcsDirections:
            self.rcsDirections[direction] = active

    def update(self, dt):
        if not self.running:
            return

        GROUND_Y = 515
        body = self.rocket.physicsBody
        body.clearForce()
        applyGravity(body)
        groundTorque = self.rocket.getGroundTorque(GROUND_Y)
        body.addTorque(groundTorque)

        if self.engineActive:
            fuelNeeded = self.rocket.getEngineFuelNeeded(dt)
            fuelUsed = self.rocket.consumeFuel(fuelNeeded)

            if fuelUsed > 0:
                self.rocket.applyThrustPhys()

        for direction, active in self.rcsDirections.items():
            if active:
                fuelNeeded = self.rocket.getRCSFuelNeeded(direction, dt)
                fuelUsed = self.rocket.consumeFuel(fuelNeeded)
                if fuelUsed > 0:
                    rcsForce = self.rocket.getRCSVec(direction)
                    applyThrust(body, rcsForce)

        updateBody(body, dt)

        if body.pos.y >= GROUND_Y:
            body.pos.y = GROUND_Y
            body.velo.y = 0