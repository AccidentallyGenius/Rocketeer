class Part:
    def __init__(self, name, mass, width, height, imagePath, topAttachment=True, bottomAttachment=True, leftAttachment=False, rightAttachment=False):
        self.name = name
        self.mass = mass
        self.width = width
        self.height = height
        self.imagePath = imagePath
        self.topAttachment = topAttachment
        self.bottomAttachment = bottomAttachment
        self.leftAttachment = leftAttachment
        self.rightAttachment = rightAttachment