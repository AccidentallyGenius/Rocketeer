import pygame

GRAVITY = 9.81

def applyGravity(body):
    gravity = pygame.Vector2(0, body.mass * GRAVITY)
    body.addForce(gravity)

def applyThrust(body, thrust):
    body.addForce(thrust)

def updateBody(body, dT):
    if body.mass > 0:
        body.accl = body.force / body.mass
    else:
        body.accl = pygame.Vector2(0, 0)

    body.velo += body.accl * dT
    body.pos += body.velo * dT

    if body.momentOfInertia > 0:
        angAccl = body.torque / body.momentOfInertia
    else:
        angAccl = 0

    body.angVelo += angAccl * dT
    body.angVelo *= 0.98
    body.angle += body.angVelo * dT
    body.clearForce()
    body.clearTorque()