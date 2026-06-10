import time, schedule # time-triggered routines
import subprocess # run shell + osascript
import pyperclip # clipboard read/write
import sys, json # cli args + read config

ROUTINES_FILE = "routines.json"

# os_bridge
class OSBridgeError(Exception):
    pass

def run_shell(cmd):
    # run a command (list of args), return (stdout, exit_code)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 and res.stderr:
        print(f"[os_bridge] {' '.join(cmd)} → exit {res.returncode}")
        print(f"[os_bridge] {res.stderr.strip()}")
    return res.stdout, res.returncode

def launch_app(name):
    # open a mac app by name, same as `open -a <name>`
    _, rc = run_shell(["open", "-a", name])
    if rc != 0:
        raise OSBridgeError(f"could not launch app: {name!r}")

def open_url(url):
    # open a url in the default browser
    _, rc = run_shell(["open", url])
    if rc != 0:
        raise OSBridgeError(f"could not open url: {url!r}")

def osa(script):
    # run one line of applescript via osascript -e
    out, rc = run_shell(["osascript", "-e", script])
    if rc != 0:
        raise OSBridgeError(f"applescript failed: {script!r}")
    return out.strip()

def safari_tab(url):
    # open a url in a new safari tab (launches safari if needed)
    osa(f'tell application "Safari" to open location "{url}"')

def notify(title, body):
    # native mac banner. escape quotes so they don't break the script
    body = body.replace('"', '\\"'); title = title.replace('"', '\\"')
    osa(f'display notification "{body}" with title "{title}"')

def spotify_play(uri=None):
    # launch spotify, then play. pass a uri (e.g. "spotify:playlist:...") to pick one
    # NOTE: i'm fairly sure `play track "<uri>"` works for playlists too — verify against
    # your spotify; if it errors, fall back to plain play and start the playlist by hand.
    launch_app("Spotify")
    osa(f'tell application "Spotify" to play track "{uri}"' if uri
        else 'tell application "Spotify" to play')

# action handlers
# each handler takes the action dict and reads what it needs off it.
def act_app(a): launch_app(a["value"])
def act_url(a): open_url(a["value"])
def act_safari(a): safari_tab(a["value"])
def act_clip(a): pyperclip.copy(a["value"])
def act_notify(a): notify("Launcher", a["value"])
def act_spotify(a): spotify_play(a.get("value"))

# the dispatch table: maps a "type" string to its handler.
# adding a new action = add one function + one entry here. the json never changes shape.
ACTIONS = {
    "app": act_app,
    "url": act_url,
    "safari": act_safari,
    "clip": act_clip,
    "notify": act_notify,
    "spotify": act_spotify,
}

# config
def load(path=ROUTINES_FILE):
    # read the json file into a python dict, with friendly errors
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"can't find {path} — make sure it's in this folder.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{path} has a syntax error: {e}")
        sys.exit(1)

# the runner
def run_routine(name, routines):
    # look up the routine, then walk its actions and dispatch each by "type"
    if name not in routines:
        avail = ", ".join(k for k in routines if not k.startswith("_"))
        raise KeyError(f"no routine named {name!r}. try one of: {avail}")

    for a in routines[name].get("actions", []):
        fn = ACTIONS.get(a["type"])
        if fn is None: # unknown type → warn + skip, don't crash
            print(f"skipping unknown action type: {a['type']!r}")
            continue
        fn(a)

    print(f"ran routine: {name}")

def run_schedule(routines):
    # register every job in the "_schedule" block, then loop forever firing due ones
    jobs = routines.get("_schedule", [])
    if not jobs:
        print('no "_schedule" block in routines.json'); return
    for job in jobs:
        schedule.every().day.at(job["at"]).do(run_routine, job["routine"], routines)
        print(f"scheduled {job['routine']} at {job['at']}")
    print("running… ctrl+c to stop")
    while True:
        schedule.run_pending()
        time.sleep(1)              # check once a second so the cpu doesn't pin at 100%

# triggers
if __name__ == "__main__":
    routines = load()
    if len(sys.argv) < 2:
        print("usage: python3 launcher.py <routine> | --schedule")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "--schedule":
        run_schedule(routines)     # time-triggered
    else:
        run_routine(arg, routines) # cli-triggered, by name