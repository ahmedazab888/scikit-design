import numpy as np


def d(g, G, A):
    """ Calculates
    """
    G_inv = np.inv(G.T * G)
    d = g.T * G_inv * A * np.inv(A.T * G_inv * A) * A.T * G_inv * g
    return d
