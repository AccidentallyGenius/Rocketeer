from Parts.Part import Part

class FuelTank(Part):
    FUEL_DENSITY = 0.8

    def __init__(self, name, mass, width, height, fuelCapacity, imagePath):
        super().__init__(name, mass, width, height, imagePath, topAttachment=True, bottomAttachment=True, leftAttachment=True, rightAttachment=True)

        self.fuelCapacity = fuelCapacity
        self.fuel = fuelCapacity

    def getFuelMass(self):
        return self.fuel * self.FUEL_DENSITY

    def consumeFuel(self, amount):
        fuelUsed = min(self.fuel, amount)
        self.fuel -= fuelUsed

        return fuelUsed