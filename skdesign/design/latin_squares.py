""" Functions of Latin Square and related designs """
import random
from numpy import array


def latin_square(k, treatment_names=None, randomize=None, seed=None):
    """ Creates a k by k Latin Square Design

    A Latin Square design is a block design with 2 blocking factors.  Each
    blocking factor has the same number of levels as there are treatments, k.

    The design can be represented as an array with each row/column representing
    one of the blocking factors.  Each treatment occurs once per row and once
    per column.

    Arguments:
        k: the number of treatments.
        treatment_names: (optional) A list with k elements representing the
            names of each treatment.  The default are the first k uppercase
            letters.
        randomize: (optional) A Boolean indicating if the design should be
            randized.  Default is True
        seed: (optional) The seed for the random number generation.

    Raises:
        ValueError: if k is not an integer greater than 2 or if one of the
            names arguments does not have the correct number of names.

    Returns:
        numpy.array: the Latin Square design
    """

    if not isinstance(k, int) or k < 2:
        raise ValueError('k must be an integer greater than 2.')

    if treatment_names is None:
        treatment_names = [chr(ord('A') + i) for i in range(k)]
    elif not isinstance(treatment_names, list) or len(treatment_names) != k:
        raise ValueError('treatment_names must be a list '
                         'of length {}'.format(k))

    if randomize is None:
        randomize = True
    elif not isinstance(randomize, bool):
        raise ValueError('randomize must be a True or False.')

    if randomize:
        # Randomize the first row to ensure it doesn't start ABCD.
        random.shuffle(treatment_names)

    latin_square = []
    for i in range(k):
        row = []
        for j in range(k):
            treatment_index = i + j
            if treatment_index >= k:
                treatment_index = i + j - k
            row.append(treatment_names[treatment_index])
        latin_square.append(row)
        print(latin_square)

    if randomize:
        # Randomize the rows
        random.shuffle(latin_square)

    return array(latin_square)


def greco_latin_square(k, treatment_names=None, randomize=None, seed=None):
    """ Creates a k by k Greco-Latin Square Design

    Arguments:
        k: the number of treatments.
        treatment_names: (optional) A list with k elements representing the
            names of each treatment.  The default are the first k uppercase
            letters.
        randomize: (optional) A Boolean indicating if the design should be
            randized.  Default is True
        seed: (optional) The seed for the random number generation.

    Raises:
        ValueError: if k is not an integer greater than 2 or if one of the
            names arguments does not have the correct number of names.

    Returns:
        numpy.array: the Latin Square design

    Note:
        This is not compatible with Python 2 due to the use of ord('α').
    """
    if treatment_names is None:
        treatment_names = [[chr(ord('A') + i) for i in range(k)],
                           [chr(ord('α') + i) for i in range(k)]]
    elif not isinstance(treatment_names, list) or len(treatment_names) != 2:
        raise ValueError('treatment_names must be a list of length 2')
        for lst in treatment_names:
            if not isinstance(lst, list) or len(lst) != k:
                raise ValueError('treatment_names must be a list of lists of '
                                 'of length {}'.format(k))

    latin_square_1 = latin_square(k, treatment_names[0], randomize, seed)
    latin_square_2 = latin_square(k, treatment_names[1], randomize, seed)

    greco_latin_square = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append(str(latin_square_1[i][j]) + str(latin_square_2[i][j]))

    return array(greco_latin_square)
