import subprocess
from typing import Sequence

# exceptions
class OSBridgeError(Exception): # A shell command or AppleScript invocation exited non-zero."""
    pass

# core primitive
def run_shell(cmd: Sequence[str]) -> tuple[str, int]: # Run a command (passed as a list of args) and return its output.
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0 and result.stderr:
        print(f"[os_bridge] {' '.join(cmd)} → exit {result.returncode}")
        print(f"[os_bridge] stderr: {result.stderr.strip()}")

    return result.stdout, result.returncode

# app launching
def launch_app(name: str) -> None: # Open a macOS app by name. Equivalent to `open -a <name>`
    _, rc = run_shell(["open", "-a", name])
    if rc != 0:
        raise OSBridgeError(f"could not launch app: {name!r}")

def open_url(url: str) -> None: # Open a URL in the default browser
    _, rc = run_shell(["open", url])
    if rc != 0:
        raise OSBridgeError(f"could not open url: {url!r}")

# AppleScript bridge
def osa(script: str) -> str: # Run one line of AppleScript via `osascript -e` and return stdout.
    out, rc = run_shell(["osascript", "-e", script])
    if rc != 0:
        raise OSBridgeError(f"applescript failed: {script!r}")
    return out.strip()

def notify(title: str, body: str) -> None:
    """Fire a native macOS notification banner."""
    script = f'display notification "{body}" with title "{title}"'
    osa(script)

def safari_tab(url: str) -> None:
    """Open a URL in a new Safari tab (launches Safari if not running)."""
    script = f'tell application "Safari" to open location "{url}"'
    osa(script)

# smoke test
def main():
    print("--- os_bridge smoke test ---")

    # 1. plain shell command
    out, rc = run_shell(["whoami"])
    print(f"whoami → {out.strip()}  (exit {rc})")

    # 2. launch an app
    print("launching Safari…")
    launch_app("Safari")

    # 3. open a URL in a Safari tab via AppleScript
    print("opening duke.edu in a new Safari tab…")
    safari_tab("https://duke.edu")

    # 4. notification banner
    print("firing notification…")
    notify("os_bridge", "Smoke test complete.")

    print("done")

if __name__ == "__main__":
    main()