import math

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    @property
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self):
        mag = self.magnitude
        if mag == 0:
            return False
        else:
            return Vector3D(self.x / mag, self.y / mag, self.z / mag)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"
    
    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar):
        return self * scalar
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __abs__(self):
        return self.magnitude
    
    def __len__(self):
        return 3
    
a = Vector3D(1, 2, 3)
b = Vector3D(4, 5, 6)
print(a + b)
print(b - a)
print(a * 3)
print(3 * a) # __rmul__ check
print(a == Vector3D(1, 2, 3))
print(a == b)
print(a.magnitude) # no parens
print(abs(a))
print(len(a))