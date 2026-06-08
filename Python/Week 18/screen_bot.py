import time
import subprocess
import pyautogui
from pynput import keyboard # pynput is reliable on macOS, unlike the keyboard lib

# retina fix: locate returns physical pixels, click wants logical points
SCALE = pyautogui.screenshot().width / pyautogui.size().width # ~2.0 on retina

def to_click(pt): # convert a located point into click coordinates
    return (pt[0] / SCALE, pt[1] / SCALE)

# config (edit these directly)
TARGET_IMAGE = "Python/Week 18/Images/save_btn.png" # cropped PNG of the button you want to click
CONFIDENCE = 0.85 # match tolerance, 0-1, opencv installed
APP_A = "Safari" # hotkey toggles focus between these two
APP_B = "Notes"

# AppleScript bridge (same idea as Day 16 os_bridge)
def run_applescript(script): # fire a one-shot AppleScript and return its stdout
    out = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True
    )
    return out.stdout.strip()

# core: find and click 
def click_image(path, timeout=5.0, conf=CONFIDENCE): # wait for the image, then click its center
    pt = find_or_wait(path, timeout, conf) # retry until it appears (or times out)
    if pt is None: # never showed up
        return False
    pyautogui.click(to_click(pt), duration=0.4) # click the located point
    print("clicked:", path, "at", pt)
    return True

def find_or_wait(path, timeout=5.0, conf=CONFIDENCE): # retry locate until it appears or timeout
    deadline = time.time() + timeout
    while time.time() < deadline:
        pt = pyautogui.locateCenterOnScreen(path, confidence=conf, grayscale=True)
        if pt is not None: # found it - hand back the point
            return pt
        time.sleep(0.3) # dont hammer the CPU, recheck a few times a second
    print("timed out waiting for:", path) # still nothing after timeout
    return None

# hotkey toggles focus between two apps
_current = {"front": APP_B} # remember which app we last switched to

def toggle_focus(): # bring whichever app isnt focused to the front
    nxt = APP_A if _current["front"] == APP_B else APP_B
    run_applescript('tell application "' + nxt + '" to activate') # activate = focus
    _current["front"] = nxt
    print("focused:", nxt)

def main():
    click_image(TARGET_IMAGE) # find the button and click it on startup

    # cmd+shift+f flips focus, esc quits
    print("hotkeys live: cmd+shift+f = toggle focus, esc = quit")
    with keyboard.GlobalHotKeys({
        "<cmd>+<shift>+f": toggle_focus,
        "<esc>": lambda: (_ for _ in ()).throw(KeyboardInterrupt) # esc raises to exit
    }) as h:
        try:
            h.join() # block here until esc
        except KeyboardInterrupt:
            print("bye")

if __name__ == "__main__":
    main()