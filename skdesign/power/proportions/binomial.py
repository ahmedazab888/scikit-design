import math
from skdesign.power import (PowerBase,
                            is_in_0_1,
                            is_integer)
import scipy.stats as stats
import numpy.random as random


class Binomial(PowerBase):
    """ Hypotheses for a Binomial test of proportions.

    Hypothesis:
        The test for equality and the test for superiority can be unified under
        the hypothesis:

        :math:`H_{0}: p = p_0 + \\delta`
        :math:`H_{1}: p = p_1`

        where :math:`p_0` is the null value, :math:`p_1` is the estimated value
        of the probability and :math:`\\delta` is the margin.

        Note that when :math:`\\delta = 0`, the hypothesis is an equality test.
        :math:`\\delta > 0 (< 0)` corresponds to a superiority
        (non-inferiority) test.

    Attributes:
        n: The sample size
        alpha: The :math:`\\alpha` level required by the hypothesis.
        beta: The :math:`\\beta` level required by the hypothesis (equal to
            :math:`1 - power`).
        power: The power required by the hypothesis (equal to
            :math:`1 - \\beta`).
        p_0: The null value for the probability
        p_1: The estimated value for the probability
        margin: The margin used in superiority hypotheses
    """

    # Parameters controling the simulation of power
    _N_SIMS = 1000
    _SEED = 710321

    # Parameters controling the search grid for the calculation of sample size.
    _minN = 2
    _maxN = 40

    def __init__(self, n=None, alpha=None, beta=None, power=None,
                 p=None, p_0=None, margin=None):

        is_in_0_1(p, 'p')
        self.p = p

        is_in_0_1(p_0, 'p_0')
        self.p_0 = p_0

        if margin is not None:
            is_in_0_1(margin + p_0, 'margin + p_0')
            self.margin = margin
            self.p_0 += margin
        else:
            self.margin = 0

        if n is not None:
            is_integer(n, 'n')
        self.n = n

        super(Binomial, self).__init__(alpha=alpha, power=power,
                                       beta=beta, hypothesis='equality')

    def calculate(self):
        if self.n is None:
            self.calculate_n()
            self.calculate_alpha()
        elif self.power is None:
            self.calculate_power()
        elif self.alpha is None:
            self.calculate_alpha()

    def calculate_n(self):
        """ Perfrom the power calculation """
        if self.power is None:
            power = 0.8
        else:
            power = self.power

        if self.alpha is None:
            alpha = 0.5
        else:
            alpha = self.alpha

        random.seed(self._SEED)

        found_solution = False
        for n in range(self._minN, self._maxN):
            res = random.binomial(n, self.p, self._N_SIMS)

            count = 0
            for x in res:
                p_val = stats.binom_test(x, n=n, p=self.p_0)
                if p_val < alpha:
                    count += 1
            test_power = count / self._N_SIMS
            if test_power > power:
                found_solution = True
                self.power = test_power
                self.n = n
                break
        if not found_solution:
            raise BaseException("N > " + str(self._maxN) +
                                ".  You should use large sample theory.")

    def calculate_power(self):
        """ Perfrom the power calculation """
        if self.alpha is None:
            alpha = 0.05
        else:
            alpha = self.alpha

        random.seed(self._SEED)

        res = random.binomial(self.n, self.p, self._N_SIMS)

        count = 0
        for x in res:
            p_val = stats.binom_test(x, n=self.n, p=self.p_0)
            if p_val < alpha:
                count += 1
        self.power = count / self._N_SIMS
        self.beta = 1 - self.power

    def calculate_alpha(self):
        """ Perfrom the power calculation """
        if self.power is None:
            power = 0.8
        else:
            power = self.power

        random.seed(self._SEED)

        res = random.binomial(self.n, self.p, self._N_SIMS)

        p_vals = []
        for x in res:
            p_val = stats.binom_test(x, n=self.n, p=self.p_0)
            p_vals.append(p_val)
        p_vals.sort()
        self.alpha = p_vals[int(self._N_SIMS * power)]
