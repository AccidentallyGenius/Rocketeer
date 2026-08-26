class Rocket:
    def __init__(self, x, y):
        self.parts = []
        self.x = x
        self.y = y

    def addPart(self, part):
        self.parts.append(part)

    def getMass(self):
        mass = 0

        for part in self.parts:
            mass += part.mass

            if hasattr(part, "getFuelMass"):
                mass += part.getFuelMass()

        return mass

    def getHeight(self):
        height = 0

        for part in self.parts:
            height += part.height

        return height


    def getThrust(self):
        thrust = 0

        for part in self.parts:
            if hasattr(part, "thrust"):
                thrust += part.thrust

        return thrust

    def getTWR(self):
        thrust = self.getThrust()
        mass = self.getMass()
        GRAVITY = 9.81

        if mass <= 0:
            return 0

        TWR = thrust / (mass * GRAVITY)

        return TWR

    def burnFuel(self, dT):
        for part in self.parts:
            if hasattr(part, "FUEL_CONSUMPTION"):
                fuelNeeded = part.FUEL_CONSUMPTION * dT

                for tank in self.parts:
                    if hasattr(tank, "consumeFuel"):
                        fuelUsed = tank.consumeFuel(fuelNeeded)

                        if fuelUsed == fuelNeeded:
                            break