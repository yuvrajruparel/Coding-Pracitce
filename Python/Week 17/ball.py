import pygame
import random

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.color = (80, 180, 255)
        pygame.draw.circle(self.image, self.color, (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = random.choice([-4, 4])
        self.vy = random.choice([-3, 3])

    def randomize_color(self):
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.image.fill((0, 0, 0, 0))   # wipe to fully transparent
        pygame.draw.circle(self.image, self.color, (10, 10), 10)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left < 0 or self.rect.right > 640:
            self.vx = -self.vx
            self.randomize_color()
        if self.rect.top < 0 or self.rect.bottom > 480:
            self.vy = -self.vy
            self.randomize_color()


pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Day 9 — Sprite & Group")
clock = pygame.time.Clock()

balls = pygame.sprite.Group()
for _ in range(50):
    balls.add(Ball(
        random.randint(20, 620),
        random.randint(20, 460)
    ))

running = True
paused = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_RIGHT:
                for b in balls: b.vx += 1
            elif event.key == pygame.K_LEFT:
                for b in balls: b.vx -= 1
            elif event.key == pygame.K_UP:
                for b in balls: b.vy -= 1
            elif event.key == pygame.K_DOWN:
                for b in balls: b.vy += 1

    if not paused:
        balls.update()

    screen.fill((15, 20, 40))
    balls.draw(screen)
    pygame.display.flip()

pygame.quit()