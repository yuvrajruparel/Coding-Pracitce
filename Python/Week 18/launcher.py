import time, schedule, random # running jobs on timers, etc
import subprocess # controlling os with code
import pyperclip # reading and writing the clipboard
import pyautogui as pag
from pynput import keyboard # pynput is reliable on macOS, unlike the keyboard lib
import sys # lets code read command-line arguments and quit the program
import json # reads json file and turns into a python dict

ROUTINES_FILE = "routines.json"

def notify(title, message):
    # native mac banner via AppleScript. osascript runs one line of script (-e).
    msg = message.replace('"', '\\"')      # don't let a quote break the script
    ttl = title.replace('"', '\\"')
    script = f'display notification "{msg}" with title "{ttl}"'
    subprocess.run(["osascript", "-e", script])

def load(path=ROUTINES_FILE):
    # read the json file into a python dict. friendly message if it's not there.
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"can't find {path} — make sure it's in this folder.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{path} has a syntax error: {e}")
        sys.exit(1)

def run_routine(name, routines):
    # look up the routine by name, then do its actions
    if name not in routines:
        avail = ", ".join(routines)
        raise KeyError(f"no routine named {name!r}. try one of: {avail}")
    r = routines[name]

    notify("Launcher", r["notify"])
    if r.get("clipboard"):                 # skip empty clipboard strings
        pyperclip.copy(r["clipboard"])

    print(f"ran routine: {name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python launcher.py <routine>   e.g. python launcher.py work")
        sys.exit(1)

    routines = load()
    run_routine(sys.argv[1], routines)