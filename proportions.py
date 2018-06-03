import numpy as np
from scipy.stats import norm


def sample_size_z(pi1, pi2, alpha=0.05, power=0.8, k=1, one_sided=False):
    """
    Function to compute sample size for A/B test given
    proportions of both groups, a significance level, power and
    ratio of samples in control to treatment.
    alpha and power can be float or
    list with start and end values of a range

    :param pi1: Proportion of success in control group
    :param pi2: Proportion of success in treatment group
    :param alpha: Significance level of the test
    :param power: Power of the test
    :param k: Proportion of # of samples in control to treatment
    :param one_sided: Flag to indicate if the test is one-sided

    :return:
        Sample size as float if k=1 and alpha/power are floats.
        Tuple of sample sizes (control, treatment) if k!=1 and
            alpha/power are floats.
        Numpy array of size 20 (sample sizes) if k=1 and
            one of alpha/power is lists.
        Tuple of numpy arrays of size 20 each (control, treatment if k!=1) and
            one of alpha/power is lists.
    """
    effect_size = np.abs(pi2 - pi1)
    if type(alpha) == list and type(power) != list:
        alpha_range = np.linspace(alpha[0], alpha[1], 20)
        power_range = power
    elif type(power) == list and type(alpha) != list:
        alpha_range = alpha
        power_range = np.linspace(power[0], power[1], 20)
    elif type(power) != list and type(alpha) != list:
        alpha_range = alpha
        power_range = power
    else:
        raise Exception(
            "Range can be submitted only for one of power/significance level"
        )

    if not one_sided:
        alpha_range = alpha_range / 2

    z_diff = norm.ppf(alpha_range) - norm.ppf(power)
    n2 = np.square(z_diff / effect_size) * (pi1 * (1 - pi1) / k + pi2 *
                                            (1 - pi2))

    if k == 1:
        return np.ceil(n2)
    else:
        return (np.ceil(k * n2), np.ceil(n2))


if __name__ == '__main__':
    main()
