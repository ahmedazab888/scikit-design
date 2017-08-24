""" Functions of Latin Square and related designs """
import random
from math import floor

MAX_ITERATIONS = 10000


def latin_square(k, factor_labels=None, seed=None):
    """ Creates a k by k Latin Square Design

    A Latin Square design is a block design with 2 blocking factors.  Each
    blocking factor has the same number of levels as there are treatments, k.

    This function returns a randomly generated latin square.

    The design is represented as a list of lists.  Each treatment occurs
    once per row and once per column.

    Arguments:
        k: the number of treatments.
        factor_labels: (optional) A list with k elements representing the
            labels applied to the levels of the blocking factor.  The default
            are the first k uppercase Latin letters.
        seed: (optional) The seed for the random number generation.

    Raises:
        ValueError: if k is not an integer greater than 2 or if one of the
            names arguments does not have the correct number of names.

    Returns:
        list of lists: the Latin Square design
    """
    random.seed(seed)

    if not isinstance(k, int) or k < 2:
        raise ValueError('k must be an integer greater than 2.')

    if factor_labels is None:
        factor_labels = [chr(ord('A') + i) for i in range(k)]
    elif not isinstance(factor_labels, list) or len(factor_labels) != k:
        raise ValueError('factor_labels must be a list '
                         'of length {}'.format(k))

    latin_square = _create_latin_square(k)
    for row in range(k):
        for col in range(k):
            latin_square[row][col] = factor_labels[latin_square[row][col]]

    return latin_square


def _cube_to_square(cube, k):
    square = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append(0)
        square.append(row)
    for x in range(k):
        for y in range(k):
            for s in range(k):
                if cube[x][y][s] == 1:
                    square[x][y] = s
                    break
    return square


def _square_to_cube(square, k):
    cube = []
    for i in range(k):
        outer_row = []
        for j in range(k):
            inner_row = []
            for m in range(k):
                inner_row.append(0)
            outer_row.append(inner_row)
        cube.append(outer_row)
    for x in range(k):
        for y in range(k):
            cube[x][y][square[x][y]] = 1
    return cube


def _default_square(k):
    lookup = [0] * (2 * k)
    square = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append(0)
        square.append(row)
    for a in range(2):
        for i in range(k):
            lookup[a * k + i] = i
    for y in range(k):
        for x in range(k):
            square[y][x] = lookup[x + y]
    return square


def _shuffle_cube(cube, k):
    min_iterations = k * k * k
    iterations = 0
    proper = True
    improper_cell = None
    while iterations < min_iterations or not proper:
        iterations += 1
        if iterations > MAX_ITERATIONS:
            raise Exception()
        if proper:
            t = {
                'x': floor(random.random() * k),
                'y': floor(random.random() * k),
                'z': floor(random.random() * k),
            }
            counter = 0
            while cube[t['x']][t['y']][t['z']] != 0:
                counter += 1
                if counter > 100:
                    raise Exception()
                t['x'] = floor(random.random() * k)
                t['y'] = floor(random.random() * k)
                t['z'] = floor(random.random() * k)
            i = 0
            while cube[i][t['y']][t['z']] == 0:
                i += 1
            x_1 = i

            i = 0
            while cube[t['x']][i][t['z']] == 0:
                i += 1
            y_1 = i

            i = 0
            while cube[t['x']][t['y']][i] == 0:
                i += 1
            z_1 = i
        else:
            t = improper_cell

            skip_next = random.random() < 0.5
            for i in range(k):
                if cube[i][t['y']][t['z']] == 1:
                    x_1 = i
                    if not skip_next:
                        break

            skip_next = random.random() < 0.5
            for i in range(k):
                if cube[t['x']][i][t['z']] == 1:
                    y_1 = i
                    if not skip_next:
                        break

            skip_next = random.random() < 0.5
            for i in range(k):
                if cube[t['x']][t['y']][i] == 1:
                    z_1 = i
                    if not skip_next:
                        break

        cube[t['x']][t['y']][t['z']] += 1
        cube[t['x']][y_1][z_1] += 1
        cube[x_1][y_1][t['z']] += 1
        cube[x_1][t['y']][z_1] += 1

        cube[t['x']][t['y']][z_1] -= 1
        cube[t['x']][y_1][t['z']] -= 1
        cube[x_1][t['y']][t['z']] -= 1
        cube[x_1][y_1][z_1] -= 1

        proper = cube[x_1][y_1][z_1] != -1
        if not proper:
            improper_cell = {
                'x': x_1,
                'y': y_1,
                'z': z_1,
            }
    return cube


def _create_latin_square(k):
    square = _default_square(k)
    cube = _square_to_cube(square, k)
    cube = _shuffle_cube(cube, k)
    square = _cube_to_square(cube, k)
    return square


def greaco_latin_square(k, factor_1_labels=None, factor_2_labels=None, seed=None):
    """ Creates a k by k Greaco-Latin Square Design

    A greaco-latin square is a design comprised of two orthogonal latin
    squares.  Note, there are no designs for k = 6.

    Arguments:
        k: the number of treatments.
        factor_1_names: (optional) A list with k elements containing the
            labels applied to the levels of the first factor.  The default are
            the first k uppercase Latin letters.
        seed: (optional) The seed for the random number generation.

    Raises:
        ValueError: if k is not an integer greater than 2 or if one of the
            names arguments does not have the correct number of names.

    Returns:
        list of lists: the Greaco-Latin Square design

    Note:
        This is not compatible with Python 2 due to the use of ord('α').
    """
    if k < 2 or k == 6:
        raise ValueError('No Greaco-Latin Squares exist for k={}'.format(k))

    if factor_1_labels is None:
        factor_1_labels = [chr(ord('A') + i) for i in range(k)]
    elif not isinstance(factor_1_labels, list) or len(factor_1_labels) != k:
        raise ValueError('factor_1_labels must be a list of length {}}').format(k)

    if factor_2_labels is None:
        factor_2_labels = [chr(ord('α') + i) for i in range(k)]
    elif not isinstance(factor_2_labels, list) or len(factor_2_labels) != k:
        raise ValueError('factor_2_labels must be a list of length {}}').format(k)

    if seed is None or seed == 0:
        seed = 7172

    n_iter = 0
    while True:
        n_iter += 1
        latin_square_1 = latin_square(k,
                                      treatment_names=factor_1_labels,
                                      randomize=True,
                                      seed=seed * n_iter)

        latin_square_2 = latin_square(k,
                                      treatment_names=factor_2_labels,
                                      randomize=True,
                                      seed=35 * seed * n_iter)
        if is_orthoganal(k, latin_square_1, latin_square_2):
            break
        if n_iter > MAX_ITERATIONS:
            raise Exception('Maximum number of iterations reached')
    greaco_latin_square = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append((str(latin_square_1[i][j]) +
                        str(latin_square_2[i][j])))
        greaco_latin_square.append(row)
    return greaco_latin_square


def is_orthoganal(k, latin_square_1, latin_square_2):
    symbols = []
    for i in range(k):
        for j in range(k):
            symbol = str(latin_square_1[i][j]) + str(latin_square_2[i][j])
            if symbol in symbols:
                return False
            symbols.append(symbol)
    return True
