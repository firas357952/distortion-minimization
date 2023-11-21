import random

from geometry_tools import Point, Polygon, Triangle

# define a triangle

p1 = Point(1, 2)
p2 = Point(2, 3)
p3 = Point(2, 4)
m = Point(1, 3)
triangle = Triangle([p1, p2, p3])

# Theoretical value

theoretical_value = triangle.average_square_distance(m) / triangle.area
print("Theoretical value", theoretical_value)


# using Monte Carlo
def estimate(cls, shape, point, N=1000):
    practical_value = 0

    for _ in range(N):
        random_point = cls.random_point_in_shape(shape)
        practical_value += point.distance(random_point) ** 2

    return practical_value / N


practical_value = estimate(Triangle, triangle, m)
print("Practical value", practical_value)
print(abs(theoretical_value - practical_value) < 10 ** (-1))

print("----------------------------------")

# test for random triangles
print("Test Triangles")
nbr_test = 100
i = 0
for _ in range(nbr_test):
    triangle = Triangle(
        [Point(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(3)]
    )
    point = Point(random.uniform(0, 100), random.uniform(0, 100))
    theoretical_value = triangle.average_square_distance(point) / triangle.area
    estimation = estimate(Triangle, triangle, point)
    error = abs(theoretical_value - estimation) / estimation
    if error > 0.05:
        print(error)
        i += 1
print(i, "error(s)")

print("----------------------------------")

# test for random polygons
print("Test polygons")
nbr_test = 100
i = 0
for _ in range(nbr_test):
    nbr_vertices = random.randint(3, 10)
    polygon: Polygon = Polygon(
        [
            Point(random.uniform(0, 100), random.uniform(0, 100))
            for _ in range(nbr_vertices)
        ]
    ).convex_hull
    point = Point(random.uniform(0, 100), random.uniform(0, 100))
    theoretical_value = polygon.average_square_distance(point) / polygon.area
    estimation = estimate(Polygon, polygon, point)
    error = abs(theoretical_value - estimation) / estimation
    x, y = zip(*polygon.exterior.coords)
    if error > 0.05:
        print(error)
        i += 1
print(i, "error(s)")
