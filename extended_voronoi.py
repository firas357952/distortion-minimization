from collections import defaultdict

import numpy as np
from scipy.spatial import Voronoi

from geometry_tools import Polygon, Point


class ExtendedVoronoi:
    def voronoi_polygons(voronoi, diameter: float):
        """Generate shapely.geometry.Polygon objects corresponding to the
        regions of a scipy.spatial.Voronoi object, in the order of the
        input points. The polygons for the infinite regions are large
        enough that all points within a distance 'diameter' of a Voronoi
        vertex are contained in one of the infinite polygons.

        """
        centroid = voronoi.points.mean(axis=0)

        # Mapping from (input point index, Voronoi point index) to list of
        # unit vectors in the directions of the infinite ridges starting
        # at the Voronoi point and neighbouring the input point.
        ridge_direction = defaultdict(list)
        for (p, q), rv in zip(voronoi.ridge_points, voronoi.ridge_vertices):
            u, v = sorted(rv)
            if u == -1:
                # Infinite ridge starting at ridge point with index v,
                # equidistant from input points with indexes p and q.
                t = voronoi.points[q] - voronoi.points[p]  # tangent
                n = np.array([-t[1], t[0]]) / np.linalg.norm(t)  # normal
                midpoint = voronoi.points[[p, q]].mean(axis=0)
                direction = np.sign(np.dot(midpoint - centroid, n)) * n
                ridge_direction[p, v].append(direction)
                ridge_direction[q, v].append(direction)

        for i, r in enumerate(voronoi.point_region):
            region = voronoi.regions[r]
            if -1 not in region:
                # Finite region.
                yield Polygon(voronoi.vertices[region])
                continue
            # Infinite region.
            inf = region.index(-1)  # Index of vertex at infinity.
            j = region[(inf - 1) % len(region)]  # Index of previous vertex.
            k = region[(inf + 1) % len(region)]  # Index of next vertex.
            if j == k:
                # Region has one Voronoi vertex with two ridges.
                dir_j, dir_k = ridge_direction[i, j]
            else:
                # Region has two Voronoi vertices, each with one ridge.
                (dir_j,) = ridge_direction[i, j]
                (dir_k,) = ridge_direction[i, k]

            # Length of ridges needed for the extra edge to lie at least
            # 'diameter' away from all Voronoi vertices.
            length = 3 * diameter / np.linalg.norm(dir_j + dir_k)

            # Polygon consists of finite part plus an extra edge.
            finite_part = voronoi.vertices[region[inf + 1 :] + region[:inf]]
            extra_edge = [
                voronoi.vertices[j] + dir_j * length,
                voronoi.vertices[k] + dir_k * length,
            ]
            yield Polygon(np.concatenate((finite_part, extra_edge)))

    @staticmethod
    def region_split(boundary_polygon: Polygon, points, diameter: float):
        polygon_list = []
        vor = Voronoi(Point.points_to_coords(points))
        voronoi_polygons = ExtendedVoronoi.voronoi_polygons(vor, diameter)

        for p in voronoi_polygons:
            points_in = [point for point in points if p.contains(point._point)]

            if len(points_in) != 1:
                raise ValueError(
                    "Error in splitting: Expected 1 point, found", len(points_in)
                )

            intersection = p.intersection(boundary_polygon)
            polygon_list.append((points_in[0], intersection))

        return polygon_list
