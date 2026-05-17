class ShapeError(Exception):
    """Base for all shapes.py errors."""

class InvalidDimensionError(ShapeError):
    """Negative, zero, or non-numeric size."""

class CollisionError(ShapeError):
    """Comparing incompatible shape types."""

class VectorError(Exception):
    """Base for vector3d.py errors."""