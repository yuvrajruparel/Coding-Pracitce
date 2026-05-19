import pygame
import numpy as np
from collections import deque

from smd_model import f, rk4_step, regime
from shapes    import Box
from vector3d  import Vector3D

# window + palette
WIN_W, WIN_H = 1100, 620
FPS          = 60
DT           = 1.0 / FPS

NAVY      = ( 15,  26,  46)
CARD_BG   = ( 24,  37,  60)
CARD_LINE = ( 45,  62,  92)
TRACK_BG  = ( 38,  54,  82)
ACCENT    = ( 61, 165, 255)
ACCENT_DK = ( 30, 136, 229)
INK       = (220, 230, 245)
SUBTLE    = (170, 185, 205)
MUTED     = (108, 122, 137)
SPRING_C  = (200, 210, 225)
WARN      = (231, 111,  63)
GOOD      = ( 27, 180, 138)

SIDEBAR_W  = 320
PX_PER_M   = 130
REST_LEN_M = 2.0

# UI primitives
class Slider:
    """Horizontal draggable slider; single source of truth for one float."""
    HEIGHT, KNOB_R = 6, 8

    def __init__(self, x, y, w, label, vmin, vmax, value, fmt="{:.2f}", unit=""):
        self.track = pygame.Rect(x, y, w, self.HEIGHT)
        self.label, self.unit, self.fmt = label, unit, fmt
        self.vmin, self.vmax = vmin, vmax
        self.value = value
        self.grabbed = False

    @property
    def knob_x(self):
        frac = (self.value - self.vmin) / (self.vmax - self.vmin)
        return self.track.x + int(frac * self.track.w)

    def _hit(self, pos):
        return self.track.inflate(0, 20).collidepoint(pos)

    def handle(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and self._hit(ev.pos):
            self.grabbed = True
            self._set_from(ev.pos[0])
        elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
            self.grabbed = False
        elif ev.type == pygame.MOUSEMOTION and self.grabbed:
            self._set_from(ev.pos[0])

    def _set_from(self, mx):
        frac = max(0.0, min(1.0, (mx - self.track.x) / self.track.w))
        self.value = self.vmin + frac * (self.vmax - self.vmin)

    def nudge(self, delta):
        self.value = max(self.vmin, min(self.vmax, self.value + delta))

    def draw(self, screen, f_lab, f_val):
        screen.blit(f_lab.render(self.label, True, MUTED),
                    (self.track.x, self.track.y - 22))
        s_val = self.fmt.format(self.value) + ((" " + self.unit) if self.unit else "")
        val_surf = f_val.render(s_val, True, INK)
        screen.blit(val_surf, (self.track.right - val_surf.get_width(), self.track.y - 22))

        pygame.draw.rect(screen, TRACK_BG, self.track, border_radius=3)
        fill_w = self.knob_x - self.track.x
        if fill_w > 0:
            pygame.draw.rect(screen, ACCENT_DK,
                             (self.track.x, self.track.y, fill_w, self.track.h),
                             border_radius=3)
        pygame.draw.circle(screen, ACCENT, (self.knob_x, self.track.centery), self.KNOB_R)
        pygame.draw.circle(screen, NAVY,   (self.knob_x, self.track.centery), self.KNOB_R, 2)

class Button:
    """Click button with optional toggled state."""
    def __init__(self, x, y, w, h, label, on_click, toggled=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.label, self.on_click = label, on_click
        self.toggled = toggled
        self.hover = False

    def handle(self, ev):
        if ev.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(ev.pos)
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 \
                and self.rect.collidepoint(ev.pos):
            self.on_click()

    def draw(self, screen, font):
        if self.toggled:
            bg, fg = ACCENT, NAVY
        elif self.hover:
            bg, fg = CARD_LINE, INK
        else:
            bg, fg = TRACK_BG, INK
        pygame.draw.rect(screen, bg, self.rect, border_radius=6)
        if not self.toggled:
            pygame.draw.rect(screen, CARD_LINE, self.rect, 1, border_radius=6)
        txt = font.render(self.label, True, fg)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

# state (globals — view layer owns these)
X0        = np.array([0.5, 0.0])
X         = X0.copy()
t         = 0.0
paused    = False
running   = True
FORCES    = ("free", "step", "sin")
force_ix  = 0
trail     = deque(maxlen=900)

mass_box  = Box(Vector3D(0, 0, 0), Vector3D(0, 0, 0), width=0.6, height=0.6)

# scene geometry filled in by main() once we know the layout
WALL_X = BASELINE_Y = GROUND_Y = 0

# forcing closure
def make_F_fn(A, omega_f):
    lbl = FORCES[force_ix]
    if lbl == "free": return lambda tt: 0.0
    if lbl == "step": return lambda tt: 1.0 if tt > 1.0 else 0.0
    return lambda tt: A * np.sin(omega_f * tt)

# world → screen
def world_to_px(x_m):
    return WALL_X + int((REST_LEN_M + x_m) * PX_PER_M)

# drawing helpers
def card(screen, rect, title, font):
    pygame.draw.rect(screen, CARD_BG,   rect, border_radius=10)
    pygame.draw.rect(screen, CARD_LINE, rect, 1, border_radius=10)
    pygame.draw.rect(screen, ACCENT, (rect.x + 14, rect.y + 14, 3, 12), border_radius=2)
    screen.blit(font.render(title, True, ACCENT), (rect.x + 24, rect.y + 11))

def draw_spring(screen, x_start, y, x_end, coils=14, amp=14):
    span = x_end - x_start
    pts = [(x_start, y)]
    if span < 6:
        pts.append((x_end, y))
    else:
        for i in range(1, coils + 1):
            px = x_start + span * i / (coils + 1)
            py = y + (amp if i % 2 else -amp)
            pts.append((px, py))
        pts.append((x_end, y))
    pygame.draw.aalines(screen, SPRING_C, False, pts)

def draw_scene(screen, scene_rect, f_sm, f_lg):
    pygame.draw.rect(screen, CARD_BG,   scene_rect, border_radius=10)
    pygame.draw.rect(screen, CARD_LINE, scene_rect, 1, border_radius=10)
    pygame.draw.rect(screen, ACCENT, (scene_rect.x + 14, scene_rect.y + 14, 3, 12), border_radius=2)
    screen.blit(f_sm.render("SCENE   wall · spring · mass", True, ACCENT),
                (scene_rect.x + 24, scene_rect.y + 11))

    # ground
    pygame.draw.line(screen, CARD_LINE,
                     (scene_rect.x + 24, GROUND_Y),
                     (scene_rect.right - 24, GROUND_Y), 1)

    # x = 0 reference tick
    rest_px = world_to_px(0.0)
    pygame.draw.line(screen, CARD_LINE,
                     (rest_px, GROUND_Y - 110),
                     (rest_px, GROUND_Y + 6), 1)
    lbl = f_sm.render("x = 0", True, MUTED)
    screen.blit(lbl, (rest_px - lbl.get_width() // 2, GROUND_Y + 10))

    # wall + hatches
    pygame.draw.line(screen, SUBTLE,
                     (WALL_X, scene_rect.y + 60),
                     (WALL_X, GROUND_Y - 4), 4)
    for ty in range(scene_rect.y + 65, GROUND_Y - 4, 12):
        pygame.draw.line(screen, MUTED, (WALL_X - 12, ty + 8), (WALL_X - 2, ty), 1)

    # mass
    mass_box.pos.x = float(X[0])
    cx   = world_to_px(mass_box.pos.x)
    half = int(mass_box.width * PX_PER_M / 2)
    cx_v = max(WALL_X + 30, min(scene_rect.right - 30, cx))   # clamp visual only

    draw_spring(screen, WALL_X + 2, BASELINE_Y, cx_v - half)

    rect = pygame.Rect(cx_v - half, BASELINE_Y - half, 2 * half, 2 * half)
    pygame.draw.rect(screen, ACCENT,    rect, border_radius=4)
    pygame.draw.rect(screen, ACCENT_DK, rect, 2, border_radius=4)
    pygame.draw.line(screen, NAVY,
                     (rect.centerx - 10, rect.centery),
                     (rect.centerx + 10, rect.centery), 2)

    # off-scene marker
    if cx != cx_v:
        warn = f_sm.render(f"off-scene  x = {X[0]:+.2f} m", True, WARN)
        screen.blit(warn, (rect.centerx - warn.get_width() // 2, rect.bottom + 12))

    # paused overlay
    if paused:
        ps = f_lg.render("PAUSED", True, SUBTLE)
        screen.blit(ps, (scene_rect.centerx - ps.get_width() // 2, scene_rect.y + 38))

def draw_state_bar(screen, m, k, c, bar_rect, fonts):
    f_sm, f_md, _ = fonts
    pygame.draw.rect(screen, CARD_BG,   bar_rect, border_radius=10)
    pygame.draw.rect(screen, CARD_LINE, bar_rect, 1, border_radius=10)

    zeta = c / (2 * (m * k) ** 0.5) if m > 0 and k > 0 else 0.0
    reg  = regime(m, c, k)
    reg_col = WARN if reg == "overdamped" else GOOD if reg == "critical" else ACCENT

    cells = [
        ("x",      f"{X[0]:+.3f} m",   INK),
        ("v",      f"{X[1]:+.3f} m/s", INK),
        ("t",      f"{t:6.2f} s",      INK),
        ("ζ",      f"{zeta:.3f}",      INK),
        ("regime", reg,                reg_col),
    ]
    cell_w = bar_rect.w // len(cells)
    for i, (lab, val, col) in enumerate(cells):
        cx = bar_rect.x + cell_w * i + cell_w // 2
        l_ = f_sm.render(lab, True, MUTED)
        v_ = f_md.render(val, True, col)
        screen.blit(l_, (cx - l_.get_width() // 2, bar_rect.y + 14))
        screen.blit(v_, (cx - v_.get_width() // 2, bar_rect.y + 36))

def draw_trail(screen, rect, fonts):
    f_sm, _, _ = fonts
    pygame.draw.rect(screen, CARD_BG,   rect, border_radius=10)
    pygame.draw.rect(screen, CARD_LINE, rect, 1, border_radius=10)
    pygame.draw.rect(screen, ACCENT, (rect.x + 14, rect.y + 14, 3, 12), border_radius=2)
    screen.blit(f_sm.render("PHASE SPACE   x → v", True, ACCENT),
                (rect.x + 24, rect.y + 11))
    screen.blit(f_sm.render("closed loop = pure oscillation     inward spiral = damping",
                            True, MUTED),
                (rect.x + 180, rect.y + 13))

    plot = pygame.Rect(rect.x + 24, rect.y + 36, rect.w - 48, rect.h - 50)
    cx, cy = plot.centerx, plot.centery
    pygame.draw.line(screen, CARD_LINE, (plot.x, cy), (plot.right, cy), 1)
    pygame.draw.line(screen, CARD_LINE, (cx, plot.y), (cx, plot.bottom), 1)
    screen.blit(f_sm.render("x", True, MUTED), (plot.right - 10, cy + 4))
    screen.blit(f_sm.render("v", True, MUTED), (cx + 4, plot.y))

    if len(trail) < 2:
        return
    arr = np.array(trail)
    xmax = max(0.05, np.max(np.abs(arr[:, 0])))
    vmax = max(0.05, np.max(np.abs(arr[:, 1])))
    sx   = plot.w / 2 / xmax * 0.92
    sy   = plot.h / 2 / vmax * 0.92
    pts  = [(cx + xi * sx, cy - vi * sy) for xi, vi in trail]
    pygame.draw.aalines(screen, ACCENT, False, pts)
    px, py = pts[-1]
    pygame.draw.circle(screen, INK, (int(px), int(py)), 3)

# main
def main():
    global X, t, running, paused, force_ix
    global WALL_X, BASELINE_Y, GROUND_Y

    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("SMD — pygame port")
    clock  = pygame.time.Clock()

    f_sm = pygame.font.SysFont("menlo,monaco,consolas,monospace", 12)
    f_md = pygame.font.SysFont("menlo,monaco,consolas,monospace", 15, bold=True)
    f_lg = pygame.font.SysFont("helveticaneue,arial,sans-serif", 26, bold=True)
    fonts = (f_sm, f_md, f_lg)

    # layout
    pad  = 16
    sb_x = pad + 8
    sb_w = SIDEBAR_W - 2 * (pad + 8)

    param_card = pygame.Rect(pad,  pad, SIDEBAR_W - 2 * pad, 370)
    force_card = pygame.Rect(pad, 398, SIDEBAR_W - 2 * pad,  64)
    ctrl_card  = pygame.Rect(pad, 478, SIDEBAR_W - 2 * pad,  64)
    hint_card  = pygame.Rect(pad, 558, SIDEBAR_W - 2 * pad,  46)

    bar_rect   = pygame.Rect(SIDEBAR_W + pad,  pad, WIN_W - SIDEBAR_W - 2 * pad,  70)
    scene_rect = pygame.Rect(SIDEBAR_W + pad, 102, WIN_W - SIDEBAR_W - 2 * pad, 340)
    trail_rect = pygame.Rect(SIDEBAR_W + pad, 458, WIN_W - SIDEBAR_W - 2 * pad, 146)

    WALL_X     = scene_rect.x + 60
    GROUND_Y   = scene_rect.bottom - 40
    BASELINE_Y = GROUND_Y - 70

    # sliders
    y0 = 84
    s_m = Slider(sb_x, y0,       sb_w, "m",   0.1, 10.0,  1.0, "{:5.2f}", "kg")
    s_k = Slider(sb_x, y0 +  56, sb_w, "k",   0.1, 50.0, 10.0, "{:5.2f}", "N/m")
    s_c = Slider(sb_x, y0 + 112, sb_w, "c",   0.0, 10.0,  0.5, "{:5.2f}", "Ns/m")
    s_A = Slider(sb_x, y0 + 168, sb_w, "A",   0.0, 10.0,  1.0, "{:5.2f}", "N")
    s_w = Slider(sb_x, y0 + 224, sb_w, "ω_f", 0.1, 20.0,  3.0, "{:5.2f}", "rad/s")
    sliders = [s_m, s_k, s_c, s_A, s_w]

    # force radio buttons
    def set_force(i):
        def _():
            global force_ix
            force_ix = i
        return _

    bw = (sb_w - 16) // 3
    by = force_card.y + 28
    force_btns = [
        Button(sb_x + i * (bw + 8), by, bw, 28, lbl, set_force(i), toggled=(i == 0))
        for i, lbl in enumerate(FORCES)
    ]

    # pause / reset
    def do_pause():
        global paused
        paused = not paused
    def do_reset():
        global X, t
        X = X0.copy()
        t = 0.0
        trail.clear()

    bw2 = (sb_w - 8) // 2
    by2 = ctrl_card.y + 18
    btn_pause = Button(sb_x,           by2, bw2, 36, "PAUSE", do_pause)
    btn_reset = Button(sb_x + bw2 + 8, by2, bw2, 36, "RESET", do_reset)

    # main loop
    while running:
        # 1. EVENTS
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if   ev.key == pygame.K_ESCAPE: running = False
                elif ev.key == pygame.K_SPACE:  do_pause()
                elif ev.key == pygame.K_r:      do_reset()
                elif ev.key == pygame.K_f:      force_ix = (force_ix + 1) % len(FORCES)
                elif ev.key == pygame.K_EQUALS:        s_m.nudge( 0.1)
                elif ev.key == pygame.K_MINUS:         s_m.nudge(-0.1)
                elif ev.key == pygame.K_LEFTBRACKET:   s_w.nudge(-0.2)
                elif ev.key == pygame.K_RIGHTBRACKET:  s_w.nudge( 0.2)
            for s in sliders:     s.handle(ev)
            for b in force_btns:  b.handle(ev)
            btn_pause.handle(ev)
            btn_reset.handle(ev)

        # sync toggled states
        for i, b in enumerate(force_btns):
            b.toggled = (i == force_ix)
        btn_pause.label   = "RESUME" if paused else "PAUSE"
        btn_pause.toggled = paused

        # 2. read live params
        m, k, c = s_m.value, s_k.value, s_c.value
        A, w_f  = s_A.value, s_w.value

        # 3. UPDATE
        if not paused:
            F_fn = make_F_fn(A, w_f)
            X = rk4_step(lambda tt, xx: f(tt, xx, m, c, k, F_fn), t, X, DT)
            t += DT
            trail.append((float(X[0]), float(X[1])))

        # 4. DRAW
        screen.fill(NAVY)

        # sidebar
        card(screen, param_card, "PARAMETERS", f_sm)
        for s in sliders:
            s.draw(screen, f_sm, f_md)

        card(screen, force_card, "FORCING", f_sm)
        for b in force_btns:
            b.draw(screen, f_sm)

        card(screen, ctrl_card, "CONTROL", f_sm)
        btn_pause.draw(screen, f_sm)
        btn_reset.draw(screen, f_sm)

        card(screen, hint_card, "KEYS", f_sm)
        screen.blit(f_sm.render("SPACE pause   R reset   F force   = / - / [ / ]",
                                True, SUBTLE),
                    (hint_card.x + 14, hint_card.y + 28))

        # main area
        draw_state_bar(screen, m, k, c, bar_rect, fonts)
        draw_scene(screen, scene_rect, f_sm, f_lg)
        draw_trail(screen, trail_rect, fonts)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
