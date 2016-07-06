import math
from skdesign.power.means import TwoSampleParallel
from skdesign.power import (is_non_negative,
                            is_positive)


class Exponential(TwoSampleParallel):
    """ Hypotheses that compares two exponential survival functions.

    Hypothesis:
        Let :math:`\\delta = \\lambda_{c} - \\lambda_{t}`.
        Equality: The test of equality tests the null hypothesis that
            :math:`\\delta \\eq 0` versus the alternative that
            :math:`\\delta \\ne 0`.
        Superiority and Non-Inferiority: The test of superiority (and the test
            of non-inferiority, which differs only in the direction of the
            comparison) tests the null hypothesis that
            :math:`\\delta \\le \\epsilon` versus the alternative that
            :math:`\\delta \\gt \\epsilon` where :math:`\\epsilon` is
            the margin above which two means are considered different.
        Equivalence: The test of equivalence tests the null hypothesis that
            :math:`|\\delta| \\ge \\epsilon` versus the alternative that
            :math:`|\\delta| \\lt \\epsilon` where :math:`\\epsilon` is
            the margin above which two means are considered different.

    Attributes:
        n_1: The control sample size.
        n_2: The treatment sample size.
        alpha: The :math:`\\alpha` level required by the hypothesis.
        beta: The :math:`\\beta` level required by the hypothesis (equal to
            :math:`1 - power`).
        power: The power required by the hypothesis (equal to
            :math:`1 - \\beta`).
        control_hazard: The hazard rate, :math:`\lambda`, of the control group.
        treatment_hazard: The hazard rate, :math:`\lambda`, of the
            treatment group.
        trial_time: The total time the trial runs, :math:`T`.
        accrual_time: The time dedicated to accrual, :math:`T_{0}`.
        gamma: The patient entry parameter.  The default is 1.
        margin: (optional) The margin of the test, :math:`\\epsilon`.  The
            default is 0.
        hypothesis: (optional) An indication of the type of hypothesis.  It is
            equal to either 'equality', 'superiority' or 'equivalence'.  The
            default is 'equality'.
        ratio: (optional) The ratio between the treatment and control sample
            sizes.  If :math:`n_{1}` is the control sample size and
            :math:`n_{2}` is the treatment sample size, the ratio, :math:`k`,
            is defined as :math:`n_{1} = k n_{2}`.  The default value is 1.

    Notes:
        The follow up time is defined as :math:`T - T_{0}`.
    """

    def __init__(self, n_1=None, n_2=None, ratio=1,
                 alpha=None, power=None, beta=None, hypothesis=None,
                 margin=None, control_hazard=None, treatment_hazard=None,
                 gamma=None, trial_time=None, accrual_time=None):

        is_positive(accrual_time, 'Accrual Time')
        is_positive(trial_time, 'Trial Time')
        if gamma is None:
            gamma = 1
        else:
            is_non_negative(gamma, 'Gamma')

        g = gamma
        t = trial_time
        t_0 = accrual_time
        variance = []

        is_positive(control_hazard, 'Control Hazard')
        is_positive(treatment_hazard, 'Treatment Hazard')

        for hazard in [control_hazard, treatment_hazard]:
            if g == 0:
                EVNum = (math.exp(-hazard * t) - math.exp(-hazard * (t - t_0)))
                EVDenom = hazard * t_0
            else:
                EVNum = (g * math.exp(-g * t) *
                         (1 - math.exp((hazard - g) * t_0)))
                EVDenom = (hazard - g) * (1 - math.exp(-g * t_0))
            EV = 1 + EVNum / EVDenom
            variance.append(hazard**2 / EV)

        stdev = math.sqrt(variance[0] / ratio + variance[1])

        # Initialize the remaining arguments through the parent.
        super(Exponential, self).__init__(n_1=n_1, n_2=n_2, ratio=ratio,
                                          mu_1=control_hazard,
                                          mu_2=treatment_hazard, stdev=stdev,
                                          known_stdev=True, alpha=alpha,
                                          beta=beta, power=power,
                                          margin=margin, hypothesis=hypothesis)
