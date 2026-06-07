import time, threading
import pyautogui as pag
from pynput import keyboard

# config
pag.PAUSE = 0 # stop pyautogui's default 0.1s pause so cps is accurate
click_button = "right" # "left" or "right" — change here only
clicking = False
cps = 30 # clicks per second
hold_key = "r" # hold key
holding = False
running = True

# toggle-mode click loop
def click_loop():
    while running:
        if clicking:
            t = time.perf_counter()
            pag.click(button=click_button) # follows cursor (pyautogui default)
            time.sleep(max(0, 1 / cps - (time.perf_counter() - t))) # subtract click time
        else:
            time.sleep(1 / cps)

# hold mode: click ONLY while key is down
def hold_loop():
    while running:
        if holding:
            t = time.perf_counter()
            pag.click(button=click_button)
            time.sleep(max(0, 1 / cps - (time.perf_counter() - t)))
        else:
            time.sleep(1 / cps)

# cps control
def set_cps(new):
    global cps
    cps = max(1, min(50, new))
    print(f"cps = {cps}")

# toggle mode: press once on, press again off
# decorator: bind a function to a key combo
_hotkeys = {}
def hotkey(combo):
    def wrap(fn):
        _hotkeys[combo] = fn
        return fn
    return wrap

@hotkey("<ctrl>+<shift>+s")
def toggle():
    global clicking
    clicking = not clicking
    print("clicking ON" if clicking else "clicking OFF")

@hotkey("<ctrl>+<shift>+<up>")
def cps_up():   set_cps(cps + 1)

@hotkey("<ctrl>+<shift>+<down>")
def cps_down(): set_cps(cps - 1)

@hotkey("<esc>")
def quit_app():
    global running
    running = False
    listener.stop()

# build HotKey objects from the decorator map
_combos = [keyboard.HotKey(keyboard.HotKey.parse(c), fn) for c, fn in _hotkeys.items()]

# one listener: feed every key to the combos + track the hold key
def on_press(key):
    global holding
    k = listener.canonical(key)
    for hk in _combos:
        hk.press(k)
    if key == keyboard.KeyCode.from_char(hold_key):
        holding = True

def on_release(key):
    global holding
    k = listener.canonical(key)
    for hk in _combos:
        hk.release(k)
    if key == keyboard.KeyCode.from_char(hold_key):
        holding = False

# start click loops
threading.Thread(target=click_loop, daemon=True).start()
threading.Thread(target=hold_loop, daemon=True).start()

# build the prompt from the decorator map so it updates when a hotkey changes
prompt = " · ".join(f"{fn.__name__.replace('_', ' ')}: {c.replace('<', '').replace('>', '')}" for c, fn in _hotkeys.items())
print(f"{prompt} · hold '{hold_key}'")

# single listener: combos + hold key; esc quits
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
try:
    listener.join()      # blocks main thread until esc/quit
except KeyboardInterrupt:
    quit_app()