from skdesign.power import (
    PowerBase,
    is_integer
)
import scipy.stats as stats


class Normal(PowerBase):
    """ """

    # Parameters controling the simulation of power
    _N_SIMS = 1000
    _SEED = 710321

    # Parameters controling the search grid for the calculation of sample size.
    _minN = 2
    _maxN = 100

    def __init__(self, n=None, alpha=None, beta=None, power=None, method=None,
                 dist=None, seed=None, **kwargs):
        if n is not None:
            is_integer(n, '`n` should be of type Int.')
        self.n = n

        if dist in dir(stats):
            self.dist = getattr(stats, dist)(**kwargs)

        if seed is None:
            self.seed = self._SEED
        else:
            self.seed = seed

        if method == 'anderson' or method == 'anderson-darling':
            self.normal_test = stats.anderson
        elif method == 'kolmogorov-smirnov' or method == 'ks':
            def norm_ks(rvs):
                return stats.kstest(rvs, 'norm')
            self.normal_test = norm_ks
        elif method == 'kurt' or method == 'kurtosis':
            self.normal_test = stats.kurtosistest
        elif method == 'martinez-iglewicz':
            raise ValueError('{} is not a valid method'.format(method))
        elif method in ['normaltest', 'omnibus']:
            self.normal_test = stats.normaltest
        elif method == 'range':
            raise ValueError('{} is not a valid method'.format(method))
        elif method in ['shapiro', 'sw', 'shapiro-wilks']:
            self.normal_test = stats.shapiro
        elif method in ['skew', 'skewness']:
            self.normal_test = stats.skewtest
        else:
            raise ValueError('{} is not a valid method'.format(method))

        # Initialize the remaining arguments through the parent.
        super(Normal, self).__init__(alpha=alpha, power=power,
                                     beta=beta, hypothesis=None)

    def calculate(self):
        if self.n is None:
            self._set_default_alpha()
            self._set_default_power()
            self._calculate_n()
        elif self.power is None:
            self._set_default_alpha()
            self._calculate_power()
        elif self.alpha is None:
            self._calculate_alpha()

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

        found_solution = False
        for n in range(self._minN, self._maxN):
            res = self.dist(size=self._N_SIMS, random_state=self.seed)

            count = 0
            for x in res:
                _, p_val = self.normal_test(res)
                if p_val < alpha:
                    count += 1
            test_power = count / self._N_SIMS
            if test_power > power:
                found_solution = True
                self.power = test_power
                self.n = n
                break
        if not found_solution:
            raise BaseException("N is greater than maximum N")

    def calculate_power(self):
        """ Perfrom the power calculation """
        if self.alpha is None:
            alpha = 0.05
        else:
            alpha = self.alpha

        count = 0
        for sim in range(self._N_SIMS):
            res = self.dist(size=self.n, random_state=self.seed)

            _, p_val = self.normal_test(res)
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

        p_vals = []
        for sim in range(self._N_SIMS):
            res = self.dist(size=self.n, random_state=self.seed)

            _, p_val = self.normal_test(res)
            p_vals.append(p_val)
        p_vals.sort()
        self.alpha = p_vals[int(self._N_SIMS * power)]
