class Rocket:
    def __init__(self, x, y):
        self.parts = []

    def addPart(self, part):
        self.parts.append(part)