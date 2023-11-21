from geometry_tools import Line, Point, Polygon, Triangle, Vector

# Define points
p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(2, 3)
p4 = Point(2, 4)
m = Point(1, 3)

print(p1 == p2)
print(p1 == p3)
print(p1.distance(p3))
print(p1.closest_point([p3, p4, m]))

print("----------------------------------")

# Create a line
l = Line(p1, p3)
print("Projection", l.get_projection_coordinate(m))
print("Projection", l.get_projection_coordinate(p2))
print("perpendicular line", l.perpendicular_line(p4))

print("----------------------------------")

# Create a vector
v = Vector(p1, p3)
print("vector", v)
print("norm", v.norm)
print("normal vector", v.normal_vector())

print("----------------------------------")

# Create a triangle
triangle = Triangle([p1, p3, p4])

# Calculate surface area
area = triangle.area
print("Surface Area:", area)

# Calculate center of mass
g = triangle.centroid
print("Center of Mass:", g.x, g.y)

# Calculate average square distance
avg_sq_distance = triangle.average_square_distance(m)
print("Average Square Distance:", avg_sq_distance)

print("----------------------------------")

# Create a polygon
polygon = Polygon([p1, p3, p4, m])

# Calculate surface area
area = polygon.area
print("Surface Area:", area)

# Calculate center of mass
g = polygon.centroid
print("Center of Mass:", g.x, g.y)

# Calculate average square distance
avg_sq_distance = polygon.average_square_distance(m)
print("Average Square Distance:", avg_sq_distance)
