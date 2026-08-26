class Rocket:
    def __init__(self):
        self.parts = []

    def addPart(self, part):
        self.parts.append(part)

    def removePart(self, part):
        self.parts.remove(part)