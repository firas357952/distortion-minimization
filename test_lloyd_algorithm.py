from lloyd_algorithm import ContinuousLloydAlgorithm

# Define a boundary and number of points
boundary = [[0, 0], [10, 0], [10, 10], [0, 10]]  # Example boundary coordinates
num_points = 5  # Example number of points

lloyd = ContinuousLloydAlgorithm(boundary, num_points)

num_iterations = None  # Example number of iterations
lloyd.run_simulation(num_iterations)
