import pygame, random, math, os

# Setting up all the variables
SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 800, 600, 60
IMAGES_DIR = "/Users/yuvraj/Desktop/GitHub/Coding_Practice/Python/Week 17/images"
WHITE, DIM, RED, YELLOW = (240, 240, 240), (90,  90,  100), (220, 70,  70), (255, 252, 98)
SHIP_ROT_SPEED, SHIP_THRUST, SHIP_RADIUS, SHIP_INVUL_TIME, FIRE_COOLDOWN = 200, 220, 12, 2.0, 0.25
MAX_LIVES = 3
BULLET_SPEED, BULLET_LIFE = 480, 0.9
NUM_ASTEROIDS, ASTEROID_RADIUS, ASTEROID_SPEED, SPAWN_AVOID = 5, 10, (40, 90), 120
SCORE_PER_HIT = 25

CTRL_INTRO    = "RETURN start  ·  CLICK shoot  ·  SPACE pause  ·  ESC quit"
CTRL_PAUSE    = "RETURN to menu  ·  SPACE to unpause  ·  ESC to quit"
CTRL_GAMEOVER = "RETURN to menu  ·  ESC to quit"

# Helper Functions
def wrap(pos): # take a Vector2 position, wrap it around the screen edges
    pos.x %= SCREEN_WIDTH
    pos.y %= SCREEN_HEIGHT
    return pos

def unit_from_angle(angle_deg): # turn an angle (degrees) into a length-1 (x, y) direction
    rad = math.radians(angle_deg - 90)
    return pygame.Vector2(math.cos(rad), math.sin(rad))

def load_img(name, size, rotate=0): # load a PNG, resize it, optionally rotate it
    img = pygame.image.load(os.path.join(IMAGES_DIR, name)).convert_alpha()
    img = pygame.transform.smoothscale(img, size)
    if rotate:
        img = pygame.transform.rotate(img, rotate)
    return img

def draw_centered(screen, font, text, color, y): # render text and drop it horizontally centered at row y
    surf = font.render(text, True, color)
    screen.blit(surf, (SCREEN_WIDTH / 2 - surf.get_width() / 2, y))

class Ship:
    def __init__(self):
        self.reset()

    def reset(self):
        self.pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.radius = SHIP_RADIUS
        self.invul = SHIP_INVUL_TIME
        self.cooldown = 0.0

    def update(self, keys, dt):
        if keys[pygame.K_LEFT]:  self.angle -= SHIP_ROT_SPEED * dt
        if keys[pygame.K_RIGHT]: self.angle += SHIP_ROT_SPEED * dt
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_UP]:   direction += unit_from_angle(self.angle)
        if keys[pygame.K_DOWN]: direction -= unit_from_angle(self.angle)
        self.vel = direction * SHIP_THRUST
        self.pos += self.vel * dt
        wrap(self.pos)
        self.invul = max(0, self.invul - dt)
        self.cooldown = max(0, self.cooldown - dt)

    def can_fire(self):
        return self.cooldown <= 0

    def fire(self):
        self.cooldown = FIRE_COOLDOWN
        return Bullet(self.pos, self.angle)

    def draw(self, screen):
        if self.invul > 0 and int(self.invul * 8) % 2:
            return
        img = pygame.transform.rotate(Ship.image, -self.angle)
        rect = img.get_rect(center=self.pos)
        screen.blit(img, rect)

class Bullet:
    def __init__(self, pos, angle):
        self.pos = pygame.Vector2(pos)
        self.vel = unit_from_angle(angle) * BULLET_SPEED
        self.life = BULLET_LIFE
        self.angle = angle

    def update(self, dt):
        self.pos += self.vel * dt
        wrap(self.pos)
        self.life -= dt

    def draw(self, screen):
        img = pygame.transform.rotate(Bullet.image, -self.angle)
        rect = img.get_rect(center=self.pos)
        screen.blit(img, rect)

class Asteroid:
    def __init__(self, pos, size=3):
        self.pos = pygame.Vector2(pos)
        ang = random.uniform(0, 360)
        speed = random.uniform(*ASTEROID_SPEED) * (4 - size) / 2
        self.vel = pygame.Vector2(math.cos(math.radians(ang)),
                                  math.sin(math.radians(ang))) * speed
        self.size = size
        self.radius = size * ASTEROID_RADIUS
        d = int(self.radius * 2)
        self.image = pygame.transform.smoothscale(Asteroid.base, (d, d))

    def update(self, dt):
        self.pos += self.vel * dt
        wrap(self.pos)

    def draw(self, screen):
        rect = self.image.get_rect(center=self.pos)
        screen.blit(self.image, rect)

def split(a): # called when an asteroid `a` is destroyed — returns its fragments
    if a.size > 1:
        return [Asteroid(a.pos, a.size - 1), Asteroid(a.pos, a.size - 1)]
    return []

