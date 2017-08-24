import math


def obrien_fleming_cutoff(K, current_k, alpha):
    """ Returns the cutoff value for O'Brien and Fleming's Test

    Arguments:
        K: An integer less than 10.
        current_k: The current interm analysis number
        alpha: The alpha level of the overall trial (0.01, 0.05 or 0.1).

    Returns:
        cutoff: The value of \(C_B(K, \alpha)\) for the study.

    Note:
        Since there is no closed source formula for the cutoff value, a lookup
        table is used.
    """

    if not isinstance(K, int) or K < 1 or K > 10:
        raise ValueError('K must be an integer between 1 and 10.')

    if not isinstance(current_k, int) or current_k < 1 or current_k > 10:
        raise ValueError('current_k must be an integer between 1 and 10.')
    if current_k > K:
        raise ValueError('current_k must be less than k.')

    if alpha not in [0.01, 0.05, 0.1]:
        raise ValueError('alpha must be 0.01, 0.05, or 0.1.')

    cutoffs = {
        "0.01": [2.576, 2.580, 2.595, 2.939, 2.986, 3.023, 3.053, 3.078, 3.099, 3.117],
        "0.05": [1.960, 2.178, 2.289, 2.361, 2.413, 2.453, 2.485, 2.512, 2.535, 2.555],
        "0.1": [1.645, 1.875, 1.992, 2.067, 2.122, 2.164, 2.197, 2.225, 2.249, 2.270],
    }
    return cutoffs[str(alpha)][K - 1] * math.sqrt(K / current_k)


def obrien_fleming_adjust_n(n, K, alpha, power):
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
            "0.01": [1.000, 1.001, 1.007, 1.011, 1.015, 1.017, 1.019, 1.021, 1.022, 1.024],
            "0.05": [1.000, 1.008, 1.017, 1.024, 1.028, 1.032, 1.035, 1.037, 1.038, 1.040],
            "0.1": [1.000, 1.016, 1.027, 1.035, 1.040, 1.044, 1.047, 1.049, 1.051, 1.053],
        },
        "0.9": {
            "0.01": [1.000, 1.001, 1.006, 1.010, 1.014, 1.016, 1.018, 1.020, 1.021, 1.022],
            "0.05": [1.000, 1.007, 1.016, 1.022, 1.026, 1.030, 1.032, 1.034, 1.036, 1.037],
            "0.1": [1.000, 1.014, 1.025, 1.032, 1.037, 1.041, 1.044, 1.046, 1.048, 1.049],
        },
    }
    return math.ceil(n * factors[str(power)][str(alpha)][K - 1])


def obrien_fleming_test(z, K, current_k, alpha):
    """ Indicates if a z-score is large enough to stop a test using O'Brien and Fleming's Test

    Arguments:
        z: The z-score to be tested.
        K: An integer less than 10.
        current_k: The current interm analysis number.
        alpha: The alpha level of the overall trial (0.01, 0.05 or 0.1).

    Returns:
        stop: a boolean indicating is the trial should be stoped.

    Note:
        Since there is no closed source formula for the cutoff value, a lookup
        table is used.
    """
    c = obrien_fleming_cutoff(K, current_k, alpha)
    return c < abs(z)
