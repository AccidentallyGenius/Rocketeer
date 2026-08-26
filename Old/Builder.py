from Rocket import Rocket
from Parts.DraggablePart import DraggablePart
from Parts.Engine import Engine
from Parts.FuelTank import FuelTank
from Parts.NoseCone import NoseCone

class Builder:
    def __init__(self):
        self.rocket = Rocket(700, 600)
        self.availableParts = [
            DraggablePart("Engine", "Images/Engine.png", 100, 180),
            DraggablePart("Fuel Tank", "Images/FuelTank.png", 100, 300),
            DraggablePart("Nose Cone", "Images/NoseCone.png", 100, 420)
        ]

    def createEngine(self):
        if len(self.rocket.parts) != 0:
            return

        engine = Engine("Engine", 100, 2, 100000, 10, "Images/Engine.png")
        self.rocket.addPart(engine)

    def createFuelTank(self):
        if len(self.rocket.parts) == 0:
            return
        if isinstance(self.rocket.parts[-1], NoseCone):
            return

        fuelTank = FuelTank("Tank", 500, 5, 2000, "Images/FuelTank.png")
        self.rocket.addPart(fuelTank)

    def createNoseCone(self):
        if len(self.rocket.parts) == 0:
            return
        if isinstance(self.rocket.parts[-1], NoseCone):
            return

        noseCone = NoseCone("Nose Cone", 100, 2, "images/NoseCone.png")
        self.rocket.addPart(noseCone)

    def removeLastPart(self):
        if self.rocket.parts:
            self.rocket.parts.pop()

    def handleEvent(self, event):
        for part in self.availableParts:
            part.handleEvent(event)