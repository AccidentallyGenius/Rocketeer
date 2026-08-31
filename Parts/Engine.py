from Parts.Part import Part

class Engine(Part):
    def __init__(self, name, mass, width, height, thrust, fuelConsumption, imagePath, rcs=False):
        super().__init__(name, mass, width, height, imagePath, topAttachment=not rcs, bottomAttachment=False, leftAttachment=rcs, rightAttachment=rcs)

        self.thrust = thrust
        self.fuelConsumption = fuelConsumption
        self.rcs = rcs

    def fuelNeeded(self, dT):
        return self.fuelConsumption * dT