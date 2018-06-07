import plotly.graph_objs as go
from proportions import *
from means import *


def plot_sample_size(sample_size, alpha=[0.05, 0.1], power=0.8, effect_size=None, k=1):
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
    if isinstance(alpha, list):
        alpha_range = np.linspace(alpha[0], alpha[1], 20)
        if k == 1:
            data.append(go.Scatter(x=alpha_range, y=sample_size))
        else:
            data.append(
                go.Scatter(x=alpha_range, y=sample_size[0], name='Control(n1)'))
            data.append(
                go.Scatter(x=alpha_range, y=sample_size[1], name='Treatment(n2)'))
        if effect_size:
            layout = go.Layout(
                title=f'Sample Size vs α with Power(1-β) = {power}' +
                f' and δ = {effect_size}',
                font=dict(size=15))
        else:
            layout = go.Layout(
            title=f'Sample Size vs α with Power(1-β) = {power}',
            font=dict(size=15))
    elif isinstance(power, list):
        power_range = np.linspace(power[0], power[1], 20)
        if k == 1:
            data.append(go.Scatter(x=power_range, y=sample_size))
        else:
            data.append(
                go.Scatter(x=power_range, y=sample_size[0], name='Control(n1)'))
            data.append(
                go.Scatter(x=power_range, y=sample_size[1], name='Treatment(n2)'))
        if effect_size:
            layout = go.Layout(
                title=f'Sample Size vs Power(1-β) with α = {alpha}'+
                f' and δ = {effect_size}',
                font=dict(size=15))
        else:
            layout = go.Layout(
                title=f'Sample Size vs Power(1-β) with α = {alpha}',
                font=dict(size=15))
    elif isinstance(effect_size, list):
        effect_size_range = np.linspace(effect_size[0], effect_size[1], 20)
        if k == 1:
            data.append(go.Scatter(x=effect_size_range, y=sample_size))
        else:
            data.append(
                go.Scatter(x=power_range, y=sample_size[0], name='Control(n1)'))
            data.append(
                go.Scatter(x=power_range, y=sample_size[1], name='Treatment(n2)'))
        layout = go.Layout(
            title=f'Sample Size vs δ with α = {alpha} and' +
            f' Power(1-β) = {power}',
            font=dict(size=15))
    else:
        if k == 1:
            data.append(go.Scatter(x=[alpha], y=[sample_size]))
        else:
            data.append(go.Scatter(x=[alpha], y=[sample_size[0]],
                                   name='Control(n1)'))
            data.append(
                go.Scatter(x=[alpha], y=[sample_size[1]], name='Treatment(n2)'))
        if effect_size:
            layout = go.Layout(
                title=f'Sample Size with α = {alpha} and' +
                f' Power(1-β) = {power} and δ = {effect_size}',
                font=dict(size=15))
        else:
            layout = go.Layout(
                title=f'Sample Size with α={alpha} and' +
                f' Power(1-β) = {power}',
                font=dict(size=15))

    return dict(data=data, layout=layout)


def wrap_calculations(test_type='prop',
                      tailed='one',
                      alpha=[0.05, 0.05],
                      power=[0.8, 0.8],
                      effect_size=[0.5, 0.5],
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
    alpha_val = alpha[0] if alpha[0] == alpha[1] else alpha
    power_val = power[0] if power[0] == power[1] else power
    effect_size_val = effect_size[0] if effect_size[0] == effect_size[1] else effect_size
    if test_type == 'prop':
        if effect_size[0] != effect_size[1]:
            pi1 = effect_size[0]
            pi2 = effect_size[1]
        else:
            raise Exception("Choose different values of proportions")
            return None
        sample_size = sample_size_z(
            pi1,
            pi2,
            alpha=alpha_val,
            power=power_val,
            k=k,
            one_sided=tailed == 'one')
        return plot_sample_size(sample_size, alpha_val, power_val, k=k)
    elif test_type == 'mean':
        sample_size = sample_size_t(
            alpha=alpha_val,
            power=power_val,
            effect_size=effect_size_val,
            k=k,
            one_sided=tailed == 'one')
        return plot_sample_size(sample_size, alpha_val, power_val, effect_size_val, k=k)
    else:
        return None


if __name__ == '__main__':
    main()
