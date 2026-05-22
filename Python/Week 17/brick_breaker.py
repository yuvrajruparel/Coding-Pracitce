import pygame, random

# Setting up all the variables
SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 640, 480, 60
PADDLE_W, PADDLE_H = 100, 12
BALL_SIZE, BALL_VX, BALL_VY = 20, random.choice([-5, 5]), -5
BRICK_W, BRICK_H, BRICK_COL, BRICK_ROW, GAP = 70, 20, 8, 5, 80/9
BG = (0, 10, 30)
PADDLE_COLOR, BALL_COLOR = (255, 255, 255), (255, 255, 255)
ROW_COLORS = [(255, 80, 80), (255, 160, 80), (255, 220, 80), (120, 220, 100), (100, 180, 255)]

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # generate 5 squish frames as Surfaces (no PNG files needed)
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
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.w, mouse_x - self.rect.w // 2))   # mouse follow
        if not self.playing:    # animation advance — only when playing
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
        self.vx = random.choice([-5, 5])
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
        self.big = pygame.font.SysFont(None, 64)                         
        self.small = pygame.font.SysFont(None, 26)                                     
    def handle_event(self, event):                                                     
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:                
            self.manager.go_to(PlayScene(self.manager))                              
    def draw(self, screen):                                                      
        screen.fill(BG)                                                                  
        title = self.big.render("BRICK BREAKER", True, (150, 230, 255))                  
        hint1 = self.small.render("RETURN to start  ·  SPACE to pause  ·  ESC to quit", True, (180, 180, 180))  
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30)))       
        screen.blit(hint1, hint1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30)))

class PlayScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = make_bricks()
        self.score = 0
        self.elapsed_ms = 0
        self.paused = False
        self.score_font = pygame.font.SysFont(None, 120)
        self.timer_font = pygame.font.SysFont(None, 26)
        self.hit    = pygame.mixer.Sound("Python/Week 17/sounds/hit.wav");    self.hit.set_volume(0.6)
        self.break_ = pygame.mixer.Sound("Python/Week 17/sounds/break.wav");  self.break_.set_volume(0.6)
        self.lose   = pygame.mixer.Sound("Python/Week 17/sounds/lose.wav");   self.lose.set_volume(1)
        self.win    = pygame.mixer.Sound("Python/Week 17/sounds/win.wav");    self.win.set_volume(1)
        pygame.mixer.music.load("Python/Week 17/sounds/bg_loop.wav")
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(loops=-1)

    def format_time(self):
        cs_total = self.elapsed_ms // 10
        minutes  = cs_total // 6000
        seconds  = (cs_total // 100) % 60
        cs       = cs_total % 100
        return f"{minutes:02d}:{seconds:02d}.{cs:02d}"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.paused = not self.paused
            (pygame.mixer.music.pause if self.paused else pygame.mixer.music.unpause)()

    def update(self, dt):
        if self.paused: return
        self.elapsed_ms += dt
        mouse_x = pygame.mouse.get_pos()[0]
        self.paddle.update(mouse_x, dt)
        self.ball.update()

        if self.ball.rect.colliderect(self.paddle.rect):
            self.hit.play()
            self.paddle.squish()
            self.ball.vy = -self.ball.vy
            self.ball.rect.bottom = self.paddle.rect.top
            offset = (self.ball.rect.centerx - self.paddle.rect.centerx) / (PADDLE_W / 2)
            self.ball.vx = int(5 * offset) if offset else self.ball.vx
            if self.ball.vx == 0:
                self.ball.vx = 5 if offset >= 0 else -5

        hits = pygame.sprite.spritecollide(self.ball, self.bricks, True)
        if hits:
            self.break_.play()
            self.ball.vy = -self.ball.vy
            self.score += 10 * len(hits)

        if self.ball.rect.top > SCREEN_HEIGHT:
            pygame.mixer.music.stop(); self.lose.play()
            self.manager.go_to(GameOver(self.manager, self.score, self.format_time(), won=False))
        elif len(self.bricks) == 0:
            pygame.mixer.music.stop(); self.win.play()
            self.manager.go_to(GameOver(self.manager, self.score, self.format_time(), won=True))

    def draw(self, screen):
        screen.fill(BG)
        score_surf = self.score_font.render(str(self.score), True, (40, 60, 110))
        screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
        self.bricks.draw(screen)
        screen.blit(self.paddle.image, self.paddle.rect)
        screen.blit(self.ball.image, self.ball.rect)
        timer_surf = self.timer_font.render(self.format_time(), True, (255, 255, 255))
        screen.blit(timer_surf, timer_surf.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10)))
        if self.paused:
            p_surf = self.score_font.render("PAUSED", True, (255, 255, 255))
            screen.blit(p_surf, p_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80)))

class GameOver(Scene):
    def __init__(self, manager, score, time_str, won):
        super().__init__(manager)
        self.score = score
        self.time_str = time_str
        self.won = won
        self.big   = pygame.font.SysFont(None, 56)
        self.med   = pygame.font.SysFont(None, 36)
        self.small = pygame.font.SysFont(None, 22)
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.go_to(MenuScene(self.manager))
    def draw(self, screen):
        screen.fill(BG)
        cx = SCREEN_WIDTH // 2
        msg   = "YOU WIN" if self.won else "GAME OVER"
        color = (120, 220, 100) if self.won else (255, 80, 80)
        title  = self.big.render(msg, True, color)
        s_line = self.med.render(f"Total Score: {self.score}", True, (255, 220, 80))
        t_line = self.med.render(f"Total Time:  {self.time_str}", True, (255, 255, 255))
        hint   = self.small.render("press RETURN for menu  ·  ESC to quit", True, (180, 180, 180))
        screen.blit(title,  title.get_rect(center=(cx, 130)))
        screen.blit(s_line, s_line.get_rect(center=(cx, 230)))
        screen.blit(t_line, t_line.get_rect(center=(cx, 280)))
        screen.blit(hint,   hint.get_rect(center=(cx, 380)))

def main():
    pygame.mixer.pre_init(
        frequency=44100, # 44.1 kHz
        size=-16, # signed 16-bit samples
        channels=2, # stereo
        buffer=512 # samples per buffer
    )
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Brick Breaker Game")
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