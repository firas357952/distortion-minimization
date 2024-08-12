from lloyd_algorithm import ContinuousLloydAlgorithm

# Define a boundary and number of points
boundary = [[100, 100], [500, 100], [500, 500], [100, 500]]
num_points = 9  # Example number of points

lloyd = ContinuousLloydAlgorithm(boundary, num_points)

num_iterations = 200  # Example number of iterations
lloyd.run_simulation(num_iterations)
