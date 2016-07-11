from skdesign.power import (PowerBase,
                            is_in_0_1,
                            is_integer)
import scipy.stats as stats


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
        if self.alpha is None:
            alpha = 0.05
        else:
            alpha = self.alpha
        if self.power is None:
            power = 0.8
        else:
            power = self.power

        beta = 1 - power
        for thisN in range(self._minN, self._maxN + 1):
            # First find a candidate alpha
            dist = stats.binom(thisN, self.p_0)
            lastP = 1
            for thisR in range(thisN + 1):
                thisP = 1 - dist.cdf(thisR)
                if lastP > alpha and thisP < alpha:
                    candidateR = thisR
                    break
                else:
                    lastP = thisP
            # Check the power
            dist = stats.binom(thisN, self.p)
            thisBeta = dist.cdf(candidateR)
            if thisBeta < beta:
                self.n = thisN
                self.alpha = thisP
                self.beta = thisBeta
                self.power = 1 - self.beta
                self.p
                power = 1 - thisBeta
                # Exit the function without returning anything
                return None

        # If an appropriate N is not found, fail.
        raise BaseException("N > " + str(self._maxN) +
                            ".  You should use large sample theory.")
