import numpy as np


def bootstrap_this(data, n=10000, average_statistic=np.mean, error_statistic=np.std):
    """
    Bootstrap a 1D dataset using a `average_statistic` [np.mean as the default]
    This will pick `len(data)` data-points from `data` at random (with replacement) and compute the `average_statistic`.
    This process repeats `n` times until a bootstrap_distribution of `average_statistic`s is formed.
    average_statistic and error_statistic must accept the keyword argument `axis`.
    
    Returns 
        float:          average_statistic(bootstrap_distribution)
        float:          error_statistic(bootstrap_distribution)
        array[float]:   bootstrap_distribution
    """
    assert data.ndim == 1
    choice = np.random.choice(data, (len(data), n))
    bootstrap_distribution = average_statistic(choice, axis=0)
    return average_statistic(bootstrap_distribution), error_statistic(bootstrap_distribution), bootstrap_distribution
