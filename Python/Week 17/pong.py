import pygame, random, math

# Setting up all the variables
SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 800, 600, 60
WIN_SCORE = 11
PADDLE_W, PADDLE_H = 12, 90
BALL_SIZE, BALL_START_SPEED, BALL_SPEEDUP, BALL_MAX_SPEED, MAX_BOUNCE_ANGLE = 20, 360, 1.05, 720, math.radians(60)
PLAYER_SPEED, AI_SPEED, AI_DEADZONE = 420, 340, 18
WHITE, BLACK, GREY = (255, 255, 255), (0, 0, 0), (90, 100, 110)

SCREEN_RECT = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((PADDLE_W, PADDLE_H))
        self.image.fill(WHITE)
        self.rect  = self.image.get_rect(center=(x, SCREEN_HEIGHT // 2))
        self.vy    = 0
        self.speed = PLAYER_SPEED

    def update(self, dt):
        self.rect.y += int(self.vy * (dt / 1000)) # dt is in ms
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

class AIPaddle(Paddle):
    def __init__(self, x, ball):
        super().__init__(x)
        self.ball     = ball
        self.speed    = AI_SPEED
        self.deadzone = AI_DEADZONE

    def update(self, dt):
        if self.ball.vx > 0:
            diff = self.ball.rect.centery - self.rect.centery
            if abs(diff) > self.deadzone:
                self.vy = self.speed if diff > 0 else -self.speed
            else:
                self.vy = 0
        else:
            self.vy = 0
        super().update(dt)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.rect  = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.vx = self.vy = 0.0
        self.speed = BALL_START_SPEED
        self._fx, self._fy = float(self.rect.x), float(self.rect.y)

    def reset(self, direction):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self._fx, self._fy = float(self.rect.x), float(self.rect.y)
        self.speed = BALL_START_SPEED
        angle = random.uniform(-math.radians(30), math.radians(30))
        self.vx = direction * self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def update(self, dt):
        sec = dt / 1000
        self._fx += self.vx * sec
        self._fy += self.vy * sec
        self.rect.x, self.rect.y = int(self._fx), int(self._fy)
        
        if self.rect.top <= 0:
            self.rect.top = 0
            self._fy = float(self.rect.y)
            self.vy = abs(self.vy)
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self._fy = float(self.rect.y)
            self.vy = -abs(self.vy)

class Scene:
    def __init__(self, manager):
        self.manager = manager
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self, screen): pass

class SceneManager:
    def __init__(self):
        self.active = None
    def go_to(self, scene): 
        self.active = scene
    def handle_event(self, event): self.active.handle_event(event)
    def update(self, dt): self.active.update(dt)
    def draw(self, screen): self.active.draw(screen)

class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.big = pygame.font.SysFont("menlo", 72, bold=True)
        self.small = pygame.font.SysFont("menlo", 22)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.go_to(PlayScene(self.manager))

    def draw(self, screen):
        screen.fill(BLACK)
        title = self.big.render("PONG", True, WHITE)
        hint = self.small.render("RETURN to start  ·  SPACE to pause  ·  ESC to quit", True, GREY)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)))

class PlayScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.ball = Ball()
        self.player = Paddle(30)
        self.ai = AIPaddle(SCREEN_WIDTH - 30, self.ball)
        self.paddles = pygame.sprite.Group(self.player, self.ai)
        self.score_l = 0
        self.score_r = 0
        self.paused = False
        self.font = pygame.font.SysFont("menlo", 60, bold=True)
        self.ball.reset(random.choice([-1, 1]))
        self.hit    = pygame.mixer.Sound("Python/Week 17/sounds/hit.wav");    self.hit.set_volume(0.6)
        self.lose   = pygame.mixer.Sound("Python/Week 17/sounds/lose.wav");   self.lose.set_volume(1)
        self.win    = pygame.mixer.Sound("Python/Week 17/sounds/win.wav");    self.win.set_volume(1)
        pygame.mixer.music.load("Python/Week 17/sounds/bg_loop.wav")
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(loops=-1)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.paused = not self.paused
            (pygame.mixer.music.pause if self.paused else pygame.mixer.music.unpause)()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.paused:
            pygame.mixer.music.stop()
            self.manager.go_to(MenuScene(self.manager))

    def update(self, dt):
        if self.paused: return

        keys = pygame.key.get_pressed()
        self.player.vy = 0
        if keys[pygame.K_UP]:   self.player.vy = -self.player.speed
        if keys[pygame.K_DOWN]: self.player.vy =  self.player.speed

        self.paddles.update(dt)
        self.ball.update(dt)

        # Collisions
        if self.ball.rect.colliderect(self.player.rect) and self.ball.vx < 0:
            self.bounce(self.player)
            self.hit.play()
        elif self.ball.rect.colliderect(self.ai.rect) and self.ball.vx > 0:
            self.bounce(self.ai)
            self.hit.play()

        # Scoring
        if self.ball.rect.right < 0:
            self.score_r += 1
            self.ball.reset(-1)
        elif self.ball.rect.left > SCREEN_WIDTH:
            self.score_l += 1
            self.ball.reset(1)

        if self.score_l >= WIN_SCORE:
            pygame.mixer.music.stop(); self.win.play()
            self.manager.go_to(GameOver(self.manager, self.score_l, self.score_r))
        elif self.score_r >= WIN_SCORE:
            pygame.mixer.music.stop(); self.lose.play()
            self.manager.go_to(GameOver(self.manager, self.score_l, self.score_r))

    def bounce(self, paddle):
        offset = (self.ball.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
        angle = max(-1.0, min(1.0, offset)) * MAX_BOUNCE_ANGLE
        self.ball.speed = min(self.ball.speed * BALL_SPEEDUP, BALL_MAX_SPEED)
        direction = 1 if self.ball.vx < 0 else -1
        self.ball.vx = direction * self.ball.speed * math.cos(angle)
        self.ball.vy = self.ball.speed * math.sin(angle)
        self.ball._fx = float(self.ball.rect.x)

    def draw(self, screen):
        screen.fill(BLACK)
        for y in range(0, SCREEN_HEIGHT, 24):
            pygame.draw.rect(screen, GREY, (SCREEN_WIDTH // 2 - 2, y, 4, 14))
        
        score_surf = self.font.render(f"{self.score_l}   {self.score_r}", True, WHITE)
        screen.blit(score_surf, score_surf.get_rect(midtop=(SCREEN_WIDTH // 2, 20)))
        
        self.paddles.draw(screen)
        screen.blit(self.ball.image, self.ball.rect)
        if self.paused:
            p_surf = self.font.render("PAUSED", True, WHITE)
            hint_font = pygame.font.SysFont("menlo", 20)
            h_surf = hint_font.render("SPACE to resume  ·  RETURN for menu", True, GREY)
            screen.blit(p_surf, p_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
            screen.blit(h_surf, h_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)))

class GameOver(Scene):
    def __init__(self, manager, sl, sr):
        super().__init__(manager)
        self.scores = (sl, sr)
        self.font = pygame.font.SysFont("menlo", 64, bold=True)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.go_to(MenuScene(self.manager))

    def draw(self, screen):
        screen.fill(BLACK)
        won = self.scores[0] > self.scores[1]
        msg = "YOU WIN" if won else "YOU LOSE"
        color = (120, 220, 100) if won else (255, 80, 80)
        title = self.font.render(msg, True, color)
        score = self.font.render(f"{self.scores[0]} - {self.scores[1]}", True, WHITE)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 200)))
        screen.blit(score, score.get_rect(center=(SCREEN_WIDTH//2, 300)))

def main():
    pygame.mixer.pre_init(
        frequency=44100, # 44.1 kHz
        size=-16, # signed 16-bit samples
        channels=2, # stereo
        buffer=512 # samples per buffer
    )
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong - Scene Style")
    clock = pygame.time.Clock()

    manager = SceneManager()
    manager.go_to(MenuScene(manager))
    
    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                manager.handle_event(event)

        manager.update(dt)
        manager.draw(screen)
        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()