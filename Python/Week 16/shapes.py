import math
from vector3d import Vector3D
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

class Shape:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
    
    @property
    def pos(self):
        return self._pos

    @pos.setter                                     # checks if pos is Vector3D
    def pos(self, value):
        if not isinstance(value, Vector3D):
            raise TypeError("position must be a Vector3D")
        self._pos = value

    def update(self, dt, g=9.81):
        self.vel = self.vel + Vector3D(0, -g, 0) * dt
        self.pos = self.pos + self.vel * dt
    
    @staticmethod
    def collision_pair(a, b):
        """True if a and b collide (either direction)."""
        return a.collides_with(b) or b.collides_with(a)

    @staticmethod
    def clamp(value, lo, hi):
        """Pin value into [lo, hi]."""
        return max(lo, min(hi, value))

    def __repr__(self):
        name = type(self).__name__
        return f"{name}(pos={self.pos}, vel={self.vel})"
    

class Circle(Shape):
    def __init__(self, pos, vel, radius):
        super().__init__(pos, vel) 
        self.radius = radius

    @property
    def radius(self):
        return self._radius
    
    @radius.setter                          # checks if radius > 0 and numeric  
    def radius(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("radius must be numeric")
        if value <= 0:
            raise ValueError("radius must be > 0")
        self._radius = value

    @property
    def area(self):
        return math.pi * self.radius ** 2

    def collides_with(self, other):
        if isinstance(other, Circle):
            d = abs(self.pos - other.pos)
            return d < self.radius + other.radius
        elif isinstance(other, Box):
            dx = abs(self.pos.x - other.pos.x)
            dy = abs(self.pos.y - other.pos.y)
            return (dx < self.radius + other.width / 2
                and dy < self.radius + other.height / 2)
        return False
    
    @classmethod
    def unit(cls, pos):                             # unit circle at given position
        return cls(pos, Vector3D(0, 0, 0), 1.0)

    @classmethod
    def at_rest(cls, pos, radius):                  # zero velocity
        return cls(pos, Vector3D(0, 0, 0), radius)
    
class Box(Shape):
    def __init__(self, pos, vel, width, height):
        super().__init__(pos, vel)
        self.width = width
        self.height = height
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("width must be numeric")
        if value <= 0:
            raise ValueError("width must be > 0")
        self._width = value

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("height must be numeric")
        if value <= 0:
            raise ValueError("height must be > 0")
        self._height = value

    @property
    def area(self):
        return self._width * self._height

    def collides_with(self, other):
        if isinstance(other, Box):
            dx = abs(self.pos.x - other.pos.x)
            dy = abs(self.pos.y - other.pos.y)
            return (dx < (self.width + other.width) / 2
                and dy < (self.height + other.height) / 2)
        elif isinstance(other, Circle):
            dx = abs(self.pos.x - other.pos.x)
            dy = abs(self.pos.y - other.pos.y)
            return (dx < self.width / 2 + other.radius
                and dy < self.height / 2 + other.radius)
        return False
    
    @classmethod
    def square(cls, pos, vel, side):                # width = height = side
        return cls(pos, vel, side, side)
    
    @classmethod
    def at_rest(cls, pos, w, h):
        return cls(pos, Vector3D(0, 0, 0), w, h)
    
# wall bounce helper
def bounce_walls(s, x_min, x_max, y_min, y_max):
    
    # sets the edges in the case where s is a circle or s is a square
    if isinstance(s, Circle):
        ex = ey = s.radius
    else:
        ex, ey = s.width / 2, s.height / 2
    
    if s.pos.x - ex < x_min:                # check if shape's left edge went past left wall
        s.pos.x = x_min + ex                # push it back so the edge touches the wall
        s.vel.x = -s.vel.x                  # bounce: reverse speed direction of s

    if s.pos.x + ex > x_max:                # check if shape's right edge went past right wall
        s.pos.x = x_max - ex                # push it back so the edge touches the wall
        s.vel.x = -s.vel.x                  # bounce reverse speed direction of s
    
    if s.pos.y - ey < y_min:                # check if shape's bottom edge went past floor
        s.pos.y = y_min + ey                # push it back so the edge touches the floor
        s.vel.y = -s.vel.y                  # bounce: reverse speed direction of s
    
    if s.pos.y + ey > y_max:                # check if shape's top edge went past ceiling
        s.pos.y = y_max - ey                # push it back so the edge touches the floor
        s.vel.y = -s.vel.y                  # bounce: reverse speed direction of s

def main():
    # container setup
    X_MIN, X_MAX = -5, 5                    # left and right walls
    Y_MIN, Y_MAX = 0, 10                    # floor and ceiling
    DT = 0.02                               # time periods, per frame (seconds)

    # A mix of shapes
    shapes = [
        Circle(Vector3D(-2, 8, 0), Vector3D( 3,  0, 0), radius=0.5),
        Circle(Vector3D( 2, 7, 0), Vector3D(-2,  1, 0), radius=0.7),
        Box   (Vector3D( 0, 9, 0), Vector3D( 1,  0, 0), width=1.0, height=1.0),
        Box   (Vector3D(-3, 5, 0), Vector3D( 2,  1, 0), width=0.8, height=1.2),
    ]

    # creating elastic collision between two shapes
    def elastic(a, b):
        dx = b.pos.x - a.pos.x              # vector from a to b
        dy = b.pos.y - a.pos.y
        distance = (dx*dx + dy*dy) ** 0.5   # distance between centers
        if distance == 0: 
            return                          # skips function if shapes overlap
        nx, ny = dx/distance, dy/distance   # unit vector conversion
        va_n = a.vel.x*nx + a.vel.y*ny      # a's speed along the line
        vb_n = b.vel.x*nx + b.vel.y*ny      # b's speed along the line
        if vb_n - va_n >= 0:                # ensures elastic collisions
            return  
        delta_v = vb_n - va_n
        a.vel.x += delta_v * nx
        a.vel.y += delta_v * ny
        b.vel.x -= delta_v * nx
        b.vel.y -= delta_v * ny
    
    # matplotlib figure
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_aspect('equal')
    ax.set_title("2D Shape Physics Sandbox")

    # one patch per shape, drawn once, moved each frame)
    artists = []
    for s in shapes:
        if isinstance(s, Circle):
            p = patches.Circle((s.pos.x, s.pos.y), s.radius, fill=False, lw=2)
        else:
            p = patches.Rectangle((s.pos.x - s.width/2, s.pos.y - s.height/2),
                                  s.width, s.height, fill=False, lw=2)
        ax.add_patch(p)
        artists.append(p)
    
    # one animation step
    def step(frame):
        # 1. move every shape
        for s in shapes:
            s.update(DT)
            bounce_walls(s, X_MIN, X_MAX, Y_MIN, Y_MAX)
        # 2. check every pair for collision
        for a, b in itertools.combinations(shapes, 2):
            if a.collides_with(b):
                elastic(a, b)
        # 3. push new positions into the drawn patches
        for s, art in zip(shapes, artists):
            if isinstance(s, Circle):
                art.center = (s.pos.x, s.pos.y)
            else:
                art.set_xy((s.pos.x - s.width/2, s.pos.y - s.height/2))
        return artists
    
    anim = FuncAnimation(fig, step, frames=600, interval=20, blit=False)
    plt.show()

if __name__=="__main__":
    main()