import math
import pygame
import sys
from components.body import Rectangle, Circle
from components.scene import Scene
from components.variables import *

# You can check and change every variables and constants through components/variables.py.
# If you want to modify some variables, please modify components/variables.py.

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Physics Engine")
scene = Scene([])

ball_1 = Circle(
    x = BALL_1_X,
    y = BALL_1_Y,
    radius = BALL_1_R,
    mass = BALL_1_M,
    name = "Ball_1"
)

ball_2 = Circle(
    x = BALL_2_X,
    y = BALL_2_Y,
    radius = BALL_2_R,
    mass = BALL_2_M,
    name = "Ball_2"
)

wall_U = Rectangle(
    x = WALL_U_X,
    y = WALL_U_Y,
    width = WALL_U_W,
    height = WALL_U_H
)

wall_L = Rectangle(
    x = WALL_L_X,
    y = WALL_L_Y,
    width = WALL_L_W,
    height = WALL_L_H
)

wall_D = Rectangle(
    x = WALL_D_X,
    y = WALL_D_Y,
    width = WALL_D_W,
    height = WALL_D_H
)

wall_R = Rectangle(
    x = WALL_R_X,
    y = WALL_R_Y,
    width = WALL_R_W,
    height = WALL_R_H
)

def calculate_drag_force(velocity, radius):
    area = math.pi * (radius ** 2)
    drag_force = 0.5 * RHO * CD * area * (velocity ** 2)
    return -math.copysign(drag_force, velocity)

def game():
    scene.bodies = [
        ball_1,
        ball_2,
        wall_U,
        wall_L,
        wall_D,
        wall_R
    ]

    scene.bodies[0].velocity[0] = BALL_1_VX
    scene.bodies[0].velocity[1] = BALL_1_VY
    scene.bodies[1].velocity[0] = BALL_2_VX
    scene.bodies[1].velocity[1] = BALL_2_VY
    dt = 1 / FPS

    is_game_running = False

    while True:
        # ==================== EVENT HANDLING ==================== #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_game_running = not is_game_running

        # ==================== CALCULATE ==================== #

        if is_game_running:
            for ball in [ball_1, ball_2]:
                radius = ball.radius
                vx = ball.velocity[0]
                vy = ball.velocity[1]

                drag_x = calculate_drag_force(vx, radius)
                drag_y = calculate_drag_force(vy, radius)

                ball.velocity[1] += (G + drag_y / ball.mass) * dt
                ball.velocity[0] += drag_x / ball.mass * dt

                # ball.velocity[1] += G * dt # Ignore Air Resistance

            collided_info = scene.step(dt)
            collided_walls_1 = collided_info[0]
            collided_walls_2 = collided_info[1]
            collided_balls = collided_info[2]

            # Check vertical Collision_1
            if 2 in collided_walls_1 or 4 in collided_walls_1:
                if 2 in collided_walls_1:
                    scene.bodies[0].center[1] = HEIGHT - scene.bodies[0].radius - WALL
                elif 4 in collided_walls_1:
                    scene.bodies[0].center[1] = scene.bodies[0].radius + WALL
                scene.bodies[0].velocity[1] *= -COR

            # Check horizontal Collision_1
            if 3 in collided_walls_1 or 5 in collided_walls_1:
                if 3 in collided_walls_1:
                    scene.bodies[0].center[0] = scene.bodies[0].radius + WALL
                elif 5 in collided_walls_1:
                    scene.bodies[0].center[0] = WIDTH - scene.bodies[0].radius - WALL
                scene.bodies[0].velocity[0] *= -COR

            # Check vertical Collision_2
            if 2 in collided_walls_2 or 4 in collided_walls_2:
                if 2 in collided_walls_2:
                    scene.bodies[1].center[1] = HEIGHT - scene.bodies[1].radius - WALL
                elif 4 in collided_walls_2:
                    scene.bodies[1].center[1] = scene.bodies[1].radius + WALL
                scene.bodies[1].velocity[1] *= -COR

            # Check horizontal Collision_2
            if 3 in collided_walls_2 or 5 in collided_walls_2:
                if 3 in collided_walls_2:
                    scene.bodies[1].center[0] = scene.bodies[1].radius + WALL
                elif 5 in collided_walls_2:
                    scene.bodies[1].center[0] = WIDTH - scene.bodies[1].radius - WALL
                scene.bodies[1].velocity[0] *= -COR

            # Check ball Collision
            if collided_balls:
                dx = ball_2.center[0] - ball_1.center[0]
                dy = ball_2.center[1] - ball_1.center[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance != 0:
                    nx = dx / distance
                    ny = dy / distance

                    v1n = ball_1.velocity[0] * nx + ball_1.velocity[1] * ny
                    v1t = -ball_1.velocity[0] * ny + ball_1.velocity[1] * nx
                    v2n = ball_2.velocity[0] * nx + ball_2.velocity[1] * ny
                    v2t = -ball_2.velocity[0] * ny + ball_2.velocity[1] * nx

                    m1 = ball_1.mass
                    m2 = ball_2.mass
                    u1n = ((m1 - m2) * v1n + 2 * m2 * v2n) / (m1 + m2)
                    u2n = ((m2 - m1) * v2n + 2 * m1 * v1n) / (m1 + m2)

                    ball_1.velocity[0] = u1n * nx - v1t * ny
                    ball_1.velocity[1] = u1n * ny + v1t * nx
                    ball_2.velocity[0] = u2n * nx - v2t * ny
                    ball_2.velocity[1] = u2n * ny + v2t * nx

                    overlap = ball_1.radius + ball_2.radius - distance
                    correction_factor = overlap / (m1 + m2)
                    ball_1.center[0] -= correction_factor * m2 * nx
                    ball_1.center[1] -= correction_factor * m2 * ny
                    ball_2.center[0] += correction_factor * m1 * nx
                    ball_2.center[1] += correction_factor * m1 * ny

        # ==================== DISPLAY ==================== #

        screen.fill(COLORS["white"])
        for body in scene.bodies:
            if body.name == "Ball_1":
                color = COLORS["red"]
            elif body.name == "Ball_2":
                color = COLORS["blue"]
            else:
                color = COLORS["black"]

            if body.shape_type == "Polygon":
                pygame.draw.polygon(
                    screen,
                    color,
                    [(vertex.x, HEIGHT - vertex.y) for vertex in body.get_vertices()],
                )
            elif body.shape_type == "Circle":
                pygame.draw.circle(
                    screen,
                    color,
                    (int(body.center[0]), int(HEIGHT - body.center[1])),
                    int(body.radius)
                )

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

if __name__ == '__main__':
    game()
