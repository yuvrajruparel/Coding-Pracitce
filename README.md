# Python Learning Program
## Current Level in Python: Weeks 1-15 Solid Foundation
Elements worked with: Operators, strings, conditionals, loops, functions, built in functions, lists, tuples, sets, dictionaries, arrays, linked lists, plotting, curve fitting, multidimensional audio <br>
Libraries worked with: Numpy, Matplotlib, Sound Device
* ISS Deorbit Project: takes real time data from the International Space Station, plots its deorbit ground track over a chosen time window
* DNA Translator: protein translation, reads a DNA scodon sequence and outputs the corresponding amino acid chain
* Cantilever beam deflection: computes deflection along a cantilever beam under given loading conditions
* Unit converter: converts values between length, mass, and temperature units
* Pig Latin translator: takes English input and returns the Pig Latin version
## Week 16 (May 11th/2026 - May 17th/2026): OOP Fundamentals
<table border="1">
  <tr>
    <th>Date</th>
    <th>Topic</th>
    <th>What I learnt</th>
    <th>Mini Project</th>
  </tr>
  <tr>
    <td>05/11/2026</td>
    <td>OOP Fundamentals</td>
    <td>Classes, instance vs class attributes, methods</td> 
    <td>Vector3D: program with magnitude, dot product, normalize</td>
  </tr>
  <tr>
    <td>05/12/2026</td>
    <td>Operator Overloading</td>
    <td>Dunders: add, sub, mul, rmul, eq, abs, len, @property</td> 
    <td>Upgraded Vector3D with all operators and magnitude as property</td>
  </tr>
  <tr>
    <td>05/13/2026</td>
    <td>Inheritance and Composition</td>
    <td>D"Is-a" vs "has-a", super(), subclassing, building objects</td> 
    <td>2D Shape Physics Sandbox: Shape base composed of Vector3D, subclassed into circle, box, with gravity, walls, and elastic collisions (matplotlib)</td>
  </tr>
  <tr>
    <td>05/14/2026</td>
    <td>Properties, Class & Static Methods</td>
    <td>@property setters with validation, @classmethod, @staticmethod</td> 
    <td>Extended Shape module: validated dims (negative raise), factory constructors (Box.square, Circle.unit), static helpers</td>
  </tr>
  <tr>
    <td>05/15/2026</td>
    <td>Exceptions & Error Handling</td>
    <td>try/except/else/finally, raise/re-raise/raise from, custom exceptions</td>
    <td>Hardened shapes.py & vector3d.py: exceptions.py module (ShapeError, InvalidDimensionError, VectorError), fixed silent normalize() bug, sandbox loop recovers from bad frames</td>
  </tr>
</table>

### Weekend Project: Spring-Mass-Damper Sandbox
A spring-mass-damper is a model of a vibrating system — a block attached to a spring with some friction slowing it down. It shows up everywhere from car suspensions to building sway. I created an interactive simulation of a 1-DOF mass spring damper system. Newton's 2nd Law cast into a state space form and integrated with RK4 method. 

Saturday: Built the model using a matplotlib view system, with sliders, and radio buttons for forcing type.

