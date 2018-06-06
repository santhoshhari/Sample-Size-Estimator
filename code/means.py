import scipy.stats as sc
import numpy as np


def get_power_double_side(alpha, n, k, effect_size):
    """
    Gives the power of a two tailed t-test
    For more info http://faculty.washington.edu/fscholz/DATAFILES498B2008/NoncentralT.pdf
    :return: power
    """
    c = sc.t.ppf(1 - alpha / 2, (1 + k) * n - 2)
    delta_norm = effect_size * np.sqrt(1 / (1 / n + 1 / (n * k)))
    p = 1 - sc.nct.cdf(c, (1 + k) * n - 2, delta_norm) + sc.nct.cdf(-c, (1 + k) * n - 2, delta_norm)
    return p


def get_power_one_side(alpha, n, k, effect_size):
    """
    Gives the power of a one tailed t-test
    For more info http://faculty.washington.edu/fscholz/DATAFILES498B2008/NoncentralT.pdf
    :return: power
    """
    c = sc.t.ppf(1 - alpha, (1 + k) * n - 2)
    delta_norm = effect_size * np.sqrt(1 / (1 / n + 1 / (n * k)))
    p = 1 - sc.nct.cdf(c, (1 + k) * n - 2, delta_norm)
    return p


def sample_size_t_sub(alpha=0.05, power=0.8, k=1, delta=1, one_sided=False):
    """
    Returns the sample size at which power is greater than what is required
    :return: power
    """
    # Calculate the critical point
    for i in range(2, 100):
        if one_sided:
            p = get_power_one_side(alpha, i, k, delta)
        else:
            p = get_power_double_side(alpha, i, k, delta)
        if p > power:
            return i


def sample_size_t(alpha=0.05, power=0.8, k=1, effect_size=1, one_sided=False):
    """
    Function to compute sample size for A/B test given
    the attributes of the test such as
    significance level, power and
    effect size and nature of hypothesis
    alpha and power can be float or
    list with start and end values of a range

    :param alpha: Significance level of the test
    :param power: Power of the test
    :param k: Proportion of # of samples in control to treatment
    :param one_sided: Flag to indicate if the test is one-sided
    :param effect_size : normalized effect size(∂/Standard Deviation)

    :return:
        Sample size as float if k=1 and alpha/power are floats.
        Tuple of sample sizes (control, treatment) if k!=1 and
            alpha/power are floats.
        Numpy array of size 20 (sample sizes) if k=1 and
            one of alpha/power is lists.
        Tuple of numpy arrays of size 20 each (control, treatment if k!=1) and
            one of alpha/power is lists.
    """
    if type(alpha) == list and type(power) != list:
        alpha_range = np.linspace(alpha[0], alpha[1], 20)
        if 0 in alpha:
            raise Exception(
                "Alpha can't be zero"
            )
        sample_sizes = []
        for one_alpha in alpha_range:
            s_size = sample_size_t_sub(one_alpha, power, k, effect_size, one_sided)
            sample_sizes.append(s_size)
        return sample_sizes

    elif type(power) == list and type(alpha) != list:
        power_range = np.linspace(power[0], power[1], 20)
        if 1 in power:
            raise Exception(
                "Power can't be One"
            )
        sample_sizes = []
        for one_pow in power_range:
            s_size = sample_size_t_sub(alpha, one_pow, k, effect_size, one_sided)
            sample_sizes.append(s_size)
        return sample_sizes
    elif type(power) != list and type(alpha) != list:
        return sample_size_t_sub(alpha, power, k, effect_size, one_sided)
    else:
        raise Exception(
            "Range can be submitted only for one of power/significance level"
        )
