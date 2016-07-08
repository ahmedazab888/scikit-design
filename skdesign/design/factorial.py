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
    print(factor_names)
    print(factor_levels)
    print(factors)

    design = []
    current_level = [0] * n_factors
    for run in range(total_levels):
        design.append(current_level[:])
        for factor in range(n_factors - 1, 0, -1):
            current_level[factor] += 1
            if current_level[factor] > factor_levels[factor] - 1:
                current_level[factor] = 0
                current_level[factor - 1] += 1

    print(design)
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
