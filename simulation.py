import random
import tkinter as tk
import numpy as np
from tkinter import Canvas
from geometry_tools import *
from extended_voronoi import ExtendedVoronoi


class VoronoiAnimation:
    def __init__(self, root, screen_width, screen_height, boundary, num_prototypes):
        self.root = root
        self.root.title("Voronoi Animation")

        self.canvas_width = screen_width * 0.8
        self.canvas_height = screen_height * 0.8
        self.canvas = Canvas(
            root, width=self.canvas_width, height=self.canvas_height, bg="white"
        )
        self.canvas.pack()

        self.label = tk.Label(root, text="", font=("Arial", 12))
        self.label.pack()

        # Check if boundary is within canvas boundaries
        if not self.is_boundary_within_canvas(boundary):
            print("Boundary is outside the canvas limits!")
            # Log or display a warning message here
            return

        self.boundary = np.array(boundary)
        self.boundary_polygon = Polygon(self.boundary)
        self.diameter = np.linalg.norm(np.ptp(self.boundary, axis=0))

        self.N_prototypes = num_prototypes

        self.prototypes = [
            Point(
                random.uniform(self.boundary[0][0], self.boundary[2][0]),
                random.uniform(self.boundary[0][1], self.boundary[2][1]),
            )
            for _ in range(self.N_prototypes)
        ]
        self.polygon_list = ExtendedVoronoi.region_split(
            self.boundary_polygon, self.prototypes, self.diameter
        )

        # Assign colors from a more aesthetically pleasing palette
        self.cell_colors = [
            "#FFC300",
            "#DAF7A6",
            "#FF5733",
            "#C70039",
            "#6857E6",
            "#FF6F61",
            "#5E503F",
            "#00A8CC",
            "#F5D0C4",
        ]
        self.point_color = "black"

    def is_boundary_within_canvas(self, boundary):
        min_x, min_y = (
            min(boundary, key=lambda x: x[0])[0],
            min(boundary, key=lambda x: x[1])[1],
        )
        max_x, max_y = (
            max(boundary, key=lambda x: x[0])[0],
            max(boundary, key=lambda x: x[1])[1],
        )

        return (
            0 <= min_x <= self.canvas_width
            and 0 <= min_y <= self.canvas_height
            and 0 <= max_x <= self.canvas_width
            and 0 <= max_y <= self.canvas_height
        )

    def calculate_distortion(self, polygon_list):
        return sum(p.average_square_distance(point) for point, p in polygon_list) / sum(
        p.area for _, p in polygon_list
    )

    def clear_canvas(self):
        self.canvas.delete("points")
        self.canvas.delete("voronoi")

    def draw_voronoi_cells(self):
        for i, (_, p) in enumerate(self.polygon_list):
            polygon_coords = Point.points_to_coords(p.vertices)
            self.canvas.create_polygon(
                polygon_coords,
                fill=self.cell_colors[i % len(self.cell_colors)],
                outline="black",
                tags="voronoi",
            )

    def draw_prototypes(self):
        for point in self.prototypes:
            x, y = point.x, point.y
            self.canvas.create_oval(
                x - 3, y - 3, x + 3, y + 3, fill=self.point_color, tags="points"
            )  # Updated color for prototypes

    def draw_enclosing_rectangle(self):
        self.canvas.create_rectangle(
            self.boundary[0][0],
            self.boundary[0][1],
            self.boundary[2][0],
            self.boundary[2][1],
            outline="green",
        )

    def update(self):
        d_omega = self.calculate_distortion(self.polygon_list)
        self.clear_canvas()
        self.draw_voronoi_cells()
        self.draw_prototypes()
        self.draw_enclosing_rectangle()

        self.label.config(text=f"d_omega = {d_omega:.2f}")
        self.prototypes = [p.centroid for _, p in self.polygon_list]
        self.polygon_list = ExtendedVoronoi.region_split(
            self.boundary_polygon, self.prototypes, self.diameter
        )

        self.root.after(50, self.update)


def main():
    root = tk.Tk()

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set your boundary and number of prototypes here
    boundary = [[100, 100], [700, 100], [700, 500], [100, 500]]
    num_prototypes = 10

    animation = VoronoiAnimation(
        root, screen_width, screen_height, boundary, num_prototypes
    )
    root.after(50, animation.update)
    root.mainloop()


if __name__ == "__main__":
    main()
