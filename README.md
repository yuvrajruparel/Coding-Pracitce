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
A spring-mass-damper is the simplest model of a vibrating system — a block attached to a spring with some friction slowing it down. It's the standard textbook example for studying how things oscillate, settle, and resonate, and shows up everywhere from car suspensions to building sway. Created interactive simulation of a 1-DOF mass spring damper system. Newton's 2nd Law cast into a state space form and integrated with RK4 method. 

Saturday: Built the model using a matplotlib view system, with sliders for m/k/c/x₀/v₀/A/ω_f, and radio buttons for forcing type (free/step/sin).

Sunday: Built the model using a pygame view system, with sliders, radio buttons, and a physical simulation of the spring-mass damper. 