## Sample Size Calculator for A/B Tests

Power analysis and sample size calculations are key to drawing valid conclusion from any A/B test. These address the concerns around identifying number of units required in each condition (control and treatment) of the experiment. Theoretically it is easy to consider large number of samples in experiments but in practice it is expensive (time spent, lost revenue, lost customers, etc.). This makes sample size calculations key to the the entire experimentation process.

In this repository, we have developed functions to compute sample sizes for tests involving comparison of means and comparison of proportions. The functions are flexible enough to handle multiple testing conditions like one/two-sided tests, can take in range of power/significance level/effect size. An interactive version of these functions is built as a dash version and can be launche by running the sample_size_dash_app.py file (under code folder). Please install all requirements using following command before launching the app.

`pip install -r requirements.txt`

### Formula for computing sample size

**Variable Description:**
- <img src="https://latex.codecogs.com/gif.latex?n_1" title="n_1" />: Number of samples in control group
- <img src="https://latex.codecogs.com/gif.latex?n_2" title="n_2" />: Number of samples in treatment group
- <img src="https://latex.codecogs.com/gif.latex?\delta" title="\delta" />: Effect Size in terms of standard deviation (<img src="https://latex.codecogs.com/gif.latex?\sigma" title="\sigma" />)
- <img src="https://latex.codecogs.com/gif.latex?k:n_1/n_2" title="k=n_1/n_2" />
- <img src="https://latex.codecogs.com/gif.latex?z_{\alpha/2}" title="z_{\alpha/2}" />: Z-Score corresponding to the probability of incorrectly rejecting null hypothesis
- <img src="https://latex.codecogs.com/gif.latex?z_{1-\beta}" title="z_{1-\beta}" />: Z-Score corresponding to the propability of correctly rejecting null hypothesis
- <img src="https://latex.codecogs.com/gif.latex?\pi_1" title="\pi_1" />: Proportion of success (ex - click through rate) in control group (already known)
- <img src="https://latex.codecogs.com/gif.latex?\pi_2" title="\pi_2" />: Proportion of success in treatment group (estimated)


**Sample size for comparison of means:**

<img src="https://latex.codecogs.com/gif.latex?n_2&space;=&space;(1/k&space;&plus;&space;1)(z_{\alpha/2}&space;-&space;z_{1-\beta})^2/\delta^2" title="x" />

**Sample size for comparison of proportions:**

<img src="https://latex.codecogs.com/gif.latex?n_2&space;=&space;(z_{\alpha/2}-z_{1-\beta})^2&space;[\pi_1(1-\pi_1)/k&space;&plus;&space;\pi_2(1-\pi_2)]/\delta^2" title="n_2 = (z_{\alpha/2}-z_{1-\beta})^2 [\pi_1(1-\pi_1)/k + \pi_2(1-\pi_2)]/\delta^2" />
