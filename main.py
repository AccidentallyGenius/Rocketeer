import pygame

from Builder.Builder import Builder
from Builder.PartInventory import PartInventory
from Rendering.Renderer import Renderer
from Simulation.Flight import Flight
from Simulation.FlightRenderer import FlightRenderer


pygame.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ROCKETEER")
clock = pygame.time.Clock()
running = True
draggedPart = None

builder = Builder()
flight = Flight(builder.rocket)
flightRenderer = FlightRenderer(screen)
renderer = Renderer(screen)
inventory = PartInventory()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                draggedPart = builder.getPartAt(event.pos[0], event.pos[1])

                if draggedPart is None:
                    draggedPart = inventory.handleMouseDown(event.pos[0], event.pos[1])

                if draggedPart is not None:
                    draggedPart.startDrag(event.pos[0], event.pos[1])

                    if draggedPart in builder.placedParts:
                        builder.removePart(draggedPart)
        elif event.type == pygame.MOUSEMOTION:
            if draggedPart is not None:
                draggedPart.drag(event.pos[0], event.pos[1])
                snap = builder.findSnap(draggedPart)

                if snap is not None:
                    builder.applySnap(draggedPart, snap)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if draggedPart is not None:
                    draggedPart.stopDrag()

                    if builder.isInsideBuildArea(draggedPart):
                        builder.addPart(draggedPart)

                    draggedPart = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flight.launch(750, 540)

    screen.fill((30, 30, 30))

    if flight.running:
        flightRenderer.drawGround()
        flightRenderer.drawRocket(builder.rocket)
    else:
        renderer.drawInventory(inventory)
        renderer.drawBuildArea(builder)

    renderer.drawRocketStats(builder.rocket)

    if draggedPart is not None:
        renderer.drawPart(draggedPart)

    dT = clock.get_time() / 1000
    pygame.display.flip()
    clock.tick(60)

pygame.quit()