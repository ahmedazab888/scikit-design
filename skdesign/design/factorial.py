""" Functions for a factorial design """
import random


def block_design(randomize=None, seed=None, **kwargs):
    """ Generate a Block Design

    Arguments:
        randomize: (optional) A boolean indicating if the runs should be in a
            random order.  The default is false.
        seed: (optional) The seed for the RNG.
        **kwargs: A list of factors for each nuisance factor

    Returns:
        dict: The dictionary has two components: a list of names that is the
            names of the factors in the order they appear in the lists and a
            list of lists where each list represents a run.
    """
    factor_names = []
    factor_levels = []
    total_levels = 1

    # Sort the keywords to ensure reproducibiltiy
    factors = sorted(kwargs.items())
    for factor, levels in factors:
        factor_names.append(factor)
        if not isinstance(levels, list):
            raise ValueError('Each factor must have a list of levels.')
        factor_levels.append(len(levels))
        total_levels *= len(levels)
    n_factors = len(factor_names)

    # design = [[0] * n_factors] * total_levels
    design = []
    current_level = [0] * n_factors
    for run in range(total_levels):
        design.append(current_level[:])
        current_level[n_factors - 1] += 1
        for factor in range(n_factors - 1, 0, -1):
            if current_level[factor] > factor_levels[factor] - 1:
                current_level[factor] = 0
                current_level[factor - 1] += 1
    for run in range(total_levels):
        for factor in range(n_factors):
            design[run][factor] = factors[factor][1][design[run][factor]]

    if randomize:
        random.seed(seed)
        random.shuffle(design)

    res = {
        'names': factor_names,
        'design': design
    }

    return res


def two_series_factorial(k=None, factors=None, labels=None,
                         randomize=None, seed=None):
    """ Generates a design for a two series factorial

    A two series factorial (:math:`2^k`) design with :math:`k` factors is a
    special case of the block design where each factor has only two levels,
    high and low.

    Arguments:
        k: (optional) the number of factors
        factors: (optional)
        labels: (optional) labels for the high and low levels.  The default is
            ['High', 'Low']
        randomize: (optional) A boolean indicating if the runs should be in a
            random order.  The default is false.
        seed: (optional) The seed for the RNG.

    Returns:
        dict: The dictionary has two components: a list of names that is the
            names of the factors in the order they appear in the lists and a
            list of lists where each list represents a run.

    Raises:
        ValueError: if k is not an int, k < 2, labels is not a list or
            len(labels) is not 2.

    Note:
        Either k or factors is required.
    """
    if k is None:
        if factors is None:
            raise ValueError('Either `k` or `factors` must be given')
        if not isinstance(labels, list) or len(labels) < 2:
            raise ValueError('`factors` must be a list of at least length 2')
        k = len(factors)
    else:
        if not isinstance(k, int) or k < 2:
            raise ValueError('`k` must be greater than 1.')
        if factors is None:
            factors = ['x_' + str(i + 1) for i in range(k)]
        elif len(factors) != k:
            raise ValueError('`factors` must be length `k`')

    if labels is None:
        labels = ['High', 'Low']
    else:
        if not isinstance(labels, list) or len(labels) != 2:
            raise ValueError('`labels` must be a list of length 2')

    levels = {}
    for factor in factors:
        levels[factor] = labels

    return block_design(randomize=randomize, **levels)
