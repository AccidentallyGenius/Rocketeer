class RocketRenderer:
    def __init__(self, screen):
        self.screen = screen

    def drawRocket(self, rocket):
        y = rocket.y
        x = rocket.x

        for part in rocket.parts:
            image = part.image
            self.screen.blit(image, ((x - image.get_width() / 2), y - image.get_height()))

            y -= image.get_height()

    def drawPartsPanel(self, builder):
        for part in builder.availableParts:
            self.screen.blit(part.image, part.rect)