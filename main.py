import pygame

from Builder.Builder import Builder
from Builder.PartInventory import PartInventory
from Rendering.Renderer import Renderer
from Rendering.FlightRenderer import FlightRenderer
from Simulation.Flight import Flight
from Simulation.World import World

pygame.init()

WIDTH = 800
HEIGHT = 600

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
world = World(WIDTH, HEIGHT)

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
            elif event.button == 3:
                clickedPart = builder.getPartAt(event.pos[0], event.pos[1])
                if clickedPart is not None:
                    builder.removePart(clickedPart)

                    if draggedPart == clickedPart:
                        draggedPart = None
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
        elif event.type == pygame.MOUSEWHEEL:
            mouseX, mouseY = pygame.mouse.get_pos()

            if inventory.area.collidepoint(mouseX, mouseY):
                inventory.scroll(event.y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flight.launch(WIDTH / 2, HEIGHT - 100)

            elif event.key == pygame.K_j:
                flight.setRCSDirection("left", True)
            elif event.key == pygame.K_l:
                flight.setRCSDirection("right", True)
            elif event.key == pygame.K_i:
                flight.setRCSDirection("up", True)
            elif event.key == pygame.K_k:
                flight.setRCSDirection("down", True)

            elif event.key == pygame.K_w:
                flight.engineActive = not flight.engineActive
            elif event.key == pygame.K_a:
                builder.rocket.physicsBody.angVelo = -60
            elif event.key == pygame.K_d:
                builder.rocket.physicsBody.angVelo = 60

            if event.key == pygame.K_f and draggedPart is not None:
                draggedPart.flipHorizontal()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                flight.setRCSDirection("left", False)
            elif event.key == pygame.K_l:
                flight.setRCSDirection("right", False)
            elif event.key == pygame.K_i:
                flight.setRCSDirection("up", False)
            elif event.key == pygame.K_k:
                flight.setRCSDirection("down", False)

            elif event.key == pygame.K_d or event.key == pygame.K_a:
                builder.rocket.physicsBody.angVelo = 0

    screen.fill((24, 71, 147))


    if flight.running:
        dT = clock.get_time() / 1000
        flight.update(dT)
        world.updateCamera(builder.rocket)
        world.draw(screen, world.camera)
        flightRenderer.drawRocket(builder.rocket, world.camera)
    else:
        renderer.drawInventory(inventory)
        renderer.drawBuildArea(builder)

    renderer.drawRocketStats(builder.rocket)

    if draggedPart is not None:
        renderer.drawPart(draggedPart)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()