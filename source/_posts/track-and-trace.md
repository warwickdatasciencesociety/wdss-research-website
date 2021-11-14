---
title: "Reinventing Test and Trace: A Bayesian Approach For Modelling SARS-CoV-2 Setting-Specific Transmission"
date: 2021-11-14
updated: 2021-11-14
authors_plus:
- "Tim Hargreaves"
- "Patricio Hernandez"
contacts_plus:
- "https://www.linkedin.com/in/tim-hargreaves/"
- "https://www.linkedin.com/in/patriciohdzs/"
tags:
- covid19
- bayesian-modelling
- track-and-trace
categories:
- []
languages:
- python, r, stan
description: "One of the key failures many countries had in dealing with the COVID-19 pandemic was a lack of coherent, data-driven analysis on setting-specific transmission risk. In this article, we outline a novel first-principles hierarchical Bayesian model for setting-specific transmission that, alongside the corresponding data collection methodology, could help governments in determining pandemic control policy"
cover: /banners/covid.jpg
---
## Introduction 

It is no secret that the response of multiple countries following the outbreak of the COVID-19 pandemic has been abismal - and the UK is no exception. With £355 billion amounting in economic losses (OBR, 2021), a 4.8% rate of unemployment (ONS, 2021) and, perhaps most shockingly, over 128,000 deaths to this date (Gov.uk, 2021), the UK government has undoubtedly handled this crisis poorly, with two key government-led programmes standing out amongst the list of policy failures. 

The Test and Trace programme, established to curb Coronavirus reproduction, aims to provide accessible testing as well as contact tracing to notify exposed individuals and instruct them to self-isolate. One major failure of the T&T programme has been the lack of a coherent data collection strategy for analysing setting-specific transmission; that is, the relative likelihood of contracting COVID in different locations, such as a hair dresser, a restaurant, etc. Given the dependence of the UK Tier System on our understanding of setting-specific transmission, this alone serves as an explanation of the latter's failure, as settings grouped together often bear no resemblance in terms of their underlying transmission rates, resulting in unnecessary business closures and contributing to the economic hemorrhage.

Thus, we set out to formulate a data collection and analysis methodology that is both compatible with the current T&T programme and enables us to model and estimate setting-specific COVID-19 transmission rates, in the hope of guiding lockdown policies using a reliable, data-driven approach.

## Our approach and assumptions

### Data collection methodology
Starting out, our goal was to model a random vector $\boldsymbol{\theta} \in [0,1]^P$ of transmission rates for $P$ different settings. To estimate this model, we would require data that could be feasibly collected through the T&T programme. Therefore, we devised the following data collection strategy to accompany the probabilistic model developed below, making sure to prioritize its feasibility and scalability:

1. Data is to be collected from individuals in the T&T programme through a short survey of binary responses on whether or not they visited each one of $P$ locations in the last few days.

2. For each individual surveyed through T&T, the result of their COVID-19 antigen test is also observed.

3. Finally, a random survey is also sent out. This survey is identical to the one in (1.) but, since it is not distributed by T&T, no antigen test is taken and therefore no outcome is observed.


### Model assumptions
In order for us to combine this data collection methodology with a statistical model that allows for inference on the estimated setting-specific transmission rates, we had to lay down the following assumptions:

- Multiple visits to a location in one week are rare enough to be ignored or in cases (such as supermarkets) where multiple visits are expected, the distribution of number of visits is tight.

## Building a first-principles model

Given the data collection strategy detailed above, for each individual, we observe a binary vector $\boldsymbol{x}_i \in \{0,1\}^{P}$, which indicates their responses on the location visits survey, and random variable $y_i \in \{0,1\}$ which indicates if they tested positive for COVID-19.

### The base model

We formulate our model generatively through the latent transmission vector $\boldsymbol{t}_i \in \{0,1\}^{P}$, which follows a multivariate Bernoulli distribution with transmission probabilities dependent on the individual's attendance to each setting and the respective setting-specific transmission rates. Furthermore, we capture the case of COVID transmission in a location not specified by the survey through the latent variable $b_i \in \{0,1\}^{P}$, which is analogous to $\boldsymbol{t}_i$, but parameterized by the underlying base transmission risk: 

$$\boldsymbol{t}_i \sim \text{Ber}(\boldsymbol{x}_i \circ \boldsymbol{\theta})$$

$$b_i \sim \text{Ber}(\rho)$$

We denote whether or not the individual contracted COVID-19 with the binary variable $w_i$ and define it using the natural relationship with the aforementioned latent variables. Since transmission in any of the settings surveyed or in some other unaccounted location results in contraction, we define $w_i$ as the indicator of this scenario:

$$w_i=\mathbb{1}\{\textbf{1}^\text{T}\boldsymbol{t}_i + b_i>0\}$$

### Curbing selection bias

The next challenge for our model was to account for selection bias in T&T survey observations. More specifically, infected individuals (who feel unwell and present symptoms) are more likely to get in contact with T&T and hence select into the survey, thus introducing bias into any transmission rate estimates. To mitigate this, we collect observations of $\boldsymbol{x}_i$ from a random survey and define $s_i$ to indicate whether or not the observation came from T&T:
$$s_i=\begin{cases} 
            1,\; \text{T&T sample} \\
            0,\; \text{otherwise}
            \end{cases}$$
            
From there, we utilize $s_i$ to define the testing rates as the probability of getting tested conditional on being COVID-19 infected, and use these to weight down the transmission likelihood for our observations.


$$ \mathbb{P}(s_i=1|w_i=1) = \gamma_+ $$
$$ \mathbb{P}(s_i=1|w_i=0) = \gamma_- $$

