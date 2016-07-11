from skdesign.power import (PowerBase,
                            is_in_0_1)
import math
import numbers
import scipy.stats as stats


class RelativeRiskParallel(PowerBase):
    """ Hypotheses for a two sample test of proportions under large sample
        theory and a parallel design using relative risks.

    The Two Sample Test of Proportions for Parallel Studies using Relative
    Risks covers three hypothesis: equality, superiority, and equivalence.
    Let :math:`OR` be the odds ratio equal to:

    :math:`OR=\\frac{p_{2}(1 - p_{1})}{p_{1}(1 - p_{2})}`

    where :math:`p_{2}` is the proportion for the treatment group and
    :math:`p_{1}` is the proportion for the control group.

    The test for equality tests :math:`H_{0}: OR=1` versus
    :math:`H_{1}: OR \\ne 1`.

    The test for superiority tests :math:`H_{0}: OR > 1` versus
    :math:`H_{1}: OR \\le 1`.

    The test for equivalence tests :math:`H_{0}: OR \ne 1` versus
    :math:`H_{1}: OR = 1`.

    Attributes:
        n: The sample size required to test the hypothesis at an
            :math:`\\alpha` level and a power of :math:`1 - \\beta` for
            group 1.
        n_1: The sample size required to test the hypothesis at an
            :math:`\\alpha` level and a power of :math:`1 - \\beta` for
            group 1.
        n_2: The sample size required to test the hypothesis at an
            :math:`\\alpha` level and a power of :math:`1 - \\beta` for
            group 2.

        alpha: The :math:`\\alpha` level required by the hypothesis.
        beta: The :math:`\\beta` level required by the hypothesis (equal to
            :math:`1 - power`).
        power: The power required by the hypothesis (equal to
            :math:`1 - \\beta`).
        hypothesis: One of 'equality', 'superiority', or 'equvalence'.  Tests
            of 'non-inferiority' are the same as tests of 'superiority' with
            respect to the power calculation so choose 'superiority' for both.
        margin: This is the superiority or equivalence margin.
        p_1: The probability for the control group
        p_2: The probability for the treatment
        ratio: The ratio of n_1 to n_2.
    """

    def __init__(self, n_1=None, n_2=None, p_1=None, p_2=None, margin=None,
                 ratio=None, hypothesis=None, alpha=None, beta=None,
                 power=None):
        is_in_0_1(p_1, '`p_1` should be in (0, 1).')
        is_in_0_1(p_2, '`p_2` should be in (0, 1).')

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

        stdev = (1 / (p_1 * (1 - p_1) * ratio)) + (1 / (p_2 * (1 - p_2)))
        stdev = math.sqrt(stdev)

        odds_ratio = math.log((p_2 * (1 - p_1)) / (p_1 * (1 - p_2)))

        if hypothesis is 'superiority':
            epsilon = odds_ratio + margin
        elif hypothesis is 'equivalence':
            epsilon = margin - abs(odds_ratio)
        else:
            epsilon = odds_ratio

        self.theta = epsilon / stdev

        # Initialize the remaining arguments through the parent.
        super(RelativeRiskParallel, self).__init__(alpha=alpha,
                                                   power=power,
                                                   beta=beta,
                                                   hypothesis=hypothesis)

    def _calculate_n_known(self):
        """ Calculate n in the case that the standard deviation is known.

        This is an internal method only.
        """
        distribution = stats.norm()
        z_alpha = distribution.ppf(1 - self.alpha / self._alpha_adjustment)
        z_beta = distribution.ppf(1 - self.beta / self._beta_adjustment)

        n_2 = (z_alpha + z_beta)**2 / self.theta**2
        self.n_2 = math.ceil(n_2)
        self.n_1 = math.ceil(self.ratio * self.n_2)

    def _calculate_alpha_known(self):
        """ Calculate :math:`\\alpha` in the case that the standard deviation
        is known.

        This is an internal method only.
        """
        distribution = stats.norm()
        z_beta = distribution.ppf(1 - self.beta / self._beta_adjustment)
        z_alpha = math.sqrt(self.n_2) * self.theta - z_beta

        self.alpha = (1 - distribution.cdf(z_alpha)) * self._alpha_adjustment

    def _calculate_power_known(self):
        """ Calculate power in the case that the standard deviation is known.

        This is an internal method only.
        """
        distribution = stats.norm()
        z_alpha = distribution.ppf(1 - self.alpha / self._alpha_adjustment)
        z_beta = math.sqrt(self.n_2) * self.theta - z_alpha

        self.beta = (1 - stats.norm.cdf(z_beta)) * self._beta_adjustment
        self.power = 1 - self.beta

    def calculate(self):
        if self.n is None:
            self._set_default_alpha()
            self._set_default_power()
            self._calculate_n_known()
            self._calculate_power_known()
        elif self.power is None:
            self._set_default_alpha()
            self._calculate_power_known()
        elif self.alpha is None:
            self._calculate_alpha_known()

    def __repr__(self):
        """ The canonical representation of a TwoSampleParallel object
        """
        representation = "Alpha: " + str(self.alpha) + "\n" + \
                         "Power: " + str(self.power) + "\n" + \
                         "Sample Size (Group 1): " + str(self.n_1) + "\n" \
                         "Sample Size (Group 2): " + str(self.n_2) + "\n"
        return representation