def spawn_field(n, avoid_pos, avoid_radius=SPAWN_AVOID): # make n big rocks, none too close to avoid_pos
    out = []
    for _ in range(n):
        while True:
            x = random.uniform(0, SCREEN_WIDTH)
            y = random.uniform(0, SCREEN_HEIGHT)
            if (pygame.Vector2(x, y) - avoid_pos).length() > avoid_radius:
                break
        out.append(Asteroid((x, y), size=3))
    return out

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
        self.font_title = pygame.font.SysFont("menlo", 64, bold=True)
        self.font_sm    = pygame.font.SysFont("menlo", 18, bold=True)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.go_to(PlayScene(self.manager))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, screen):
        screen.blit(Scene.bg, (0, 0))
        draw_centered(screen, self.font_title, "ASTEROIDS LITE", YELLOW, SCREEN_HEIGHT/2 - 60)
        draw_centered(screen, self.font_sm,    CTRL_INTRO,       WHITE,  SCREEN_HEIGHT/2 + 30)
        mm = self.font_sm.render("M for Main Menu", True, WHITE)
        screen.blit(mm, mm.get_rect(topright=(SCREEN_WIDTH - 15, 15)))

class PlayScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.ship = Ship()
        self.asteroids = spawn_field(NUM_ASTEROIDS, self.ship.pos)
        self.bullets = []
        self.score = 0
        self.lives = MAX_LIVES
        self.paused = False
        self.font_sm  = pygame.font.SysFont("menlo", 18, bold=True)
        self.font_mid = pygame.font.SysFont("menlo", 56, bold=True)
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 140))
        self.shoot = pygame.mixer.Sound("Python/Week 17/sounds/shoot.wav");    self.shoot.set_volume(0.6)
        self.lose = pygame.mixer.Sound("Python/Week 17/sounds/lose.wav");   self.lose.set_volume(1)
        self.explosion = pygame.mixer.Sound("Python/Week 17/sounds/explosion.wav");    self.explosion.set_volume(0.6)
        self.die = pygame.mixer.Sound("Python/Week 17/sounds/die.wav");    self.die.set_volume(0.6)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.paused = not self.paused
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.go_to(MenuScene(self.manager))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.paused and self.ship.can_fire():
                self.bullets.append(self.ship.fire())
                self.shoot.play()

    def update(self, dt):
        if self.paused: return

        keys = pygame.key.get_pressed()
        self.ship.update(keys, dt)

        for b in self.bullets[:]:
            b.update(dt)
            if b.life <= 0:
                self.bullets.remove(b)

        for a in self.asteroids:
            a.update(dt)

        # bullet vs asteroid
        for b in self.bullets[:]:
            for a in self.asteroids[:]:
                if b.pos.distance_to(a.pos) < a.radius:
                    self.bullets.remove(b)
                    self.asteroids.remove(a)
                    self.asteroids.extend(split(a))
                    self.score += (4 - a.size) * SCORE_PER_HIT
                    self.explosion.play()
                    break

        # ship vs asteroid
        if self.ship.invul <= 0:
            for a in self.asteroids:
                if self.ship.pos.distance_to(a.pos) < a.radius + self.ship.radius:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.lose.play()
                        self.manager.go_to(GameOverScene(self.manager, self.score))
                        return
                    else:
                        self.die.play()
                        self.ship.reset()
                    break

        # next wave
        if not self.asteroids:
            self.asteroids = spawn_field(NUM_ASTEROIDS, self.ship.pos)

    def draw(self, screen):
        screen.blit(Scene.bg, (0, 0))
        for a in self.asteroids: a.draw(screen)
        for b in self.bullets:   b.draw(screen)
        self.ship.draw(screen)

        screen.blit(self.font_sm.render(f"SCORE  {self.score}", True, WHITE), (12, 10))
        for i in range(self.lives):
            screen.blit(PlayScene.heart, (12 + i * 26, 32))

        if self.paused:
            screen.blit(self.overlay, (0, 0))
            draw_centered(screen, self.font_mid, "PAUSED",   YELLOW, SCREEN_HEIGHT/2 - 50)
            draw_centered(screen, self.font_sm,  CTRL_PAUSE, WHITE,  SCREEN_HEIGHT/2 + 15)

class GameOverScene(Scene):
    def __init__(self, manager, score):
        super().__init__(manager)
        self.score = score
        self.font_sm  = pygame.font.SysFont("menlo", 18, bold=True)
        self.font_mid = pygame.font.SysFont("menlo", 56, bold=True)
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 140))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.go_to(MenuScene(self.manager))

    def draw(self, screen):
        screen.blit(Scene.bg, (0, 0))
        screen.blit(self.overlay, (0, 0))
        draw_centered(screen, self.font_mid, "GAME OVER",   RED,   SCREEN_HEIGHT/2 - 50)
        draw_centered(screen, self.font_sm,  CTRL_GAMEOVER, WHITE, SCREEN_HEIGHT/2 + 15)

def main():
    pygame.mixer.pre_init(
        frequency=44100, # 44.1 kHz
        size=-16, # signed 16-bit samples
        channels=2, # stereo
        buffer=512 # samples per buffer
    )
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids Lite")
    clock = pygame.time.Clock()

    Ship.image      = load_img("rocket.png",   (50, 50), rotate=45)
    Bullet.image    = load_img("bullet.png",   (18, 18), rotate=45)
    Asteroid.base   = load_img("asteroid.png", (84, 84))
    PlayScene.heart = load_img("heart.png",    (22, 22))
    Scene.bg        = load_img("space_bg.png", (SCREEN_WIDTH, SCREEN_HEIGHT))

    manager = SceneManager()
    manager.go_to(MenuScene(manager))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

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