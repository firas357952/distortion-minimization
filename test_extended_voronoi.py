import random

import numpy as np
from matplotlib import pyplot as plt

from extended_voronoi import ExtendedVoronoi
from geometry_tools import Point, Polygon

N_prototypes = 20

points = np.array(
    [(random.uniform(10, 90), random.uniform(10, 90)) for _ in range(N_prototypes)]
)

boundary = np.array([[0, 0], [100, 0], [100, 100], [0, 100]])

x, y = boundary.T
plt.xlim(round(x.min() - 1), round(x.max() + 1))
plt.ylim(round(y.min() - 1), round(y.max() + 1))
plt.plot(*points.T, "b.")

diameter = np.linalg.norm(boundary.ptp(axis=0))
points = Point.coords_to_points(points)
boundary_polygon = Polygon(boundary)

polygon_list = ExtendedVoronoi.region_split(boundary_polygon, points, diameter)
for point, p in polygon_list:
    print(p, "\n")
    x, y = zip(*p.exterior.coords)
    plt.plot(x, y, "r-")

plt.show()
