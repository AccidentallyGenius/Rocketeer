from Parts.Part import Part

class Fairing(Part):
    def __init__(self, name, mass, width, height, imagePath):
        super().__init__(name, mass, width, height, imagePath, topAttachment=True, bottomAttachment=True, leftAttachment=False, rightAttachment=False)