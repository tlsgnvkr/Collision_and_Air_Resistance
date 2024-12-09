import math
from components.vector import Vector2D

class Body():
    def __init__(self, x, y, name = None):
        self.center = Vector2D(x, y)
        self.angle = 0
        self.name = name
        self.shape_type = None
        self.velocity = Vector2D(0, 0)
        self.angular_velocity = 0

class Rectangle(Body):
    def __init__(self, x, y, width, height, name = None):
        super().__init__(x, y, name)
        self.width = width
        self.height = height
        self.shape_type = "Polygon"
        half_width = self.width / 2
        half_height = self.height / 2

        self.local_vertices = [
            Vector2D(-half_width, -half_height),
            Vector2D(half_width, -half_height),
            Vector2D(half_width, half_height),
            Vector2D(-half_width, half_height)
        ]

    def get_axes(self):
        self.x_axis = Vector2D(math.cos(self.angle), math.sin(self.angle))
        self.y_axis = Vector2D(-math.sin(self.angle), math.cos(self.angle))

        return [self.x_axis, self.y_axis]

    def get_vertices(self):
        return [vertex.rotate(self.angle).add(self.center) for vertex in self.local_vertices]

    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self.angle += angle

class Polygon(Body):
    def __init__(self, x, y, vertices: list[Vector2D, list, tuple], name=None):
        super().__init__(x, y, name)
        centroid = (
            sum(vertex[0] for vertex in vertices) / len(vertices),
            sum(vertex[1] for vertex in vertices) / len(vertices),
        )

        self.local_vertices = [Vector2D(vertex[0] - centroid[0], vertex[1] - centroid[1]) for vertex in vertices]
        self.shape_type = "Polygon"

    def get_vertices(self):
        return [vertex.rotate(self.angle).add(self.center) for vertex in self.local_vertices]

    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self.angle += angle

class Circle(Body):
    def __init__(self, x, y, radius, mass, name = None):
        super().__init__(x, y, name)
        self.radius = radius
        self.shape_type = "Circle"
        self.mass = mass

    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self.angle += angle
