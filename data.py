import random


def save_points_to_file(points, filename):
    with open(filename, "w") as file:
        for x, y in points:
            file.write(f"{x}, {y}\n")


# Example usage:
def random_point():
    return random.uniform(10, 700), random.uniform(10, 700)


fixed_points = [random_point() for _ in range(1000)]

filename = "points.txt"
save_points_to_file(fixed_points, filename)
