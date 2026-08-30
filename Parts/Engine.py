from Parts.Part import Part

class Engine(Part):
    def __init__(self, name, mass, width, height, thrust, fuelConsumption, imagePath):
        super().__init__(name, mass, width, height, imagePath, topAttachment=True, bottomAttachment=False)

        self.thrust = thrust
        self.fuelConsumption = fuelConsumption

    def fuelNeeded(self, dT):
        return self.fuelConsumption * dT