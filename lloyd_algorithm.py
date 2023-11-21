import random

import numpy as np

from extended_voronoi import ExtendedVoronoi
from geometry_tools import Point, Polygon


class LloydAlgorithm:
    def __init__(self, boundary, num_points):
        self.boundary = np.array(boundary)
        self.boundary_polygon = Polygon(self.boundary)
        self.num_points = num_points
        self.prototypes = self.generate_random_points()
        self.polygon_list = self.voronoi_partition()
        self.distortion = self.calculate_distortion()

    def generate_random_points(self):
        return [
            Point(
                random.uniform(self.boundary[0][0], self.boundary[2][0]),
                random.uniform(self.boundary[0][1], self.boundary[2][1]),
            )
            for _ in range(self.num_points)
        ]

    def voronoi_partition(self):
        raise NotImplementedError("Subclasses must implement voronoi_partition method")

    def compute_centroids(self, polygon_list):
        raise NotImplementedError("Subclasses must implement compute_centroids method")

    def calculate_distortion(self):
        raise NotImplementedError(
            "Subclasses must implement calculate_distortion method"
        )

    def update_points(self, centroids):
        self.prototypes = centroids

    def single_iteration(self):
        centroids = self.compute_centroids(self.polygon_list)
        self.update_points(centroids)
        self.polygon_list = self.voronoi_partition()
        self.distortion = self.calculate_distortion()

    def run_simulation(self, num_iterations=None):
        iteration = 1
        try:
            while True:
                self.single_iteration()
                print(f"Iteration {iteration}: Distortion = {self.distortion:.2f}")
                iteration += 1

                if num_iterations and iteration > num_iterations:
                    print("Final prototypes:")
                    for point in self.prototypes:
                        print(f"({point.x}, {point.y})")
                    break
        except KeyboardInterrupt:
            print("\nSimulation stopped by user.")
            print("Final prototypes:")
            for point in self.prototypes:
                print(f"({point.x}, {point.y})")


class ContinuousLloydAlgorithm(LloydAlgorithm):
    def voronoi_partition(self):
        return ExtendedVoronoi.region_split(
            self.boundary_polygon,
            self.prototypes,
            np.linalg.norm(np.ptp(self.boundary, axis=0)),
        )

    def compute_centroids(self, polygon_list):
        return [p.centroid for _, p in polygon_list]

    def calculate_distortion(self):
        return sum(
            p.average_square_distance(point) for point, p in self.polygon_list
        ) / sum(p.area for _, p in self.polygon_list)


class DiscreteLloydAlgorithm(LloydAlgorithm):
    def voronoi_partition(self):
        # Implement discrete Voronoi partition logic
        pass

    def compute_centroids(self, polygon_list):
        # Implement discrete centroid computation
        pass

    def calculate_distortion(self):
        # Implement discrete distortion calculation
        pass
