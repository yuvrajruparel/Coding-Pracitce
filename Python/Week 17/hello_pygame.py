import pygame
import random

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Day 8 — Bouncing Ball")

running = True
paused = False
clock = pygame.time.Clock()
balls = [
    {"x": 320, "y": 240, "vx": 4, "vy": 3, "color": (255, 255, 255)},
    {"x": 150, "y": 100, "vx": -3, "vy": 5, "color": (255, 255, 255)},
    {"x": 500, "y": 350, "vx": 2, "vy": -4, "color": (255, 255, 255)},
]

# creating a translucent trail
trail = pygame.Surface((640, 480))
trail.fill((20, 20, 30))
trail.set_alpha(30)

while running:
    for event in pygame.event.get():
        # Window-close button clicked
        if event.type == pygame.QUIT:
            running = False

        # Any arrow keys pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: paused = not paused
            elif event.key == pygame.K_RIGHT:
                for ball in balls: ball["vx"] += 1
            elif event.key == pygame.K_LEFT:
                for ball in balls: ball["vx"] -= 1
            elif event.key == pygame.K_UP:
                for ball in balls: ball["vy"] -= 1
            elif event.key == pygame.K_DOWN:
                for ball in balls: ball["vy"] += 1

        # Mouse button clicked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("clicked at", event.pos)

    # Update position of the ball
    if not paused:
        for ball in balls:
            ball["x"] += ball["vx"]
            ball["y"] += ball["vy"]
            if ball["x"] > 640 - 20 or ball["x"] < 20:
                ball["vx"] = -ball["vx"]
                ball["color"] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if ball["y"] > 480 - 20 or ball["y"] < 20:
                ball["vy"] = -ball["vy"]
                ball["color"] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # creates the ball
    screen.blit(trail, (0, 0))
    for ball in balls:
        pygame.draw.circle(screen, ball["color"], (ball["x"], ball["y"]), 20)
    pygame.display.flip()
    clock.tick(60)