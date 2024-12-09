from components.vector import Vector2D
from components.body import Body, Polygon, Rectangle, Circle

def obb_collision(obb_1: Rectangle, obb_2: Rectangle):
    axes = obb_1.get_axes() + obb_2.get_axes()
    vertices1 = obb_1.get_vertices()
    vertices2 = obb_2.get_vertices()
    
    for axis in axes:
        axis = axis.normalize()
        
        min1, max1 = project_vertices(vertices1, axis)
        min2, max2 = project_vertices(vertices2, axis)
        
        if max1 < min2 or max2 < min1:
            return False
    
    return True

def polygons_collision(polygon_1: Polygon, polygon_2: Polygon):
    vertices1 = polygon_1.get_vertices()
    vertices2 = polygon_2.get_vertices()

    axes = []

    for i in range(len(vertices1)):
        va = vertices1[i]
        vb = vertices1[(i + 1) % len(vertices1)]
        
        edge = vb - va
        
        axis = Vector2D(-edge.y, edge.x).normalize()
        axes.append(axis)

    for i in range(len(vertices2)):
        va = vertices2[i]
        vb = vertices2[(i + 1) % len(vertices2)]
        
        edge = vb - va
        
        axis = Vector2D(-edge.y, edge.x).normalize()
        
    for axis in axes:
        min_a, max_a = project_vertices(vertices1, axis)
        min_b, max_b = project_vertices(vertices2, axis)

        if min_a >= max_b or min_b >= max_a:
            return False

    return True

def polygon_circle_collision(polygon: Polygon, circle: Circle):
    assert polygon.shape_type == "Polygon" and circle.shape_type == "Circle", \
        "Shape types of polygon and circle must be 'Polygon' and 'Circle' respectively."
    
    vertices = polygon.get_vertices()
    
    for i in range(len(vertices)):
        va = vertices[i]
        vb = vertices[(i + 1) % len(vertices)]

        edge = vb - va

        axis = Vector2D(-edge.y, edge.x).normalize()
       
        min_a, max_a = project_vertices(vertices, axis)
        min_b, max_b = project_circle(circle.center, circle.radius, axis)
        
        if max_a <= min_b or max_b <= min_a:
            return False
    
    cp_index = find_closest_point_on_polygon(circle.center, vertices)
    
    cp = vertices[cp_index]
    
    axis = (cp - circle.center).normalize()

    min_a, max_a = project_circle(circle.center, circle.radius, axis)
    min_b, max_b = project_vertices(vertices, axis)

    if max_a <= min_b or max_b <= min_a:
        return False
    
    return True


def project_vertices(vertices: list[Vector2D], axis: Vector2D):
    min_proj = float('inf')
    max_proj = float('-inf')

    for v in vertices:
        proj = v.dot(axis)

        if proj < min_proj:
            min_proj = proj
        if proj > max_proj:
            max_proj = proj

    return min_proj, max_proj

def project_circle(center, radius: float, axis: Vector2D):
    direction = axis.normalize()
    direction_and_radius = direction * radius

    p1 = center + direction_and_radius
    p2 = center - direction_and_radius
    
    min_proj = p1.dot(axis)
    max_proj = p2.dot(axis)
    
    if min_proj > max_proj:
        min_proj, max_proj = max_proj, min_proj

    return min_proj, max_proj

def find_closest_point_on_polygon(circle_center: Vector2D, vertices: list[Vector2D]):
    result = -1
    min_distance = float('inf')

    for i, v in enumerate(vertices):
        dist = Vector2D.distance(v, circle_center)

        if dist < min_distance:
            min_distance = dist
            result = i
    
    return result

#################################################################################################################

