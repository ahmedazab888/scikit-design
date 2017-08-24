import math
from skdesign.power import (PowerBase,
                            is_in_0_1)
import scipy.stats as stats
import numpy.random as random


class Fisher(PowerBase):
    """ Hypotheses for Fisher's Exact Test

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
    _minN = 4
    _maxN = 100

    def __init__(self, n_1=None, n_2=None, ratio=None, alpha=None, beta=None, power=None,
                 p_1=None, p_2=None):

        is_in_0_1(p_1, 'p_1')
        self.p_1 = p_1

        is_in_0_1(p_2, 'p_2')
        self.p_2 = p_2

        # n is only used to help with control flow
        if ratio is None:
            if n_1 is None:
                ratio = 1
                if n_2 is None:
                    n = None
                else:
                    n_1 = n_2
                    n = n_1 + n_2
            else:
                if n_2 is None:
                    ratio = 1
                    n_2 = n_1
                    n = n_1 + n_2
                else:
                    n = n_1 + n_2
                    ratio = n_1 / float(n_2)
        else:
            if n_1 is None:
                if n_2 is None:
                    n = None
                else:
                    n_1 = math.ceil(ratio * n_2)
                    n = n_1 + n_2
            else:
                if n_2 is None:
                    n_2 = math.ceil(n_1 / ratio)
                    n = n_1 + n_2
                else:
                    n = n_1 + n_2

        self.n_1 = n_1
        self.n_2 = n_2
        self.n = n
        self.ratio = float(ratio)

        super(Fisher, self).__init__(alpha=alpha, power=power,
                                     beta=beta, hypothesis='equality')

    def calculate(self):
        if self.n is None:
            self.calculate_n()
        elif self.power is None:
            self.calculate_power()
        elif self.alpha is None:
            self.calculate_alpha()

    def calculate_power(self):
        """ Perfrom the power calculation """
        if self.alpha is None:
            alpha = 0.05
        else:
            alpha = self.alpha

        random.seed(self._SEED)

        res_1 = random.binomial(self.n_1, self.p_1, self._N_SIMS)
        res_2 = random.binomial(self.n_2, self.p_2, self._N_SIMS)

        count = 0
        for x_1, x_2 in zip(res_1, res_2):
            contingency = [[x_1, self.n_1 - x_1], [x_2, self.n_2 - x_2]]
            _, p_val = stats.fisher_exact(contingency)
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

        res_1 = random.binomial(self.n_1, self.p_1, self._N_SIMS)
        res_2 = random.binomial(self.n_2, self.p_2, self._N_SIMS)

        res = []
        for x_1, x_2 in zip(res_1, res_2):
            contingency = [[x_1, self.n_1 - x_1], [x_2, self.n_2 - x_2]]
            _, p_val = stats.fisher_exact(contingency)
            res.append(p_val)
        res.sort()
        self.alpha = res[math.ceil(self._N_SIMS * power)]

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

        group_1_proportion = self.ratio / (1 + self.ratio)
        found_solution = False
        for n in range(self._minN, self._maxN):
            n_1 = round(n * group_1_proportion)
            n_2 = n - n_1

            res_1 = random.binomial(n_1, self.p_1, self._N_SIMS)
            res_2 = random.binomial(n_2, self.p_2, self._N_SIMS)

            count = 0
            for x_1, x_2 in zip(res_1, res_2):
                contingency = [[x_1, n_1 - x_1], [x_2, n_2 - x_2]]
                _, p_val = stats.fisher_exact(contingency)
                if p_val < alpha:
                    count += 1
            test_power = count / self._N_SIMS
            if test_power > power:
                found_solution = True
                self.power = test_power
                self.n_1 = n_1
                self.n_2 = n_2
                self.n = n
                break
        if not found_solution:
            raise BaseException("N > " + str(self._maxN) +
                                ".  You should use large sample theory.")
