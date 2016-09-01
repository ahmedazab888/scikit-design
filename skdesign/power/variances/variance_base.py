from skdesign.power import (PowerBase,
                            is_positive)


class VarianceBase(PowerBase):
    """ The base for hypothesis on variance using an F statistic.

    Attributes:
        n: The number of subjects required to test the hypothesis at an
            :math:`\\alpha` level and a power of :math:`1 - \\beta`.
        m: The number of replicates per subject.
        stdev_1: The variance of the first treament.
        stdev_2: The variance of the second treamment.
        similarity_limit: :math:`\\delta`

        alpha: The :math:`\\alpha` level required by the hypothesis.
        beta: The :math:`\\beta` level required by the hypothesis (equal to
            :math:`1` - power).
        power: The power required by the hypothesis (equal to
            :math:`1 - \\beta`).
    """

    def __init__(self, n=None, m=None, stdev_1=None, stdev_2=None,
                 similarity_limit=None, hypothesis=None,
                 alpha=None, beta=None, power=None):

        if n is not None:
            if isinstance(n, int):
                self.n = n
            else:
                raise ValueError('`n` should be of type Int.')
        else:
            self.n = None

        if m is not None:
            if isinstance(m, int):
                self.m = m
            else:
                raise ValueError('`m` should be of type Int.')
        else:
            raise ValueError('`m` must be provided.')

        is_positive(stdev_1, 'stdev_1')
        self.stdev_1 = stdev_1
        is_positive(stdev_2, 'stdev_2')
        self.stdev_2 = stdev_2

        if hypothesis == 'equality':
            self._alpha_adjustment = 2
            self._beta_adjustment = 1
            similarity_limit = 1
            sigma_ratio = stdev_2 / stdev_1
        elif hypothesis == 'superiority':
            self._alpha_adjustment = 1
            self._beta_adjustment = 1
            if similarity_limit is None:
                raise ValueError('A similarity_limit must be provided')
            sigma_ratio = stdev_2 / (stdev_1 * similarity_limit)
        elif hypothesis == 'equivalence':
            self._alpha_adjustment = 1
            self._beta_adjustment = 2
            if similarity_limit is None:
                raise ValueError('A similarity_limit must be provided')
            sigma_ratio = (stdev_2 * similarity_limit) / stdev_1

        self.similarity_limit = similarity_limit
        self.sigma_ratio = sigma_ratio

        # Initialize the remaining arguments through the parent.
        super(VarianceBase, self).__init__(alpha=alpha, power=power,
                                           beta=beta, hypothesis=hypothesis)
