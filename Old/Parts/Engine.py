from Old.Parts.Part import Part

class Engine(Part):
    def __init__(self, name, mass, height, thrust, fuelConsumption, imagePath):
        super().__init__(name, mass, height, imagePath)
        self.thrust = thrust
        self.fuelConsumption = fuelConsumption