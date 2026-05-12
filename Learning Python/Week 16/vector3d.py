import math

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            print("Vector cannot be normalized since the vector is a zero vector")
        else:
            return Vector3D(self.x / mag, self.y / mag, self.z / mag)
        
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"

v = Vector3D(1, 2, 3)
print(v)
print(v.magnitude())
u = Vector3D(1, 0, 0)
w = Vector3D(0, 1, 0)
print(u.dot(w))
n = v.normalize()
print(n)
print(n.magnitude())