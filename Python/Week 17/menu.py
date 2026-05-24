import pygame, sys, os, subprocess

WIDTH, HEIGHT, FPS = 800, 600, 60
BG          = (40, 0, 40)
WHITE       = (255, 255, 255)
BTN_IDLE    = (70, 10, 70)
BTN_HOVER   = (110, 30, 110)
BORDER      = (220, 180, 240)
HINT_GREY   = (180, 150, 200)

HERE = os.path.dirname(os.path.abspath(__file__))

class Button:
    def __init__(self, label, rect, filename):
        self.label = label
        self.rect = pygame.Rect(rect)
        self.filename = filename
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen, font):
        fill = BTN_HOVER if self.hovered else BTN_IDLE
        pygame.draw.rect(screen, fill,   self.rect, border_radius=10)
        pygame.draw.rect(screen, BORDER, self.rect, 2, border_radius=10)
        text = font.render(self.label, True, WHITE)
        screen.blit(text, text.get_rect(center=self.rect.center))

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return self.filename
        return None

def main():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Arcade")
    clock = pygame.time.Clock()

    pygame.mixer.music.load("Python/Week 17/sounds/arcade.wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    click_sfx = pygame.mixer.Sound("Python/Week 17/sounds/click.wav")
    click_sfx.set_volume(0.7)

    title_font = pygame.font.SysFont("menlo", 72, bold=True)
    btn_font   = pygame.font.SysFont("menlo", 28, bold=True)
    hint_font  = pygame.font.SysFont("menlo", 16, bold=True)

    bw, bh = 380, 65
    x = (WIDTH - bw) // 2
    buttons = [
        Button("BRICK BREAKER",  (x, 230, bw, bh), "brick_breaker.py"),
        Button("PONG",           (x, 320, bw, bh), "pong.py"),
        Button("ASTEROIDS LITE", (x, 410, bw, bh), "asteroids_lite.py"),
    ]

    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for b in buttons:
                    target = b.click(mouse_pos)
                    if target:
                        click_sfx.play()
                        pygame.mixer.music.pause()
                        subprocess.run([sys.executable, os.path.join(HERE, target)])
                        pygame.mixer.music.unpause()
                        break

        for b in buttons:
            b.update(mouse_pos)

        screen.fill(BG)
        title = title_font.render("MINI ARCADE", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))
        for b in buttons:
            b.draw(screen, btn_font)
        hint = hint_font.render("Click a game  ·  ESC to quit", True, HINT_GREY)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 30)))

        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()