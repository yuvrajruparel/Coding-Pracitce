import pygame, random

# Setting up all the variables
SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 640, 480, 60
PADDLE_W, PADDLE_H = 100, 12
BALL_SIZE, BALL_VX, BALL_VY = 20, random.choice([-5, 5]), -5
BRICK_W, BRICK_H, BRICK_COL, BRICK_ROW, GAP = 70, 20, 8, 5, 80/9
BG = (15, 20, 40)
PADDLE_COLOR, BALL_COLOR = (255, 255, 255), (255, 255, 255)
ROW_COLORS = [(255, 80, 80), (255, 160, 80), (255, 220, 80), (120, 220, 100), (100, 180, 255)]

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # generate 5 squish frames as Surfaces (no PNG files needed)
        heights = [12, 8, 6, 8, 12]   # idle → compress → compress → uncompress → idle
        self.frames = []
        for h in heights:
            surf = pygame.Surface((PADDLE_W, PADDLE_H), pygame.SRCALPHA)
            y = (PADDLE_H - h) // 2     # vertically center the squished bar
            pygame.draw.rect(surf, PADDLE_COLOR, (0, y, PADDLE_W, h))
            self.frames.append(surf)
        self.idx = 0
        self.timer = 0
        self.playing = False
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30))

    def squish(self):
        self.idx = 0
        self.timer = 0
        self.playing = True

    def update(self, mouse_x, dt):
        # mouse follow (unchanged)
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.w, mouse_x - self.rect.w // 2))
        # animation advance — only when playing
        if not self.playing:
            return
        self.timer += dt
        if self.timer >= 80:
            self.timer = 0
            self.idx += 1
            if self.idx >= len(self.frames):
                self.idx = 0
                self.playing = False
            self.image = self.frames[self.idx]

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        self.color = BALL_COLOR
        pygame.draw.circle(self.image, self.color, (BALL_SIZE / 2, BALL_SIZE / 2), BALL_SIZE / 2)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.vx = BALL_VX
        self.vy = BALL_VY
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = -self.vx
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.vx = -self.vx
        if self.rect.top < 0:
            self.rect.top = 0
            self.vy = -self.vy

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_W, BRICK_H))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

def make_bricks():
    bricks = pygame.sprite.Group()
    for row in range(BRICK_ROW):
        for col in range(BRICK_COL):
            x = GAP + col * (BRICK_W + GAP)
            y = GAP + row * (BRICK_H + GAP)
            bricks.add(Brick(x, y, ROW_COLORS[row]))
    return bricks

def reset():
    return Paddle(), Ball(), make_bricks(), "play"

def main():
    pygame.mixer.pre_init(
        frequency=44100, # 44.1 kHz
        size=-16, # signed 16-bit samples
        channels=2, # stereo
        buffer=512 # samples per buffer
    )
    pygame.init()

    hit = pygame.mixer.Sound("Python/Week 17/sounds/hit.wav")
    hit.set_volume(0.6)
    break_ = pygame.mixer.Sound("Python/Week 17/sounds/break.wav")
    break_.set_volume(0.6)
    lose = pygame.mixer.Sound("Python/Week 17/sounds/lose.wav")
    lose.set_volume(1)
    win = pygame.mixer.Sound("Python/Week 17/sounds/win.wav")
    win.set_volume(1)

    pygame.mixer.music.load("Python/Week 17/sounds/bg_loop.wav")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(loops=-1)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Brick Breaker Prototype")
    clock = pygame.time.Clock()
    big = pygame.font.SysFont(None, 56)
    small = pygame.font.SysFont(None, 22)

    paddle, ball, bricks, state = reset()

    running = True
    paused = False

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RETURN:
                    paddle, ball, bricks, state = reset()
                    pygame.mixer.music.play(loops=-1)
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
        
        if state == "play" and not paused:
            mouse_x = pygame.mouse.get_pos()[0]
            paddle.update(mouse_x, dt)
            ball.update()

            # ball collides with paddle: speed and direction change to create aim
            if ball.rect.colliderect(paddle.rect):
                hit.play()
                paddle.squish()
                ball.vy = -ball.vy
                ball.rect.bottom = paddle.rect.top
                # tiny angle nudge based on hit position
                offset = (ball.rect.centerx - paddle.rect.centerx) / (PADDLE_W / 2)
                ball.vx = int(BALL_VX * offset) if offset else ball.vx
                if ball.vx == 0:
                    ball.vx = BALL_VX if offset >= 0 else -BALL_VX
            
            # ball collides with brick, vertical velocity flips direction
            hits = pygame.sprite.spritecollide(ball, bricks, True)
            if hits:
                break_.play()
                ball.vy = -ball.vy
            
            # end conditions
            if ball.rect.top > SCREEN_HEIGHT:
                state = "lose"
                pygame.mixer.music.stop()
                lose.play()
            elif len(bricks) == 0:
                state = "win"
                pygame.mixer.music.stop()
                win.play()

        # draw
        screen.fill(BG)
        bricks.draw(screen)
        screen.blit(paddle.image, paddle.rect)
        screen.blit(ball.image, ball.rect)

        if state != "play":
            msg = "YOU WIN" if state == "win" else "GAME OVER"
            color = (120, 220, 100) if state == "win" else (255, 80, 80)
            text = big.render(msg, True, color)
            hint = small.render("ENTER to reset  ·  ESC to quit", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))

        pygame.display.flip()

    pygame.quit()
    pygame.mixer.music.stop()

if __name__ == "__main__":
    main()