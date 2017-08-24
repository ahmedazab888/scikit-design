import math


def pocock_cutoff(K, alpha):
    """ Returns the cutoff value for Pocock's Test

    Arguments:
        K: An integer less than 10.
        alpha: The alpha level of the overall trial (0.01, 0.05 or 0.1).

    Returns:
        cutoff: The value of \(C_P(K, \alpha)\) for the study.

    Note:
        Since there is no closed source formula for the cutoff value, a lookup
        table is used.
    """

    if not isinstance(K, int) or K < 1 or K > 10:
        raise ValueError('K must be an integer between 1 and 10.')

    if alpha not in [0.01, 0.05, 0.1]:
        raise ValueError('alpha must be 0.01, 0.05, or 0.1.')

    cutoffs = {
        "0.01": [2.576, 2.772, 2.873, 2.939, 2.986, 3.023, 3.053, 3.078, 3.099, 3.117],
        "0.05": [1.960, 2.178, 2.289, 2.361, 2.413, 2.453, 2.485, 2.512, 2.535, 2.555],
        "0.1": [1.645, 1.875, 1.992, 2.067, 2.122, 2.164, 2.197, 2.225, 2.249, 2.270],
    }
    return cutoffs[str(alpha)][K - 1]


def pocock_adjust_n(n, K, alpha, power):
    """ Adjusts a sample size to allow for multiple interm analyses

    Arguments:
        n: The sample size (an integer greater than 1) needed for the trial.
        K: An integer less than 10.
        alpha: The alpha level of the overall trial (0.01, 0.05 or 0.1).
        power: The power of the overall trial (0.8, 0.9).

    Returns:
        n_P: the adjusted sample size required for the trial.

    Note:
        Since there is no closed source formula for the cutoff value, a lookup
        table is used.
    """

    if not isinstance(n, int) or n < 1:
        raise ValueError('n must be an integer greater than 1.')

    if not isinstance(K, int) or K < 1 or K > 10:
        raise ValueError('K must be an integer between 1 and 10.')

    if alpha not in [0.01, 0.05, 0.1]:
        raise ValueError('alpha must be 0.01, 0.05, or 0.1.')

    if power not in [0.8, 0.9]:
        raise ValueError('power must be 0.8, or 0.9.')

    factors = {
        "0.8": {
            "0.01": [1.000, 1.092, 1.137, 1.166, 1.187, 1.203, 1.216, 1.226, 1.236, 1.243],
            "0.05": [1.000, 1.110, 1.166, 1.202, 1.229, 1.249, 1.265, 1.279, 1.291, 1.301],
            "0.1": [1.000, 1.121, 1.184, 1.224, 1.254, 1.277, 1.296, 1.311, 1.325, 1.337],
        },
        "0.9": {
            "0.01": [1.000, 1.084, 1.125, 1.152, 1.170, 1.185, 1.197, 1.206, 1.215, 1.222],
            "0.05": [1.000, 1.100, 1.151, 1.183, 1.207, 1.225, 1.239, 1.252, 1.262, 1.271],
            "0.1": [1.000, 1.110, 1.166, 1.202, 1.228, 1.249, 1.266, 1.280, 1.292, 1.302],
        },
    }
    return math.ceil(n * factors[str(power)][str(alpha)][K - 1])


def pocock_test(z, K, alpha):
    """ Indicates if a z-score is large enough to stop a test using Pocock's Test

    Arguments:
        z: The z-score
        K: An integer less than 10.
        alpha: The alpha level of the overall trial (0.01, 0.05 or 0.1).

    Returns:
        stop: a boolean indicating is the trial should be stoped.

    Note:
        Since there is no closed source formula for the cutoff value, a lookup
        table is used.
    """

    c = pocock_cutoff(K, alpha)
    return c < abs(z)