def collide(body_1: Body, body_2: Body):
    if isinstance(body_1, Rectangle) and isinstance(body_2, Rectangle):
        is_collision = obb_collision(body_1, body_2)
    elif body_1.shape_type == "Polygon" and body_2.shape_type == "Circle":
        is_collision = polygon_circle_collision(body_1, body_2)
    elif body_1.shape_type == "Circle" and body_2.shape_type == "Polygon":
        is_collision = polygon_circle_collision(body_2, body_1)
    elif body_1.shape_type == "Circle" and body_2.shape_type == "Circle":
        is_collision = circles_collision(body_1, body_2)
    else :
        is_collision = polygons_collision(body_1, body_2)

    if not is_collision:
        return None
    
    if body_1.shape_type == "Polygon" and body_2.shape_type == "Polygon":
        contact_points = polygons_contact_points(body_1, body_2)
    elif body_1.shape_type == "Circle" and body_2.shape_type == "Circle":
        contact_points = circles_contact_points(body_1, body_2)
    elif body_1.shape_type == "Polygon" and body_2.shape_type == "Circle":
        contact_points = polygon_circle_contact_points(body_1, body_2)
    elif body_1.shape_type == "Circle" and body_2.shape_type == "Polygon":
        contact_points = polygon_circle_contact_points(body_2, body_1)

    return contact_points

def point_to_line_segment_projection(point: Vector2D, a: Vector2D, b: Vector2D):
    ab = b - a
    ap = point - a
    
    proj = ap.dot(ab)
    d = proj / ab.dot(ab)

    if d <= 0:
        contact_point = a
    elif d >= 1:
        contact_point = b
    else: 
        contact_point = a + ab * d

    distance = Vector2D.distance(contact_point, point)

    return contact_point, distance

def polygons_contact_points(polygon_1: Polygon, polygon_2: Polygon):
    epsilon = 0.0005
    min_distance = float('inf')
    contact_point_1 = None
    contact_point_2 = None

    for i in range(len(polygon_1.get_vertices())):
        vp = polygon_1.get_vertices()[i]
        for j in range(len(polygon_2.get_vertices())):
            va = polygon_2.get_vertices()[j]
            vb = polygon_2.get_vertices()[(j + 1) % len(polygon_2.get_vertices())]

            cp, distance = point_to_line_segment_projection(vp, va, vb)

            if contact_point_1 is not None and abs(distance - min_distance) < epsilon and not cp.distance_to(contact_point_1) < epsilon:
                contact_point_2 = cp
            elif distance < min_distance:
                min_distance = distance
                contact_point_2 = None
                contact_point_1 = cp

    for i in range(len(polygon_2.get_vertices())):
        vp = polygon_2.get_vertices()[i]
        for j in range(len(polygon_1.get_vertices())):
            va = polygon_1.get_vertices()[j]
            vb = polygon_1.get_vertices()[(j + 1) % len(polygon_1.get_vertices())]

            cp, distance = point_to_line_segment_projection(vp, va, vb)

            if contact_point_1 is not None and abs(distance - min_distance) < epsilon and not cp.distance_to(contact_point_1) < epsilon:
                contact_point_2 = cp
            elif distance < min_distance:
                min_distance = distance
                contact_point_2 = None
                contact_point_1 = cp

    return [cp for cp in [contact_point_1, contact_point_2] if cp is not None]

def polygon_circle_contact_points(polygon: Polygon, circle: Circle):
    min_distance = float('inf')
    vertices = polygon.get_vertices()
    
    for i in range(len(vertices)):
        va = vertices[i]
        vb = vertices[(i + 1) % len(vertices)]

        cp, distance = point_to_line_segment_projection(circle.center, va, vb)

        if distance < min_distance:
            min_distance = distance
            contact_point = cp
        
    return [contact_point]

def circles_contact_points(body_1: Circle, body_2: Circle):
    normal = (body_2.center - body_1.center).normalize()

    contact_point = body_1.center + normal * body_1.radius

    return [contact_point]

def circles_collision(body_1: Circle, body_2: Circle):
    assert body_1.shape_type == "Circle" and body_2.shape_type == "Circle", \
        "Both body_1 and body_2 must be of shape_type 'Circle' for Circle collision."
    
    distance = Vector2D.distance(body_1.center, body_2.center)

    if distance >= body_1.radius + body_2.radius:
        return False
    
    return True
                