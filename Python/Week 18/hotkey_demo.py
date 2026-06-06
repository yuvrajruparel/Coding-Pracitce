from pynput import keyboard
import pyautogui as pag
import time

# Corner-slam the cursor to abort — your panic button if a loop goes haywire.
pag.FAILSAFE = True

EMAIL = "yuvrajruparel@gmail.com"

# Module-level handle to the listener so the esc handler can stop it.
listener = None

def type_email(): # Type the email into the focused field, one key at a time.
    print("[hotkey] cmd+shift+1 -> typing email")
    time.sleep(0.4)
    pag.typewrite(EMAIL, interval=0.05)

def click_center(): # Move to the center pixel of the screen and click.
    w, h = pag.size()
    print(f"[hotkey] cmd+shift+2 -> clicking center ({w // 2}, {h // 2})")
    pag.moveTo(w // 2, h // 2, duration=0.3)
    pag.click()

def quit_demo(): # Stop the listener, which unblocks join() and ends the program.
    print("esc pressed — exiting.")
    listener.stop()

def main():
    global listener
    # GlobalHotKeys takes a dict of {combo string: function}. pynput's combo
    # syntax wraps named keys in angle brackets: <cmd>, <shift>, <esc>.
    listener = keyboard.GlobalHotKeys({
        "<cmd>+<shift>+1": type_email,
        "<cmd>+<shift>+2": click_center,
        "<esc>": quit_demo,
    })

    print("Hotkeys live:")
    print("  cmd+shift+1  ->  type email")
    print("  cmd+shift+2  ->  click center")
    print("  esc          ->  quit")
    print("Waiting... (press esc to stop)")

    # start() launches the background listener; join() blocks here keeping the
    # program alive until quit_demo() calls listener.stop().
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()