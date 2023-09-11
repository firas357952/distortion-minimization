import random
import tkinter as tk
from cmath import sqrt
from tkinter import Canvas

def load_points_from_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            # Split each line into x and y values using the comma as a separator
            x, y = map(float, line.strip().split(','))
            points.append((x, y))
    return points


def random_point():
    return random.uniform(10, length), random.uniform(10, width)


def distance(P1, P2):
    x1, y1 = P1
    x2, y2 = P2
    return sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2).real


def closest_specific_point(point):
    min_dist = float("inf")
    for sp_point in specific_points:
        d = distance(point, sp_point)
        if d < min_dist:
            min_dist = d
            closest_point = sp_point

    return closest_point


def distortion():
    total_dist = sum(
        distance(point, closest_specific_point(point)) for point in fixed_points
    )
    return total_dist / len(fixed_points)


def partition():
    partitions = {}
    for point in fixed_points:
        p = closest_specific_point(point)
        if p in partitions:
            partitions[p].append(point)
        else:
            partitions[p] = [point]
    return partitions


def center_of_mass(points):
    if not points:
        return None

    return sum(point[0] for point in points) / len(points), sum(
        point[1] for point in points
    ) / len(points)


def iteration():
    return [center_of_mass(points) for points in list(partition().values())]


def update():
    global specific_points, length, width

    d_omega = distortion()  # Calculate the distortion

    canvas.delete("points")  # Clear all points

    # Draw fixed points
    for x, y in fixed_points:
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue", tags="points")

    # Draw specific points
    for x, y in specific_points:
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", tags="points")

    # Draw the enclosing rectangle (in green)
    canvas.create_rectangle(5, 5, length + 5, width + 5, outline="green")

    label.config(text=f"d_omega = {d_omega:.2f}")
    root.after(100, update)  # Update every second

    specific_points = iteration()


# Create the main window
root = tk.Tk()
root.title("Animation")

# Create a canvas for drawing points
canvas = Canvas(root, width=710, height=710)
canvas.pack()

# Create a label for displaying d_omega
label = tk.Label(root, text="", font=("Arial", 12))
label.pack()

# Initialize
num_specific_points = 10
num_fixed_points = 1000
length, width = 700, 700

fixed_points = load_points_from_file("points.txt")

specific_points = [random_point() for _ in range(num_specific_points)]

# Start the animation
update()

# Start the Tkinter main loop
root.mainloop()
