""" Test cases for the power.means module """

import pytest
from skdesign.power.means import OneSample


def test_one_sample():
    """ Test Cases for One Sample test of means """

    # From Chow et al. 3.1.4
    h = OneSample(mu=1, mu_0=0.5, stdev=1, alpha=0.05,
                  power=0.8, hypothesis="equality")
    h.calculate()
    assert h.n == 32
    assert h.power > 0.8

    h = OneSample(mu=1, mu_0=0.5, stdev=1, n=32,
                  power=0.8, hypothesis="equality")
    h.calculate()
    assert h.alpha < 0.05

    h = OneSample(mu=1, mu_0=0.5, stdev=1, n=32,
                  alpha=0.05, hypothesis="equality")
    h.calculate()
    assert h.power > 0.8

    h = OneSample(mu=1, mu_0=0.5, stdev=1, alpha=0.05,
                  power=0.8, margin=-0.5, hypothesis="superiority")
    h.calculate()
    assert h.n == 7
    assert h.power > 0.8

    h = OneSample(mu=1, mu_0=0.5, stdev=1, n=7,
                  power=0.8, margin=-0.5, hypothesis="superiority")
    h.calculate()
    assert h.alpha < 0.05

    h = OneSample(mu=1, mu_0=0.5, stdev=1, n=7,
                  alpha=0.05, margin=-0.5, hypothesis="superiority")
    h.calculate()
    assert h.power > 0.8

    h = OneSample(mu=1, mu_0=0.5, stdev=1, alpha=0.05,
                  power=0.8, margin=-0.5, hypothesis="superiority",
                  known_stdev=False)
    h.calculate()
    assert h.n == 8
    assert h.power > 0.8

    h = OneSample(mu=1, mu_0=0.5, stdev=1, n=8,
                  power=0.8, margin=-0.5, hypothesis="superiority",
                  known_stdev=False)
    h.calculate()
    assert h.alpha < 0.05

    h = OneSample(mu=1, mu_0=1, stdev=0.1, alpha=0.05,
                  power=0.8, margin=0.05, hypothesis="equivalence")
    h.calculate()
    assert h.n == 35
    assert h.power > 0.8

    h = OneSample(mu=1, mu_0=1, stdev=0.1, n=35,
                  power=0.8, margin=0.05, hypothesis="equivalence")
    h.calculate()
    assert h.alpha < 0.05

    h = OneSample(mu=1, mu_0=1, stdev=0.1, n=35,
                  alpha=0.05, margin=0.05, hypothesis="equivalence")
    h.calculate()
    assert h.power > 0.8

    h = OneSample(mu=1, mu_0=1, stdev=0.1, alpha=0.05,
                  power=0.9, margin=0.05, hypothesis="equivalence",
                  known_stdev=False)
    h.calculate()
    assert h.n == 36
    assert h.power > 0.8

    h = OneSample(mu=1, mu_0=1, stdev=0.1, n=36,
                  power=0.9, margin=0.05, hypothesis="equivalence",
                  known_stdev=False)
    h.calculate()
    assert h.alpha < 0.05

    h = OneSample(mu=1, mu_0=1, stdev=0.1, alpha=0.05,
                  n=36, margin=0.05, hypothesis="equivalence",
                  known_stdev=False)
    h.calculate()
    assert h.power > 0.9

    # From PASS 11 Manual pg 400-11
    h = OneSample(mu=2475, mu_0=3300, stdev=663, alpha=0.05,
                  power=0.8, hypothesis="equality",
                  known_stdev=False)
    h.calculate()
    assert h.n == 8
    assert h.power > 0.8

    h = OneSample(mu=2475, mu_0=3300, stdev=663, alpha=0.05,
                  power=0.9, hypothesis="equality",
                  known_stdev=False)
    h.calculate()
    assert h.n == 9
    assert h.power > 0.9

    h = OneSample(mu=2970, mu_0=3300, stdev=663, alpha=0.05,
                  power=0.8, hypothesis="equality",
                  known_stdev=False)
    h.calculate()
    assert h.n == 34
    assert h.power > 0.8

    h = OneSample(mu=2970, mu_0=3300, stdev=663, alpha=0.05,
                  power=0.9, hypothesis="equality",
                  known_stdev=False)
    h.calculate()
    assert h.n == 45
    assert h.power > 0.9

    h = OneSample(mu=3135, mu_0=3300, stdev=663, alpha=0.05,
                  power=0.8, hypothesis="equality",
                  known_stdev=False)
    h.calculate()
    assert h.n == 129
    assert h.power > 0.8

    h = OneSample(mu=3135, mu_0=3300, stdev=663, alpha=0.05,
                  power=0.9, hypothesis="equality",
                  known_stdev=False)
    h.calculate()
    assert h.n == 172
    assert h.power > 0.9

    h = OneSample(mu=2475, mu_0=3300, stdev=663, alpha=0.05,
                  n=8, hypothesis="equality",
                  known_stdev=False)
    h.calculate()
    assert h.power > 0.8

    h = OneSample(mu=2475, mu_0=3300, stdev=663, power=0.8,
                  n=8, hypothesis="equality",
                  known_stdev=False)
    h.calculate()
    assert h.alpha < 0.05
