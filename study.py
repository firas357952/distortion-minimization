import time

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from lloyd_algorithm import ContinuousLloydAlgorithm


def run_lloyd_algorithm(boundary, num_prototypes):
    lloyd = ContinuousLloydAlgorithm(boundary, num_prototypes)
    dst = lloyd.distortion
    idx_iteration = 0
    while True:
        idx_iteration += 1
        lloyd.single_iteration()
        if abs(dst - lloyd.distortion) < 0.001:
            break
        dst = lloyd.distortion
    return lloyd.distortion, idx_iteration


def group_distortion_by_range(distortion_dict, interval):
    distortion_values = [v[0] for v in distortion_dict.values()]
    grouped_distortion = {}
    for value in distortion_values:
        added = False
        for key in grouped_distortion:
            if abs(key - value) < interval:
                grouped_distortion[key] += 1
                added = True
                break
        if not added:
            grouped_distortion[round(value)] = 1
    return grouped_distortion, len(distortion_values)


def plot_histogram(distortion_dict, num_prototypes):
    grouped_distortion, nbr_passed_test = group_distortion_by_range(
        distortion_dict, interval
    )
    plt.figure(figsize=(12, 6), dpi=150)
    x_values = list(grouped_distortion.keys())
    y_values = list(grouped_distortion.values())

    bars = plt.bar(x_values, y_values, alpha=0.75, edgecolor="black", color="skyblue")

    plt.xlabel("Distortion")
    plt.ylabel("Frequency")
    plt.title(f"Distribution of Distortion Values\nNum Prototypes: {num_prototypes}")

    for _, (x, y) in enumerate(grouped_distortion.items()):
        plt.text(
            x,
            y,
            f"{y/nbr_passed_test*100:.2f}%",
            ha="center",
            va="bottom",
            fontsize=10,
            color="darkblue",
        )

    plt.xlim(min(x_values) * 0.999, max(x_values) * 1.001)
    plt.xticks(rotation=45, ha="right")
    plt.ticklabel_format(style="plain", axis="x")

    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.gca().set_axisbelow(True)

    legend_labels = [f"Distortion: {x:.2f}" for x in x_values]
    legend_labels.sort()
    plt.legend(
        bars,
        legend_labels,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=8,
        title="Distortion Values",
    )

    plt.tight_layout()
    plt.savefig(f"./figs/histogram_{num_prototypes}.png", bbox_inches="tight")

    with open(f"./figs/grouped_distortions_{num_prototypes}.txt", "w") as file:
        file.write(f"Grouped Distortion Values for {num_prototypes} Prototypes:\n")
        file.write(f"Number of Tests: {nb_tests}\n")
        file.write(f"Number of Passed Tests: {nbr_passed_test}\n")
        file.write(f"Total Execution Time: {elapsed_time:.4f} seconds\n")
        for key, value in grouped_distortion.items():
            file.write(
                f"Distortion: {key} - Count: {value} - Frequency: {value / nbr_passed_test * 100}%\n"
            )

    with open(f"./figs/distortion_values_{num_prototypes}.txt", "w") as file:
        file.write(f"Distortion Values for {num_prototypes} Prototypes:\n")
        for test_nbr, (dst, iter) in distortion_dict.items():
            file.write(
                f"Test number {test_nbr}: distortion: {dst}, iterations to stop: {iter}\n"
            )


boundary = [[100, 100], [700, 100], [700, 400], [100, 400]]
nb_tests = 100
interval = 2

for num_prototypes in range(3, 15):
    distortion_dict = {}

    start_time = time.time()
    for idx_test in range(nb_tests):
        try:
            distortion, idx_iteration = run_lloyd_algorithm(boundary, num_prototypes)
            distortion_dict[idx_test] = (distortion, idx_iteration)
        except Exception:
            pass

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(
        f"Total Execution Time for {num_prototypes} Prototypes: {elapsed_time:.4f} seconds"
    )

    plot_histogram(distortion_dict, num_prototypes)
