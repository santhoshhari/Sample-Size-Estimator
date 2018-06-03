import numpy as np
from scipy.stats import norm
import plotly.graph_objs as go


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


def plot_sample_size(sample_size, alpha=[0.05, 0.1], power=0.8, k=1):
    """
    Function to return plotly data and layout objects

    :param sample_size: sample size returned by the calculation functions
    :param alpha: Significance level of the test
    :param power: Power of the test
    :param k: Proportion of # of samples in control to treatment

    :return:
        Appropriate data and layout objects for plotting
    """
    data = list()
    if type(alpha) == list:
        alpha_range = np.linspace(alpha[0], alpha[1], 20)
        if k == 1:
            data.append(go.Scatter(x=alpha_range, y=sample_size))
        else:
            data.append(
                go.Scatter(x=alpha_range, y=sample_size[0], name='Control'))
            data.append(
                go.Scatter(x=alpha_range, y=sample_size[1], name='Treatment'))
        layout = go.Layout(
            title=f'Sample Size vs significance level with power={power}',
            font=dict(family='Balto'))
    elif type(power) == list:
        power_range = np.linspace(power[0], power[1], 20)
        if k == 1:
            data.append(go.Scatter(x=power_range, y=sample_size))
        else:
            data.append(
                go.Scatter(x=power_range, y=sample_size[0], name='Control'))
            data.append(
                go.Scatter(x=power_range, y=sample_size[1], name='Treatment'))
        layout = go.Layout(
            title=f'Sample Size vs power with significance level={alpha}',
            font=dict(family='Balto'))
    else:
        if k == 1:
            data.append(go.Scatter(x=[alpha], y=[sample_size]))
        else:
            data.append(go.Scatter(x=[alpha], y=[sample_size[0]],
                                   name='Control'))
            data.append(
                go.Scatter(x=[alpha], y=[sample_size[1]], name='Treatment'))
        layout = go.Layout(
            title=f'Sample Size with significance level={alpha} and' +
            ' power={power}',
            font=dict(family='Balto'))

    return dict(data=data, layout=layout)


def wrap_calculations(test_type='prop',
                      tailed='one',
                      alpha=[0.05],
                      power=[0.8],
                      effect_size=[0.5],
                      k=1):
    """
    Function to communicate with frontend.
    Takes inputs from dash and returns plotly objects

    :param test_type: Type of test, can take following values
        'mean' - Comparison of Means,
        'prop' - Comparison of Proportions
    :param tailed: 'one' or 'two' for one and two tailed tests respectively
    :param alpha: Significance level of the test
    :param power: Power of the test
    :param effect_size:
        Effect size for comparison of means
        Proportions for comparison of proportions
    :param k: Proportion of # of samples in control to treatment
    :param one_sided: Flag to indicate if the test is one-sided

    :return:
        Appropriate data and layout objects for plotting
    """
    if test_type == 'prop':
        alpha_val = alpha[0] if len(alpha) == 1 else alpha
        power_val = power[0] if len(power) == 1 else power
        if len(effect_size) == 2:
            pi1 = effect_size[0]
            pi2 = effect_size[1]
        else:
            raise Exception("Choose different values of proportions")
        sample_size = sample_size_z(
            pi1,
            pi2,
            alpha=alpha_val,
            power=power_val,
            k=k,
            one_sided=tailed == 'one')
        return plot_sample_size(sample_size, alpha_val, power_val, k)
    elif test_type == 'mean':
        return None
    else:
        return None


if __name__ == '__main__':
    main()
