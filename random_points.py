import random
import tkinter as tk
from cmath import sqrt
from tkinter import Canvas


def random_point():
    return random.uniform(10, length), random.uniform(10, width)


def distance(P1, P2):
    x1, y1 = P1
    x2, y2 = P2
    return sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2).real


def distortion():
    h_dict = {}
    for point in fixed_points:
        min_dist = float("inf")
        for sp_point in specific_points:
            d = distance(point, sp_point)
            if d < min_dist:
                min_dist = d
                closest_point = sp_point
        h_dict[point] = closest_point

    total_dist = sum(distance(point, h_dict[point]) for point in h_dict)
    return total_dist / num_fixed_points


def update():
    global specific_points, length, width
    for i in range(num_specific_points):
        specific_points[i] = random_point()

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
    root.after(500, update)  # Update every second


# Create the main window
root = tk.Tk()
root.title("Animation")

# Create a canvas for drawing points
canvas = Canvas(root, width=800, height=800)
canvas.pack()

# Create a label for displaying d_omega
label = tk.Label(root, text="", font=("Arial", 12))
label.pack()

# Initialize
num_specific_points = 10
num_fixed_points = 1000
length, width = 700, 700

fixed_points = [random_point() for _ in range(num_fixed_points)]

specific_points = [random_point() for _ in range(num_specific_points)]

# Start the animation
update()

# Start the Tkinter main loop
root.mainloop()
