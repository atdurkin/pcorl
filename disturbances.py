""" Function to generate disturbance trajectories for feed concentration and feed temperature
"""
import numpy as np


def disturbances(nsteps, space):
    lb, ub = space["low"], space["high"]
    assert lb.shape == ub.shape, "low and high must be the same shape"
    dim = lb.shape[0]
    d = np.zeros((nsteps, dim))

    print(d.shape)

    for i in range(dim):
        dist = ub[i] - lb[i]
        noise = np.random.normal(0, 0.1 * dist, (nsteps,))
        mean = np.ones_like(noise) * np.mean([lb[i], ub[i]])
        print(noise.shape, mean.shape)
        d[:, i] = mean + noise
    return d


if __name__ == "__main__":
    disturbance_space = {"low": np.array([0.9, 340]), "high": np.array([1.1, 360])}
    d = disturbances(100, disturbance_space)
