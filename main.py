import math
import random
import matplotlib.pyplot as plt

COUNT = 180
MI = -1
SIGMA = 0.5

N_SAMPLES = 10000

def main():
    random.seed(42)  # reproducible results
    rejection_samples = normal_distribution_rejection_method(MI, SIGMA, N_SAMPLES)

    # generate graphs
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(rejection_samples, bins=50, density=True,
            color="steelblue", edgecolor="black", alpha=0.7,
            label=f"Samples (n={N_SAMPLES})")

    # theoretical PDF
    curve_x = [MI - 4 * SIGMA + i * (8 * SIGMA / 400) for i in range(400)]
    curve_y = [normal_pdf(x, MI, SIGMA) for x in curve_x]
    ax.plot(curve_x, curve_y, color="crimson", linewidth=2,
            label=f"Theoretical N(μ={MI}, σ={SIGMA})")

    ax.set_title("Normal distribution random generator")
    ax.set_xlabel("x")
    ax.set_ylabel("Density")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.savefig("rejection_method_histogram.png", dpi=150)

    plt.tight_layout()
    plt.show()

def normal_pdf(x, mi, sigma):
    """
    Probability Density Function of the Normal Distribution.
    f(x) = (1 / (sigma * sqrt(2*pi))) * exp(-((x - mi)^2) / (2 * sigma^2))
    """
    PI = math.pi
    E  = math.e
    
    coefficient = 1.0 / (sigma * (2 * PI) ** 0.5)
    exponent = -((x - mi) ** 2) / (2 * sigma ** 2)
    return coefficient * (E ** exponent)


def normal_distribution_rejection_method(mi, sigma, n_samples, x_min=None, x_max=None):
    "Generating random numbers that have the character of normal distribution using Monte Carlo"
    
    if x_min == None:
        x_min = mi - 3 * sigma
    if x_max == None:
        x_max = mi + 3 * sigma

    y_max = normal_pdf(mi, mi, sigma)  # maximum is at x = mi
    y_max *= 1.05 # margin

    samples = []
    while len(samples) < n_samples:
        # generate random [x, y] point
        x = x_min + random.random() * (x_max - x_min) # random x
        y = random.random() * y_max # random y

        # check if point is under curve
        y_value = normal_pdf(x, mi, sigma)
        if y <= y_value:
            samples.append(x)
    return samples

def normal_distribution_generator(mi, sigma):
    "Generating random numbers that have the character of normal distribution using the attached algorithm (from studying materials PDF)"
    pass


if __name__ == "__main__":
    main()
