import pygame

from Builder import Builder
from Renderers.RocketRenderer import RocketRenderer
from Renderers.StatsRenderer import StatsRenderer

pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocketeer")

clock = pygame.time.Clock()

builder = Builder()
rocketRenderer = RocketRenderer(screen)
statsRenderer = StatsRenderer(screen)

gameLoop = True
event = None

while gameLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False

    screen.fill((0, 0, 0))
    rocketRenderer.drawRocket(builder.rocket)
    rocketRenderer.drawPartsPanel(builder)
    statsRenderer.drawStats(builder.rocket)
    statsRenderer.drawControls()
    builder.handleEvent(event)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()