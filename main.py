import pygame

from Builder.Builder import Builder
from Builder.PartInventory import PartInventory
from Rendering.Renderer import Renderer


pygame.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ROCKETEER")
clock = pygame.time.Clock()
running = True
draggedPart = None

builder = Builder()
renderer = Renderer(screen)
inventory = PartInventory()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                draggedPart = inventory.handleMouseDown(event.pos[0], event.pos[1])

                if draggedPart is not None:
                    draggedPart.startDrag(event.pos[0], event.pos[1])
        elif event.type == pygame.MOUSEMOTION:
            if draggedPart is not None:
                draggedPart.drag(event.pos[0], event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if draggedPart is not None:
                    draggedPart.stopDrag()

                    if builder.isInsideBuildArea(draggedPart):
                        builder.addPart(draggedPart)

                    draggedPart = None

    screen.fill((30, 30, 30))

    renderer.drawInventory(inventory)
    renderer.drawBuildArea(builder)

    if draggedPart is not None:
        renderer.drawPart(draggedPart)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()