Sunday: Built pygame model, with sliders, radio buttons, and a physical simulation of the spring-mass damper. 
## Week 17 (May 18th/2026 - May 24th/2026): Pygame
<table border="1">
  <tr>
    <th>Date</th>
    <th>Topic</th>
    <th>What I learnt</th>
    <th>Mini Project</th>
  </tr>
  <tr>
    <td>05/18/2026</td>
    <td>Pygame Fundamentals</td>
    <td>Surfaces, event loop, input→update→draw, clock.tick</td>
    <td>Bouncing Ball: 3 balls in a list, space-bar pause, arrow-key velocity nudge, translucent trail, random RGB on wall hit</td>
  </tr>
  <tr>
    <td>05/19/2026</td>
    <td>Sprite & Group</td>
    <td>pygame.sprite.Sprite, image+rect, Group container, batched update()/draw()</td>
    <td>Bouncing Balls v2: 50 sprites in a Group, space-bar pause, arrow-key velocity nudge, random RGB on wall hit</td>
  </tr>
  <tr>
    <td>05/20/2026</td>
    <td>Collisions</td>
    <td>colliderect, spritecollide(dokill), Sprite vs Group, rect-based hit detection</td>
    <td>Brick-Breaker Prototype: 8×5 brick wall, mouse paddle, return reset, space pause, angle-nudge bounce on paddle hit</td>
  </tr>
  <tr>
  <td>05/21/2026</td>
  <td>Sound and Animation</td>
  <td>pygame.mixer (Sound vs music), pre_init, play/pause/loop, frame-based animation, playing flag, dt timing</td>
  <td>Brick-Breaker v2: hit/break/lose/win sfx, looping bg music, paddle squish animation (5 frames, 80ms) on ball hit</td>
  </tr>
  <tr>
  <td>05/22/2026</td>
  <td>Scene State Machine</td>
  <td>Scene base class (handle_event/update/draw), SceneManager with go_to(), polymorphic dispatch, scene swapping, thin main loop pattern</td>
  <td>Brick-Breaker v3: Menu/Play/GameOver scenes, pause overlay, +10/brick score with center watermark, mm:ss.cs timer, return-driven flow</td>
  </tr>
</table>

### Weekend Project: Mini Videogame Arcade
Using pygame to create an online Arcade with 3 classic games, Brick Breaker, Pong, and Asteroids Lite. I integrated animations, sound systems, different scenes to represent a Game Menu, Win/Lose Scene, and a Main menu that can access all 3 games, with buttons to select the game to play.

Saturday: Built the Pong game against AI Bot, completely equipped with sounds, animations, and all other features

Sunday: Built Asteroids-Lite, a more visual game, and Main Menu that links all three games
## Week 18 (June 1st/2026 - June 7th/2026): Desktop Automation
<table border="1">
  <tr>
    <th>Date</th>
    <th>Topic</th>
    <th>What I learnt</th>
    <th>Mini Project</th>
  </tr>
  <tr>
    <td>06/01/2026</td>
    <td>Decorators</td>
    <td>@decorator syntax, *args/**kwargs forwarding, functools.wraps, closures, lambda/map/filter</td>
    <td>decorators_lab.py: @timer, @retry(n), @log_calls — applied to dummy functions to verify wrapping and metadata preservation</td>
  </tr>
  <tr>
    <td>06/02/2026</td>
    <td>Talking to the OS</td>
    <td>subprocess.run, stdout/stderr/returncode, list-args vs shell=True, open -a, osascript -e</td>
    <td>os_bridge.py: run_shell helper, launch_app/open_url, osa() AppleScript wrapper, notify() and safari_tab() built on top</td>
  </tr>
  <tr>
    <td>06/03/2026</td>
    <td>pyautogui + global hotkeys</td>
    <td>moveTo/click, typewrite, global hotkeys, FAILSAFE, macOS Accessibility + Input Monitoring perms</td>
    <td>hotkey_demo.py: cmd+shift+1 types email, cmd+shift+2 clicks center, esc quits; pynput GlobalHotKeys after keyboard lib failed on mac</td>
  </tr>
  <tr>
      <td>06/04/2026</td>
      <td>autoclicker build</td>
      <td>threading daemon loops, cps timing, hold-to-spam, decorator-registered hotkeys</td>
      <td>autoclicker.py: ctrl+shift+s toggle, ctrl+shift+up/down cps, hold 'r' minecraft, esc quits; pynput single-listener after two listeners crashed on mac</td>
    </tr>
    <tr>
    <td>06/05/2026</td>
    <td>screenbot build</td>
    <td>locateOnScreen matching, retina coord fix, applescript window focus</td>
    <td>screen_bot.py: locates cropped png, clicks center; cmd+shift+f toggles safari/notes via applescript; retina 2x fix physical→logical coords; esc quits</td>
  </tr>
</table>