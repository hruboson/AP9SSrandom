import math
import random

import matplotlib.pyplot as plt

MI = -1
SIGMA = 0.5
N_SAMPLES = 180


def main():
    random.seed(42)  # reproducible results
    rejection_samples = normal_distribution_rejection_method(MI, SIGMA, N_SAMPLES)
    sum12_samples = [normal_distribution_generator(MI, SIGMA) for _ in range(N_SAMPLES)]

    # generate graphs
    _, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    curve_x = [MI - 4 * SIGMA + i * (8 * SIGMA / 400) for i in range(400)]

    curve_y = [normal_pdf(x, MI, SIGMA) for x in curve_x]

    # left: rejection sampling
    axes[0].hist(
        rejection_samples,
        bins=50,
        density=True,
        color="steelblue",
        edgecolor="black",
        alpha=0.7,
        label=f"Rejection sampling (n={N_SAMPLES})",
    )
    axes[0].plot(
        curve_x,
        curve_y,
        color="crimson",
        linewidth=2,
        label=f"Theoretical N(μ={MI}, σ={SIGMA})",
    )
    axes[0].set_title("Method 1: Rejection Sampling")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("Density")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # right: sum of 12 uniforms
    axes[1].hist(
        sum12_samples,
        bins=50,
        density=True,
        color="seagreen",
        edgecolor="black",
        alpha=0.7,
        label=f"Sum of 12 uniforms (n={N_SAMPLES})",
    )
    axes[1].plot(
        curve_x,
        curve_y,
        color="crimson",
        linewidth=2,
        label=f"Theoretical N(μ={MI}, σ={SIGMA})",
    )
    axes[1].set_title("Method 2: Sum of 12 Uniforms (Irwin–Hall)")
    axes[1].set_xlabel("x")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    plt.savefig("generated_values.jpg", dpi=150)

    plt.tight_layout()
    plt.show()

    # comparison
    _, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        rejection_samples,
        bins=60,
        density=True,
        color="steelblue",
        edgecolor="black",
        alpha=0.45,
        label="Rejection sampling",
    )

    ax.hist(
        sum12_samples,
        bins=60,
        density=True,
        color="seagreen",
        edgecolor="black",
        alpha=0.45,
        label="Sum of 12 uniforms",
    )

    ax.plot(
        curve_x,
        curve_y,
        color="crimson",
        linewidth=2.5,
        label=f"Theoretical N(μ={MI}, σ={SIGMA})",
    )

    ax.set_title("Overlay: Rejection Sampling vs. Sum of 12 Uniforms")
    ax.set_xlabel("x")
    ax.set_ylabel("Density")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.savefig("comparison.jpg", dpi=150)

    plt.tight_layout()
    plt.show()


def normal_pdf(x, mi, sigma):
    """
    Probability Density Function of the Normal Distribution.
    f(x) = (1 / (sigma * sqrt(2*pi))) * exp(-((x - mi)^2) / (2 * sigma^2))
    """
    PI = math.pi
    E = math.e

    coefficient = 1.0 / (sigma * (2 * PI) ** 0.5)
    exponent = -((x - mi) ** 2) / (2 * sigma**2)
    return coefficient * (E**exponent)


def normal_distribution_rejection_method(mi, sigma, n_samples, x_min=None, x_max=None):
    """
    Generating random numbers that have the character of normal distribution using Monte Carlo
    """
    if sigma <= 0:
        raise ValueError("Sigma must be positive.")

    if x_min == None:
        x_min = mi - 3 * sigma
    if x_max == None:
        x_max = mi + 3 * sigma

    y_max = normal_pdf(mi, mi, sigma)  # maximum is at x = mi
    y_max *= 1.05  # margin

    samples = []
    while len(samples) < n_samples:
        # generate random [x, y] point
        x = x_min + random.random() * (x_max - x_min)  # random x
        y = random.random() * y_max  # random y

        # check if point is under curve
        y_value = normal_pdf(x, mi, sigma)
        if y <= y_value:
            samples.append(x)
    return samples


def normal_distribution_generator(mi, sigma):
    if sigma <= 0:
        raise ValueError("Sigma must be positive.")

    # generate 12 independent uniform random values and calculate their sum.
    S = 0.0

    for _ in range(1, 13):  # _ = i
        r = random.random()  # random is uniform(0;1)
        S += r

    u = S - 6.0  # approximate the standard normal distribution N(0;1)
    x = mi + sigma * u  # transform to N(mi, sigma^2)

    return x


if __name__ == "__main__":
    main()
