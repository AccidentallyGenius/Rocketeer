from Parts.Part import Part

class Engine(Part):
    def __init__(self, name, mass, width, height, thrust, fuelConsumption, imagePath):
        super().__init__(name, mass, width, height, imagePath)

        self.thrust = thrust
        self.fuelConsumption = fuelConsumption