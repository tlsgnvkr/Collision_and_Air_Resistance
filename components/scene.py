from components.body import Body
from components.collision import collide

class Scene:
    def __init__(self, bodies: list[Body]):
        self.bodies: list[Body] = bodies
        self._contact_points = []
        self.crashed_objects = []

    def add(self, body: Body):
        self.bodies.append(body)

    def remove(self, i):
        del self.bodies[i]

    def update_position(self, dt):
        for body in self.bodies:
            body.center += body.velocity * dt
            body.angle += body.angular_velocity * dt

    def handle_collisions(self):
        collided_walls_1 = []
        for i in range(2, len(self.bodies)):
            contact_points = collide(self.bodies[0], self.bodies[i])
            if contact_points: collided_walls_1.append(i)

        collided_walls_2 = []
        for i in range(2, len(self.bodies)):
            contact_points = collide(self.bodies[1], self.bodies[i])
            if contact_points: collided_walls_2.append(i)

        collided_balls = False
        contact_points = collide(self.bodies[0], self.bodies[1])
        if contact_points: collided_balls = True
        
        return [collided_walls_1, collided_walls_2, collided_balls]

    def step(self, dt):
        self.update_position(dt)
        return self.handle_collisions()