### Addressing inaccurate tests

Similarly, we also account for false positive and negative antigen test results by defining the test sensitivity and specificity parameters through the conditional probability of testing positive given infected and testing negative given non-infected, respectively:

$$\mathbb{P}(y_i=1|w_i=1) = \lambda_+$$

$$\mathbb{P}(y_i=0|w_i=0) = \lambda_-$$

### Hierarchical extension

We modeled the hierarchical nature of setting-specific transmission by grouping each setting into one of $K$ encompassing classes of similar settings: $c[p]:[P] \to [K]$. For each class, we model transmission rates of member settings as draws from a [logit-normal](https://en.wikipedia.org/wiki/Logit-normal_distribution) distribution, parameterized by the mean class transmission rate $\boldsymbol{\mu} \in [0,1]^K,$ and the class transmission rate variance $\, \boldsymbol{\sigma}^2 \in \mathbb{R}_{>0}^K$. It should be noted that :

$$\theta_p \sim \text{Logitnormal}\left(\text{logit}\left(\mu_{c[p]}\right) \;,\; \sigma_{c[p]}^{2} \right)$$


### Modelling policy interventions

Finally, we also wanted to model the effect of policy interventions on different setting classes to answer questions such as: *"Does social distancing have different effects in cinemas than in restaurants?"* To do this, we can introduce policy intervention parameters and model out their interactions with different setting transmission rates, provided our data collection methodology can be feasibly extended to collect the data necessary to pin down these additional parameters. 

We exemplify this with the mask-wearing intervention, with the objective of estimating the different effects mask-wearing can have in different settings. To do this, we could extend our data collection survey to ask individuals about their mask-wearing habits, allowing us to define $m_i$ as an indicator for habitual mask-wearers:

$$m_i=\begin{cases} 
            1,\; \text{habitual mask-wearing} \\
            0,\; \text{otherwise}
            \end{cases}$$
 
 
This additional data then allows us to incorporate and estimate $\iota_{c[p]}$ as the class-specific mas wearing impact on transmission rates: 
 
 
$$\theta_{ip} \sim \text{Logitnormal}\left(\, \text{logit}\left(\mu_{c[p]}\right) + m_i \log\left(\iota_{c[p]}\right) \;,\; \sigma_{c[p]}^{2} \,\right)$$ 

Modeling policy interventions in this way allows for a clear-cut interpretation of the intervention effect parameter. More specifically, with a little algebra, it becomes evident that $\iota_{c[p]}$ essentially acts as a multiplier effect on the average class transmission odds:

$$\log\left(\frac{\mu_{c[p]}}{1-\mu_{c[p]}} \right) \rightarrow \log\left(\iota_{c[p]} \frac{\mu_{c[p]}}{1-\mu_{c[p]}} \right)$$

## Simulating our data

### Metadata
In order to be test out this model, the following metadata must be defined in relation to the application context:
- $P:$ A vector containing the number of settings per class
- $K:$ The number of setting classes considered in the model 
- $N:$ The total population
- $S:$ The number of random surveys sent out
- $T:$ The total number of T&T samples

In particular, it is worth highlighting that $N,S,$ and $T$ are constrained by the following:

$$N \geq S+T$$

It is assumed that, in the typical case, both $N$ and $T$ are predetermined, and the authority applying the model gets to choose $S$ subject to the above. In our simulation, $N$ and $S$ are pre-set and $T$ is randomly determined given the simulated testing rates.


```python
#### METADATA ####
P = [3, 5, 1, 4, 1, 2, 1, 1, 4]    # Number of settings per class 
N = 10000                          # Total population
S = 8000                           # Number of random surveys sent out
SEED = 1729                        # Random seed
```

### Population ground truth
Since we our data collection strategy is (an ideal) hypothetical, to test our model we must first specify a ground truth for the population parameters and then simulate our data accordingly. To this end we sampled our population parameters as follows, making sure to try a range of values for these to ensure model robustness:

|Parameter                       |Model Notation|Simulation|Model Priors|
|--------------------------------|------------------|----------|------------|
|Setting transmission rates      |$\theta_{ip}$     |Logit-normal distribution parameterized by class transmission rate mean and variance| $U(0,1)$ |
|Mean class transmission rates   |$\mu_{c[p]}$      |Beta distribution|$U(0,1)$|
|Class transmission rate variance|$\sigma^2_{c[p]}$ |Inverse gamma distribution|$\text{Inv-Gamma}(10, 1)$|
|Base transmission rate          |$\rho$            |Beta distribution|$U(0,1)$|
|Class-specific mask impact      |$\iota_{c[p]}$    |Normal with negative mean|$\mathcal{N}(-1, 1)$|
|Testing rates                   |$\gamma_{+,\,-}$          |Beta distribution|$U(0,1)$|
|Test precision and recall rates |$\lambda_{+,\,-} $         |Beta distribution|$\text{Beta}(\alpha*, \beta*)$, with shape hyperparameters calibrated to match the antigen test sensitivity and specificity results from the [Joint PHE Porton Down & University of Oxford SARS-CoV-2 test development and validation cell](https://www.ox.ac.uk/sites/files/oxford/media_wysiwyg/UK%20evaluation_PHE%20Porton%20Down%20%20University%20of%20Oxford_final.pdf)|

## Fitting our Model

### Our model in Stan

We implemented the code for our first-principles model using Stan, a probabilistic inference language compiled in C++. Stan allows users to carry out full Bayesian inference on statistical models via Markov Chain Monte Carlo (MCMC) sampling, and enables model specification in a block-like fashion. The main building blocks for our Stan model are:
1. The data block, which specifies the type and dimensions of data used to train the model.
2. The parameter block, which specifies all underlying statistical parameters of the model.
3. The model block, which assigns parameter priors and constructs the model likelihood describing the joint probability of the observed data as a function of the parameters.

With computational feasibility in mind, we also coded a version of our model using the TensorFlow Probability framework, as this version supports the use of GPU's and distributed computing capabilities to deliver greater computational power. For a more extensive review of the code produced, please refer to the project [GitHub repository.](https://github.com/THargreaves/reinventing-test-and-trace) 

``` Stan
model_code = """
functions {
  real expit_gaussian_lpdf(real y, real logit_mu, real sigma2) {
    return log(1 / y + 1 / (1 - y)) - (logit(y) - logit_mu)^2 / (2 * sigma2);
  }
}
data {
  int<lower=0> T;                            // number of T&T observations
  int<lower=0> S;                            // number of survey observations
  int<lower=0> P;                            // number of settings
  int<lower=0> K;                            // number of classes
  int<lower=0, upper=1> X[T,P];              // activity occurrences
  int<lower=0, upper=1> y[T];                // transmission (tested positive)
  int<lower=0, upper=1> survey[S,P];         // activity occurrences of surveyed individuals
  real lambda_prior_params[2,2];             // shape parameters for TP/TN test rate priors
  int<lower=1, upper=K> c[P];                // setting classes
  int<lower=0, upper=1> m[T];                // masking-wearing
  int<lower=0, upper=1> m_survey[S];         // masking-wearing
}
parameters {
  real<lower=0, upper=1> theta[P];           // transmission rates
  real<lower=0, upper=1> mu[K];              // class transmission means
  real<lower=0> sigma2[K];                   // class transmission variances
  real<lower=0, upper=1> gamma[2];           // Testing rates, given infected status [s|w , s|!w]
  real<lower=0, upper=1> lambda[2];          // True positive and true negative rates of tests [TP,TN]
  real<lower=0, upper=1> rho;                // underlying risk
  real iota[K];                              // intervention impacts (log)
}
transformed parameters {
  // Pre-computation for efficiency
  real log1m_theta[P] = log1m(theta);
  real log1m_theta_int[P];
  real log1m_rho = log1m(rho);
  real logit_mu[K] = logit(mu);
  real log_gamma[2];
  real log1m_gamma[2];
  real log_lambda[2];
  real log1m_lambda[2];

  for (p in 1:P) {
    log1m_theta_int[p] = log1m_inv_logit(logit(theta[p]) + iota[c[p]]);
  } 
  
  log1m_theta = log1m(theta); 
  log_gamma = log(gamma);
  log1m_gamma = log1m(gamma);
  log_lambda = log(lambda);
  log1m_lambda = log1m(lambda);
}
model {
  // Priors
  //mu ~ beta(1, 5);
  mu ~ uniform(0, 1);
  sigma2 ~ inv_gamma(10, 1);
  rho ~ beta(1, 3);
  iota ~ normal(-1, 1);
  gamma ~ uniform(0, 1);
  lambda[1] ~ beta(lambda_prior_params[1,1],lambda_prior_params[1,2]);
  lambda[2] ~ beta(lambda_prior_params[2,1],lambda_prior_params[2,2]);
  
  // Likelihood (classes)
  for (p in 1:P) {
    theta[p] ~ expit_gaussian(logit_mu[c[p]], sigma2[c[p]]);
  }
  
  // Likelihood (survey)
  for (n in 1:S) {
    real s = 0.0;
    for (p in 1:P) {
      if (survey[n,p] == 1) {
        if (m_survey[n] == 1) {
          s += log1m_theta_int[p];
        } else {
          s += log1m_theta[p];
        }
      }
    }
    s += log1m_rho;
    target += log_sum_exp((log1m_exp(s)+log1m_gamma[1]), (s+log1m_gamma[2]));
  }
  // Likelihood (T&T observations)
  for (n in 1:T) {
    real s = 0.0;
    for (p in 1:P) {
      if (X[n,p] == 1) {
        if (m[n] == 1) {
          s += log1m_theta_int[p];
        } else {
          s += log1m_theta[p];
        }
      }
    }
    s += log1m_rho;
    if (y[n] == 1) {
      target += log_sum_exp((log1m_exp(s) + log_gamma[1] + log_lambda[1]), (s + log_gamma[2] + log1m_lambda[2]));
    } else {
      target += log_sum_exp((s + log_gamma[2] + log_lambda[2]), (log1m_exp(s) + log_gamma[1] + log1m_lambda[1]));
    }
  }
}
"""
```

### Markov Chain Monte Carlo Posterior Sampling

In general, the aim of Bayesian inference is to derive the posterior distribution of our parameters by defining it mathematically using Bayes' theorem as below, where $p(\theta)$ is the parameter prior and $p(\boldsymbol{X}\,|\,\theta )$ is the model likelihood:

$$p(\theta \,|\,\boldsymbol{X}) \;=\; \frac{p(\theta) \, p(\boldsymbol{X}\,|\,\theta )}{p( \boldsymbol{X})}$$

Unfortunately, this distribution in our model (as is the case for most Bayesian models) cannot be evaluated analytically given the highly-dimensional parameter space. To overcome this, Stan utilizes the NUTS algorithm (part of the general class of MCMC methods) to infer the posterior distribution by repeatedly drawing samples from it, even though its full closed-form characterization is unknown. Unlike regular Monte Carlo sampling, which draws independent samples, MCMC allows for 'smarter' sampling as it draws correlated samples from the stationary distribution of a Markov chain that's proportional to the desired distribution. This allows for the sampling process to enter regions of high density much faster. For more details regarding how Stan achieves this using the NUTS algorithm, the interested reader should refer to [this link.](https://mc-stan.org/docs/2_18/reference-manual/hmc-chapter.html) 

At its core, there are three hyperparamters that need to be specified for MCMC sampling with the NUTS algorithm.
Firstly, the `num_warmup` parameter is used to specify the number of samples that are discarded as burn-in. This is done in order to allow convergence onto the stationary distribution of the Markov chain. Secondly, the `n_samples` parameter specifies the number of samples to be drawn from the distribution. Finally, `n_chains` specifies the number of chains that should be constructed, as using more well-mixed chains increases robustness. 


```python
### MCMC SAMPLING HYPERPARAMETERS ####
ITER = 1000
WARMUP = 500
CHAINS = 8
SEED = 1729

#### MODEL FITTING ####
# Define model data
model_data = {
    'T': T, 'S': S, 'P': sum(P), 'K': len(P),
    'X': X.to_numpy(), 'y': y.to_numpy(), 'c': c, 'm': m, 'm_survey': m_survey,
    'survey': X_survey.to_numpy(), 'lambda_prior_params':prior_params,
}

# Compile model
posterior = stan.build(model_code, data=model_data, random_seed=1)

# Fit model
fit = posterior.sample(num_samples=ITER, num_warmup=WARMUP, num_chains=CHAINS)
```

## Results and conclusion

### Visualizing posterior samples

After running our model, we computed the summary statistics of our posterior samples in the table below. Additionally, we visualize these in the subsequent traceplots, which show the distributions for all $P$ setting transmission rates, as well as the other model parameters, in the left, and the sampled values on the right. Overall, we can see that there was proper chain mixing given both the shape of our sampled value traces and the $\hat{R}$ statistics (equal to one for all model parameters), which suggests that improper model parametrization is unlikely to be an issue. 





<table>
  <thead>
    <tr>
      <th></th>
      <th>mean</th>
      <th>sd</th>
      <th>hdi_3%</th>
      <th>hdi_97%</th>
      <th>mcse_mean</th>
      <th>mcse_sd</th>
      <th>ess_mean</th>
      <th>ess_sd</th>
      <th>ess_bulk</th>
      <th>ess_tail</th>
      <th>r_hat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>theta[0]</th>
      <td>0.250</td>
      <td>0.111</td>
      <td>0.042</td>
      <td>0.444</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>4090.0</td>
      <td>4090.0</td>
      <td>3711.0</td>
      <td>3200.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[1]</th>
      <td>0.224</td>
      <td>0.101</td>
      <td>0.042</td>
      <td>0.410</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>4116.0</td>
      <td>4116.0</td>
      <td>3688.0</td>
      <td>3103.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[2]</th>
      <td>0.212</td>
      <td>0.098</td>
      <td>0.040</td>
      <td>0.390</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>4352.0</td>
      <td>4352.0</td>
      <td>3834.0</td>
      <td>3492.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[3]</th>
      <td>0.228</td>
      <td>0.098</td>
      <td>0.053</td>
      <td>0.404</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>2733.0</td>
      <td>2733.0</td>
      <td>2720.0</td>
      <td>3567.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[4]</th>
      <td>0.231</td>
      <td>0.099</td>
      <td>0.066</td>
      <td>0.420</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>2788.0</td>
      <td>2787.0</td>
      <td>2807.0</td>
      <td>3854.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[5]</th>
      <td>0.223</td>
      <td>0.097</td>
      <td>0.062</td>
      <td>0.410</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>2890.0</td>
      <td>2877.0</td>
      <td>2818.0</td>
      <td>3744.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[6]</th>
      <td>0.267</td>
      <td>0.108</td>
      <td>0.080</td>
      <td>0.471</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>2956.0</td>
      <td>2956.0</td>
      <td>2817.0</td>
      <td>3703.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[7]</th>
      <td>0.262</td>
      <td>0.110</td>
      <td>0.076</td>
      <td>0.470</td>
      <td>0.002</td>
      <td>0.002</td>
      <td>2323.0</td>
      <td>2323.0</td>
      <td>2254.0</td>
      <td>3422.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[8]</th>
      <td>0.189</td>
      <td>0.127</td>
      <td>0.000</td>
      <td>0.408</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>5756.0</td>
      <td>5756.0</td>
      <td>4251.0</td>
      <td>2878.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[9]</th>
      <td>0.314</td>
      <td>0.088</td>
      <td>0.153</td>
      <td>0.476</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>4434.0</td>
      <td>4431.0</td>
      <td>4447.0</td>
      <td>5614.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[10]</th>
      <td>0.322</td>
      <td>0.092</td>
      <td>0.154</td>
      <td>0.495</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>4290.0</td>
      <td>4290.0</td>
      <td>4273.0</td>
      <td>5728.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[11]</th>
      <td>0.282</td>
      <td>0.085</td>
      <td>0.131</td>
      <td>0.437</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>4411.0</td>
      <td>4323.0</td>
      <td>4461.0</td>
      <td>5124.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[12]</th>
      <td>0.304</td>
      <td>0.087</td>
      <td>0.150</td>
      <td>0.470</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>4219.0</td>
      <td>4200.0</td>
      <td>4279.0</td>
      <td>5716.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[13]</th>
      <td>0.223</td>
      <td>0.146</td>
      <td>0.000</td>
      <td>0.476</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>6577.0</td>
      <td>6577.0</td>
      <td>5525.0</td>
      <td>4074.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[14]</th>
      <td>0.210</td>
      <td>0.111</td>
      <td>0.021</td>
      <td>0.414</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>4139.0</td>
      <td>4139.0</td>
      <td>3687.0</td>
      <td>3482.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[15]</th>
      <td>0.236</td>
      <td>0.122</td>
      <td>0.028</td>
      <td>0.458</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>4540.0</td>
      <td>4540.0</td>
      <td>4006.0</td>
      <td>3202.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[16]</th>
      <td>0.133</td>
      <td>0.103</td>
      <td>0.000</td>
      <td>0.318</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>6605.0</td>
      <td>6605.0</td>
      <td>4609.0</td>
      <td>2862.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[17]</th>
      <td>0.207</td>
      <td>0.128</td>
      <td>0.001</td>
      <td>0.430</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>4882.0</td>
      <td>4882.0</td>
      <td>3842.0</td>
      <td>2402.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[18]</th>
      <td>0.222</td>
      <td>0.105</td>
      <td>0.043</td>
      <td>0.415</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>3161.0</td>
      <td>3161.0</td>
      <td>3078.0</td>
      <td>4504.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[19]</th>
      <td>0.230</td>
      <td>0.109</td>
      <td>0.046</td>
      <td>0.428</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>3269.0</td>
      <td>3269.0</td>
      <td>3178.0</td>
      <td>4160.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[20]</th>
      <td>0.189</td>
      <td>0.090</td>
      <td>0.037</td>
      <td>0.353</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>3694.0</td>
      <td>3694.0</td>
      <td>3518.0</td>
      <td>4593.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>theta[21]</th>
      <td>0.215</td>
      <td>0.102</td>
      <td>0.045</td>
      <td>0.408</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>3363.0</td>
      <td>3363.0</td>
      <td>3232.0</td>
      <td>4370.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>rho</th>
      <td>0.211</td>
      <td>0.064</td>
      <td>0.087</td>
      <td>0.332</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>5180.0</td>
      <td>5180.0</td>
      <td>5262.0</td>
      <td>3748.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>mu[0]</th>
      <td>0.230</td>
      <td>0.100</td>
      <td>0.053</td>
      <td>0.419</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>3899.0</td>
      <td>3899.0</td>
      <td>3493.0</td>
      <td>2856.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>mu[1]</th>
      <td>0.241</td>
      <td>0.093</td>
      <td>0.080</td>
      <td>0.418</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>2338.0</td>
      <td>2338.0</td>
      <td>2262.0</td>
      <td>3169.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>mu[2]</th>
      <td>0.202</td>
      <td>0.138</td>
      <td>0.000</td>
      <td>0.447</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>5961.0</td>
      <td>5961.0</td>
      <td>4364.0</td>
      <td>2970.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>mu[3]</th>
      <td>0.307</td>
      <td>0.080</td>
      <td>0.164</td>
      <td>0.455</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>3525.0</td>
      <td>3512.0</td>
      <td>3531.0</td>
      <td>4945.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>mu[4]</th>
      <td>0.234</td>
      <td>0.154</td>
      <td>0.000</td>
      <td>0.504</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>6848.0</td>
      <td>6848.0</td>
      <td>5735.0</td>
      <td>3834.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>mu[5]</th>
      <td>0.228</td>
      <td>0.117</td>
      <td>0.027</td>
      <td>0.444</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>4374.0</td>
      <td>4374.0</td>
      <td>3914.0</td>
      <td>3227.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>mu[6]</th>
      <td>0.145</td>
      <td>0.114</td>
      <td>0.000</td>
      <td>0.351</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>7078.0</td>
      <td>7078.0</td>
      <td>4699.0</td>
      <td>2933.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>mu[7]</th>
      <td>0.219</td>
      <td>0.139</td>
      <td>0.000</td>
      <td>0.460</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>5242.0</td>
      <td>5242.0</td>
      <td>4052.0</td>
      <td>2295.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>mu[8]</th>
      <td>0.214</td>
      <td>0.096</td>
      <td>0.051</td>
      <td>0.391</td>
      <td>0.002</td>
      <td>0.001</td>
      <td>3137.0</td>
      <td>3137.0</td>
      <td>3025.0</td>
      <td>3789.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>sigma2[0]</th>
      <td>0.131</td>
      <td>0.051</td>
      <td>0.056</td>
      <td>0.220</td>
      <td>0.001</td>
      <td>0.000</td>
      <td>7513.0</td>
      <td>5708.0</td>
      <td>10852.0</td>
      <td>5458.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>sigma2[1]</th>
      <td>0.150</td>
      <td>0.062</td>
      <td>0.061</td>
      <td>0.260</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>6404.0</td>
      <td>5250.0</td>
      <td>8836.0</td>
      <td>5385.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>sigma2[2]</th>
      <td>0.118</td>
      <td>0.043</td>
      <td>0.053</td>
      <td>0.193</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>8280.0</td>
      <td>6082.0</td>
      <td>12257.0</td>
      <td>5441.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>sigma2[3]</th>
      <td>0.135</td>
      <td>0.053</td>
      <td>0.059</td>
      <td>0.226</td>
      <td>0.001</td>
      <td>0.001</td>
      <td>7057.0</td>
      <td>5298.0</td>
      <td>10888.0</td>
      <td>5228.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>sigma2[4]</th>
      <td>0.117</td>
      <td>0.043</td>
      <td>0.054</td>
      <td>0.196</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>9024.0</td>
      <td>6569.0</td>
      <td>13371.0</td>
      <td>5450.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>sigma2[5]</th>
      <td>0.125</td>
      <td>0.048</td>
      <td>0.054</td>
      <td>0.211</td>
      <td>0.001</td>
      <td>0.000</td>
      <td>8224.0</td>
      <td>6024.0</td>
      <td>12240.0</td>
      <td>5518.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>sigma2[6]</th>
      <td>0.118</td>
      <td>0.043</td>
      <td>0.056</td>
      <td>0.200</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>8184.0</td>
      <td>5615.0</td>
      <td>13440.0</td>
      <td>5532.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>sigma2[7]</th>
      <td>0.118</td>
      <td>0.043</td>
      <td>0.055</td>
      <td>0.198</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>7992.0</td>
      <td>5761.0</td>
      <td>12288.0</td>
      <td>4824.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>sigma2[8]</th>
      <td>0.138</td>
      <td>0.052</td>
      <td>0.058</td>
      <td>0.232</td>
      <td>0.001</td>
      <td>0.000</td>
      <td>7786.0</td>
      <td>6455.0</td>
      <td>9620.0</td>
      <td>5729.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>iota[0]</th>
      <td>-0.954</td>
      <td>0.619</td>
      <td>-2.131</td>
      <td>0.208</td>
      <td>0.008</td>
      <td>0.006</td>
      <td>5775.0</td>
      <td>5775.0</td>
      <td>5852.0</td>
      <td>4816.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>iota[1]</th>
      <td>-1.256</td>
      <td>0.566</td>
      <td>-2.343</td>
      <td>-0.197</td>
      <td>0.009</td>
      <td>0.006</td>
      <td>4263.0</td>
      <td>4263.0</td>
      <td>4302.0</td>
      <td>4532.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>iota[2]</th>
      <td>-1.390</td>
      <td>0.864</td>
      <td>-2.993</td>
      <td>0.262</td>
      <td>0.009</td>
      <td>0.007</td>
      <td>9762.0</td>
      <td>8061.0</td>
      <td>9793.0</td>
      <td>6472.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>iota[3]</th>
      <td>-1.571</td>
      <td>0.429</td>
      <td>-2.392</td>
      <td>-0.812</td>
      <td>0.006</td>
      <td>0.004</td>
      <td>5454.0</td>
      <td>5227.0</td>
      <td>5576.0</td>
      <td>5157.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>iota[4]</th>
      <td>-1.163</td>
      <td>0.866</td>
      <td>-2.829</td>
      <td>0.437</td>
      <td>0.008</td>
      <td>0.007</td>
      <td>10823.0</td>
      <td>7689.0</td>
      <td>10823.0</td>
      <td>6792.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>iota[5]</th>
      <td>-0.620</td>
      <td>0.734</td>
      <td>-2.014</td>
      <td>0.734</td>
      <td>0.009</td>
      <td>0.007</td>
      <td>5981.0</td>
      <td>4847.0</td>
      <td>6037.0</td>
      <td>5498.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>iota[6]</th>
      <td>-1.295</td>
      <td>0.875</td>
      <td>-2.947</td>
      <td>0.376</td>
      <td>0.009</td>
      <td>0.007</td>
      <td>10158.0</td>
      <td>7307.0</td>
      <td>10212.0</td>
      <td>6283.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>iota[7]</th>
      <td>-1.039</td>
      <td>0.850</td>
      <td>-2.644</td>
      <td>0.550</td>
      <td>0.009</td>
      <td>0.007</td>
      <td>9000.0</td>
      <td>6438.0</td>
      <td>9066.0</td>
      <td>6105.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>iota[8]</th>
      <td>-0.505</td>
      <td>0.599</td>
      <td>-1.628</td>
      <td>0.633</td>
      <td>0.009</td>
      <td>0.006</td>
      <td>4381.0</td>
      <td>4381.0</td>
      <td>4388.0</td>
      <td>4901.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>gamma[0]</th>
      <td>0.461</td>
      <td>0.018</td>
      <td>0.429</td>
      <td>0.497</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>2755.0</td>
      <td>2747.0</td>
      <td>2819.0</td>
      <td>3925.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>gamma[1]</th>
      <td>0.191</td>
      <td>0.015</td>
      <td>0.162</td>
      <td>0.219</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>10384.0</td>
      <td>10364.0</td>
      <td>10370.0</td>
      <td>5707.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>lambda[0]</th>
      <td>0.747</td>
      <td>0.020</td>
      <td>0.712</td>
      <td>0.785</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>3566.0</td>
      <td>3554.0</td>
      <td>3625.0</td>
      <td>5333.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>lambda[1]</th>
      <td>0.997</td>
      <td>0.001</td>
      <td>0.996</td>
      <td>0.998</td>
      <td>0.000</td>
      <td>0.000</td>
      <td>15214.0</td>
      <td>15214.0</td>
      <td>15246.0</td>
      <td>5420.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>




![](/images/track-and-trace/track-and-trace_26_0.png)


### Comparison with ground truth 

After fitting, one key question is the extent to which our model is successful in estimating the underlying transmission rates. To test this, we take the posterior mean as the [minimum mean squared error estimate](https://en.wikipedia.org/wiki/Bayes_estimator) and compare it to the ground-truth parameters used to simulate the data-generating process. As shown in the table below, most parameter estimates fall reasonably close from the actual ground truth values, and all of them fall within the 94% high density interval (HDI), serving as a good indicator of our model's accuracy. 

The key condition for this comparison as proof-of-concept is the fact that our model only observes the parameter priors and the training data, but never the simulating distributions themselves. Moreover, excluding the case of antigen test accuracy rates, the priors as specifically chosen to be largely uninformative relative to the simulating distribution in order to limit the unreasonable influence of these on model performance.

Finally, a question of interest is how the accuracy of the model is affected by the number of training samples or the dimension of the parameter space. The results for both of these questions are excluded for brevity, but they tend to fall in line with what would be expected (model accuracy increases with training data and decreases with dimensionality) and the interested reader should consult the project repository for more details.





<table>
  <thead>
    <tr>
      <th></th>
      <th>Ground Truth</th>
      <th>Posterior Mean</th>
      <th>HDI 3%</th>
      <th>HDI 97%</th>
    </tr>
    <tr>
      <th>Parameter</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>theta[0]</th>
      <td>0.125388</td>
      <td>0.250</td>
      <td>0.042</td>
      <td>0.444</td>
    </tr>
    <tr>
      <th>theta[1]</th>
      <td>0.129571</td>
      <td>0.224</td>
      <td>0.042</td>
      <td>0.410</td>
    </tr>
    <tr>
      <th>theta[2]</th>
      <td>0.127706</td>
      <td>0.212</td>
      <td>0.040</td>
      <td>0.390</td>
    </tr>
    <tr>
      <th>theta[3]</th>
      <td>0.121898</td>
      <td>0.228</td>
      <td>0.053</td>
      <td>0.404</td>
    </tr>
    <tr>
      <th>theta[4]</th>
      <td>0.141731</td>
      <td>0.231</td>
      <td>0.066</td>
      <td>0.420</td>
    </tr>
    <tr>
      <th>theta[5]</th>
      <td>0.141376</td>
      <td>0.223</td>
      <td>0.062</td>
      <td>0.410</td>
    </tr>
    <tr>
      <th>theta[6]</th>
      <td>0.116330</td>
      <td>0.267</td>
      <td>0.080</td>
      <td>0.471</td>
    </tr>
    <tr>
      <th>theta[7]</th>
      <td>0.140423</td>
      <td>0.262</td>
      <td>0.076</td>
      <td>0.470</td>
    </tr>
    <tr>
      <th>theta[8]</th>
      <td>0.159181</td>
      <td>0.189</td>
      <td>0.000</td>
      <td>0.408</td>
    </tr>
    <tr>
      <th>theta[9]</th>
      <td>0.126710</td>
      <td>0.314</td>
      <td>0.153</td>
      <td>0.476</td>
    </tr>
    <tr>
      <th>theta[10]</th>
      <td>0.133879</td>
      <td>0.322</td>
      <td>0.154</td>
      <td>0.495</td>
    </tr>
    <tr>
      <th>theta[11]</th>
      <td>0.129020</td>
      <td>0.282</td>
      <td>0.131</td>
      <td>0.437</td>
    </tr>
    <tr>
      <th>theta[12]</th>
      <td>0.144806</td>
      <td>0.304</td>
      <td>0.150</td>
      <td>0.470</td>
    </tr>
    <tr>
      <th>theta[13]</th>
      <td>0.032578</td>
      <td>0.223</td>
      <td>0.000</td>
      <td>0.476</td>
    </tr>
    <tr>
      <th>theta[14]</th>
      <td>0.117005</td>
      <td>0.210</td>
      <td>0.021</td>
      <td>0.414</td>
    </tr>
    <tr>
      <th>theta[15]</th>
      <td>0.133092</td>
      <td>0.236</td>
      <td>0.028</td>
      <td>0.458</td>
    </tr>
    <tr>
      <th>theta[16]</th>
      <td>0.108155</td>
      <td>0.133</td>
      <td>0.000</td>
      <td>0.318</td>
    </tr>
    <tr>
      <th>theta[17]</th>
      <td>0.065746</td>
      <td>0.207</td>
      <td>0.001</td>
      <td>0.430</td>
    </tr>
    <tr>
      <th>theta[18]</th>
      <td>0.105766</td>
      <td>0.222</td>
      <td>0.043</td>
      <td>0.415</td>
    </tr>
    <tr>
      <th>theta[19]</th>
      <td>0.124622</td>
      <td>0.230</td>
      <td>0.046</td>
      <td>0.428</td>
    </tr>
    <tr>
      <th>theta[20]</th>
      <td>0.121615</td>
      <td>0.189</td>
      <td>0.037</td>
      <td>0.353</td>
    </tr>
    <tr>
      <th>theta[21]</th>
      <td>0.120505</td>
      <td>0.215</td>
      <td>0.045</td>
      <td>0.408</td>
    </tr>
    <tr>
      <th>rho</th>
      <td>0.183874</td>
      <td>0.211</td>
      <td>0.087</td>
      <td>0.332</td>
    </tr>
    <tr>
      <th>mu[0]</th>
      <td>0.119764</td>
      <td>0.230</td>
      <td>0.053</td>
      <td>0.419</td>
    </tr>
    <tr>
      <th>mu[1]</th>
      <td>0.133596</td>
      <td>0.241</td>
      <td>0.080</td>
      <td>0.418</td>
    </tr>
    <tr>
      <th>mu[2]</th>
      <td>0.140694</td>
      <td>0.202</td>
      <td>0.000</td>
      <td>0.447</td>
    </tr>
    <tr>
      <th>mu[3]</th>
      <td>0.136886</td>
      <td>0.307</td>
      <td>0.164</td>
      <td>0.455</td>
    </tr>
    <tr>
      <th>mu[4]</th>
      <td>0.035124</td>
      <td>0.234</td>
      <td>0.000</td>
      <td>0.504</td>
    </tr>
    <tr>
      <th>mu[5]</th>
      <td>0.137612</td>
      <td>0.228</td>
      <td>0.027</td>
      <td>0.444</td>
    </tr>
    <tr>
      <th>mu[6]</th>
      <td>0.101337</td>
      <td>0.145</td>
      <td>0.000</td>
      <td>0.351</td>
    </tr>
    <tr>
      <th>mu[7]</th>
      <td>0.075024</td>
      <td>0.219</td>
      <td>0.000</td>
      <td>0.460</td>
    </tr>
    <tr>
      <th>mu[8]</th>
      <td>0.118877</td>
      <td>0.214</td>
      <td>0.051</td>
      <td>0.391</td>
    </tr>
    <tr>
      <th>sigma2[0]</th>
      <td>0.101624</td>
      <td>0.131</td>
      <td>0.056</td>
      <td>0.220</td>
    </tr>
    <tr>
      <th>sigma2[1]</th>
      <td>0.097299</td>
      <td>0.150</td>
      <td>0.061</td>
      <td>0.260</td>
    </tr>
    <tr>
      <th>sigma2[2]</th>
      <td>0.094004</td>
      <td>0.118</td>
      <td>0.053</td>
      <td>0.193</td>
    </tr>
    <tr>
      <th>sigma2[3]</th>
      <td>0.103104</td>
      <td>0.135</td>
      <td>0.059</td>
      <td>0.226</td>
    </tr>
    <tr>
      <th>sigma2[4]</th>
      <td>0.105677</td>
      <td>0.117</td>
      <td>0.054</td>
      <td>0.196</td>
    </tr>
    <tr>
      <th>sigma2[5]</th>
      <td>0.091571</td>
      <td>0.125</td>
      <td>0.054</td>
      <td>0.211</td>
    </tr>
    <tr>
      <th>sigma2[6]</th>
      <td>0.107485</td>
      <td>0.118</td>
      <td>0.056</td>
      <td>0.200</td>
    </tr>
    <tr>
      <th>sigma2[7]</th>
      <td>0.106212</td>
      <td>0.118</td>
      <td>0.055</td>
      <td>0.198</td>
    </tr>
    <tr>
      <th>sigma2[8]</th>
      <td>0.105388</td>
      <td>0.138</td>
      <td>0.058</td>
      <td>0.232</td>
    </tr>
    <tr>
      <th>iota[0]</th>
      <td>-0.980943</td>
      <td>-0.954</td>
      <td>-2.131</td>
      <td>0.208</td>
    </tr>
    <tr>
      <th>iota[1]</th>
      <td>-1.108789</td>
      <td>-1.256</td>
      <td>-2.343</td>
      <td>-0.197</td>
    </tr>
    <tr>
      <th>iota[2]</th>
      <td>-0.864302</td>
      <td>-1.390</td>
      <td>-2.993</td>
      <td>0.262</td>
    </tr>
    <tr>
      <th>iota[3]</th>
      <td>-1.395580</td>
      <td>-1.571</td>
      <td>-2.392</td>
      <td>-0.812</td>
    </tr>
    <tr>
      <th>iota[4]</th>
      <td>-1.423259</td>
      <td>-1.163</td>
      <td>-2.829</td>
      <td>0.437</td>
    </tr>
    <tr>
      <th>iota[5]</th>
      <td>-0.037854</td>
      <td>-0.620</td>
      <td>-2.014</td>
      <td>0.734</td>
    </tr>
    <tr>
      <th>iota[6]</th>
      <td>-0.919838</td>
      <td>-1.295</td>
      <td>-2.947</td>
      <td>0.376</td>
    </tr>
    <tr>
      <th>iota[7]</th>
      <td>-1.245577</td>
      <td>-1.039</td>
      <td>-2.644</td>
      <td>0.550</td>
    </tr>
    <tr>
      <th>iota[8]</th>
      <td>-0.524771</td>
      <td>-0.505</td>
      <td>-1.628</td>
      <td>0.633</td>
    </tr>
    <tr>
      <th>gamma[0]</th>
      <td>0.563992</td>
      <td>0.461</td>
      <td>0.429</td>
      <td>0.497</td>
    </tr>
    <tr>
      <th>gamma[1]</th>
      <td>0.180336</td>
      <td>0.191</td>
      <td>0.162</td>
      <td>0.219</td>
    </tr>
    <tr>
      <th>lambda[0]</th>
      <td>0.808996</td>
      <td>0.747</td>
      <td>0.712</td>
      <td>0.785</td>
    </tr>
    <tr>
      <th>lambda[1]</th>
      <td>0.979214</td>
      <td>0.997</td>
      <td>0.996</td>
      <td>0.998</td>
    </tr>
  </tbody>
</table>



### Conclusion and future work

This project aimed to understand & model the nature of setting-specific COVID transmission with the purpose of informing and improving related policy interventions. The first-principles model presented in this article allows us to do this in a way that properly captures the data-generating process behind setting-specific transmission, all with considerations of a simple and feasible data collection methodology. Furthermore, the Bayesian nature of our model allows flexibility when incorporating expert knowledge through priors, as exemplified with the calibrated antigen test accuracy parameters, and provides accurate estimates even with few training samples thanks to its generative nature. Finally, from an implementation perspective, our model is built with scalability in mind, as the TensorFlow Probability version makes it feasible for large-scale applications with the aid of distributed computing architecture. 

There is still much left to be done and many possible extensions could be added to make our model more robust and powerful. One possible angle for future work would be extending the model to encapsulate the effect of other policy interventions (such as social distancing regulations, vaccination, etc.) in order to derive insights about the effectiveness of these in different settings. Another possible extension could be to add temporal dynamics into the model by combining with an SIR-type model. 

Overall, we believe this model serves as a great case for statistical modeling of setting-specific epidemic transmission, with great potential for future extensions and applications to similar settings. Additionally, it serves as a great example of the power of Bayesian modelling and the many benefits it can bring in applied settings.
