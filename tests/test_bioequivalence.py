from skdesign.power.bioequivalence import Average


def test_average_bioequivalence():
    """ Tests for Average Bioequivalence. """

    # See 10.2 Example from Chow et al.
    h = Average(delta=0.223, stdev=0.40, margin=0.05,
                alpha=0.05, power=0.8, known_stdev=True)
    h.calculate()
    # Chow has 21, but they have the wrong z_beta/2.  It should be 1.28,
    # not 0.84.  When that is fixed, the correct n is 23
    assert h.n == 23
    assert h.power > 0.8
