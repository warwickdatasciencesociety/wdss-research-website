---
title: "Store Sales - Time Series Forecasting Challenge"
date: 2022-02-12
updated: 2022-02-12
authors_plus:
- "Ivan Silajev"
- "Hugo Ng"
- "Amr Abdelmotteleb"
contacts_plus:
- "https://www.linkedin.com/in/ivan-silajev-04957a18b/"
- "https://www.linkedin.com/in/hugo-ryan-ng-312730197/"
- "https://www.linkedin.com/in/amr-abdelmotteleb-3574691ba/"
editor: "Janique Krasnowska"
editor_contact: "https://www.linkedin.com/in/janique-krasnowska/"
tags:
- machine learning
- time series
- clustering
- sales
- python
categories:
- [Economics, Finance]
languages:
- python
description: "We enter a Kaggle competition and use time-series forecasting to predict store sales on data from Corporación Favorita, a large Ecuadorian-based grocery retailer."
cover: /banners/time-series.png
---
## Introduction

This blog post serves as a review and a showcase of the various statistical inference and modelling techniques utilised by the WDSS Machine Learning Competition Team over the Autumn and Winter seasons in 2021.

Throughout the post, each technique is explained in chronological order to accurately portray the thought process of the team tackling the problem.

The purpose of this report is to potentially inspire readers to participate in data science competitions or even take an interest in data science if they have not already.

## Preliminaries

Before explaining the team's problem solving process, the problem itself must be formulated.

### The Competition

The competition we entered was the "Store Sales - Time Series Forecasting" competition on Kaggle. The objective was to create 15 day forecasts for the sales figures of 33 different products for 54 stores belonging to the same retailer.

In summary, we had to make accurate 15 day predictions for 1782 individual time series using data scientific methods.

### The Data

Before proceeding with creating the predictions, it was essential to examine the information, in the form of tabular data sets, given to us and determine the utility of each set.

The training data set contained past sales data, product families and if the products were on promotion. The rest of the datasets contained additional exogenous variables:
- Oil prices 
- The location, type and the daily number of transactions for each store
- Ecuadorian holidays

### The Methodology

As with any data scientific project, we all carried out an EDA (Exploratory Data Analysis) to determine how to use the data for modelling.

The following is brief list of what modelling and inference techniques we used for this competition:
- Metrics for comparing time series;
    - Euclidean distance
    - Dynamic time warping
- Methods of clustering time series;
    - UMAP-assisted K-means clustering
- Time series modelling methods;
    - SARIMAX model
    - State-space model
    - LSTM model

In the following sections, we give a detailed overview of:
- Our EDA and thought process
- The decisions we made regarding how we use the data and their justifications
- The underlying theory and code for our methods

### Aggregate Correlation of Sales

We will investigate whether all sales time series for a given product family are similar enough to be treated identically.

A simple 'measure' for the similarity between two time series is the linear correlation coefficient between the values of both series. Letting $a_i$ be the $i$ th value in the first time series and $b_i$ be the $i$ th value in the second series, plot the coordinates $(a_i, b_i)$ for all $i$. If a linear relationship is clearly visible, then both time series are approximately similar.

Two time series are completely similar if they are both affine tranformations of each other (i.e. it is possible to express time series $a_i$ in terms of $b_i$ as $A + B a_i$, where $A$ and $B$ are real values).

It is costly to compare a large number of time series with each other to produce a correlation matrix, especially when the time series contain more than 1.5 thousand values. A less reliable, but quicker solution is to compare each time series with the sum of all time series (the aggregate time series).

The aggregate time series would be approximately similar to every series that forms the largest similarity group. This way, one can detect the existence of series groupings with a given set of series.


![](/images/sales-forecasting-challenge/sales-forecasting-challenge_7_0.png)


This EDA showed that the degree of similarity between series from the same product family can vary drastically. For example, for the BEAUTY family, it ranged from small negative values to 0.85 with a mean of 0.5. Hence, there is convincing evidence that the time series can't be trivally grouped by the product family they represent.

## Clustering

By grouping similar time series data together, we may be able to reduce the number of models to fit. We focus on grouping stores and product types.

The clustering technique we use is UMAP-assisted k-Means clustering. We focus on two notions of distance: dynamic time warping and Euclidean distance. There is a reliability-speed trade-off among these two distances, as we explain below.

## The notion of distance for clustering

We need to standardize our data, such that comparisons are fair. Naturally, more expensive products may fluctuate more, but the underlying structure may be similar to cheaper products, and we want to be be able to make such comparison.

#### Dynamic time warping
We can choose dynamic time warping (DTW) or Euclidean distance for our clustering. DTW is a reliable algorithm for measuring similarity between two temporal sequences. It is able to match peaks to peaks, troughs to troughs, and account for any stretching, shrinking, and shifting/phase difference. This is helpful, since two 'close' time series can exhibit slight differences as described. 

A drawback of dynamic time warping is that it is computationally intensive by design. If we use it for clustering on a large dataset, which we have, we are doing a lot of expensive computations. This limits the usefulness of DTW, which could be remedied for example with cloud computing. 

#### Euclidean distance
Euclidean distance is fast, as naive comparison of two time series vertically is a simple computation. When two time series only differ in magnitude but match in phase, Euclidean distance is good enough.

However, Euclidean distance is not as reliable as DTW. Imagine two time series that look like sin curves, but one is shifted out of phase. Intuitively, these time series are very similar, and should be grouped together. A vertical point-to-point comparison by Euclidean distance gives us a large distance. As a result, distances between two time series may be erroneously larger than it actually is.

Due to computational constraints, we will be proceeding with euclidean distance.

# UMAP
We choose the smallest number of clusters that capture at least 97% of the distortions. In this case, 5 clusters.


```python
umap_3d = UMAP(n_components=3, n_neighbors=15, metric='euclidean' , init='random', random_state=0)

proj_3d = umap_3d.fit_transform(df.to_numpy())

kmeans = KMeans(n_clusters=5, init='k-means++', random_state=0)
clusters = kmeans.fit_predict(proj_3d)

fig_3d = px.scatter_3d(
    proj_3d, x=0, y=1, z=2,
    color=clusters.astype('str'),
    labels={'color': 'Cluster'}, 
)
fig_3d.update_traces(marker_size=5)
fig_3d.update_layout(scene = dict(
                    xaxis_title='Component 1',
                    yaxis_title='Component 2',
                    zaxis_title='Component 3'))                   
```

<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plotly.com/~Kaasiak/1.embed" height="525" width="100%"></iframe>

## Cluster Analysis

### Heatmaps
By looking at clustermaps, we can see how similarly each cluster behaves.

We analysed clusters from a number of perspectives: the percentage of cluster members belonging to each family, state, city and store number. We concluded that it is only the product's family accounts for a reasonable amount of difference and that is not the case for other characteristics. However, aggregate correlation showed that even the similarities within product families are limited. Therefore, we will be proceeding with fitting separate models for each family in each stores.


![](/images/sales-forecasting-challenge/sales-forecasting-challenge_18_0.png)


# ARIMA

In this section, we go through fitting an ARIMA model on a time series for one of the families of products in one store; to see how well it performs. 

We are now going to create a dataset for the sales of <b> Bread/Bakery </b> in <b> store 44 </b>.

One very important assumption of an ARIMA model is for the data to be stationary. We will test this with a hypothesis test called ADF (Augmented Dickey-Fuller).

<b> NOTE: </b> The null hypothesis of the ADF test is that the time series is non-stationary. 

We have a p value of 0.214832, So we do not reject the null hypothesis and so the series is non-stationary. In order to still be able to use ARIMA, we are going to difference our data.

Let us now plot the original timeseries, as well as the 1st and 2nd order differenced time series with their ACF (Autocorrelation) plots to determine the order of differencing we are going to use in our model:


![](/images/sales-forecasting-challenge/sales-forecasting-challenge_22_0.png)


The p-value for the first order differenced data is close to 0, so we can proceed with using this transformation. We now move on to identifying the number of AR terms (p) and the number of MA terms (q) that we are going to include in our ARIMA model. We do this by inspecting the ACF and PACF plots for the data.

We use q = 2 based on the autocorrelation plot and p = 6 based on the partial autocorrelation plot to fit the ARIMA model. The residuals seem to exhibit no significant patterns. We can now predict the sales for the 16 last observations from the original dataset that we kept as a test set. The predictions seem to align well with the actual data.


![](/images/sales-forecasting-challenge/sales-forecasting-challenge_24_0.png)


## SARIMA

Seasonality definitely plays a role in the time series of some of the families of products in some of the stores, so using a seasonal ARIMA (SARIMA) could be a further improvement.

We fit a SARIMA model to explore any weekly trends and we automated the process of selecting the model's parameters. However, using a grid search for selecting the best SARIMA parameters based on root-mean-square error is computationally expensive. Applying it to thousands of families of products would take a significant amount of time. Hence, we decided to explore other models with fewer parameters to specify.

## Dynamic Linear Models

State space models are a generalisation of general linear regression models. Unlike GLMs, which include ARIMA models, SSMs can consider cases where the underlying distribution of the parameters of the model changes over time. A dynamic linear model is an SSM that assumes the data can be modelled as a linear combination of its parameters.

### DLM Theory

A standard DLM can be formulated by the following four equations, given we already have data up until time $t-1$:

<center>

$x_t = \phi_t \cdot b_t + \epsilon_t : \epsilon_t \sim N(0, v_t)$

$b_t = F_t \cdot b_{t-1} + \Delta_t : \Delta_t \sim N(0, v_{t-1} \Sigma_t)$

$b_{t-1} = m_{t-1} + B_{t-1} : B_{t-1} \sim N(0, v_{t-1} B_{t-1})$

$v_t = \delta v_{t-1}$
    
</center>

The first equation is an ordinary linearity assumption for the data, the same one for ordinary linear regression, except the parameters can vary over time.

The second equation is the hidden model and is the key assumption for a linear model to be dynamic.

The third equation is a reiteration of the fact that the model parameters are random as well. The parameters possess an initial prior distribution which updates as more data is collected.

The fourth equation models the change in variance as time progresses.

Each term at time $t$ is defined as follows:
- $x_t$ is the data
- $b_t$ is the parameter vector
- $\epsilon_t$ is a normally distributed variable with variance $v_t$

- $m_t$ is the expectation of the parameters
- Both $B_{t}$ and $\Delta_t$ are multivariate normally distributed vectors with covariance matricies $v_t B_t$ and $v_{t-1} \Sigma_t$ respectively

- $\phi_t$ and $F_t$ are the transition vector and matrix respectively, which define how the model parameters combine linearly
- $\delta$ is the discount factor, a value in the interval of zero to one that models the increasing uncertainty in the distribution of future data

The model reduces to ordinary linear regression if:
- $F_t$ is the identity matrix for all $t$
- $\Sigma_t$ is the zero matrix for all $t$
- $\delta$ is one, so there is no increasing uncertainty in the distribution of future data

The dynamic linear model offers a high degree of modelling flexibility, as well as offering a convenient method for updating the model parameters over time.


![](/images/sales-forecasting-challenge/sales-forecasting-challenge_29_0.png)


## LSTM

Long short-term memory (LSTM) is a recurrent neural network (RNN) that utilises two different hidden variables rather than one to learn about the behaviour of a sequential process. In theory, LSTMs could capture deeper non-linear underlying patterns in the data.

### LSTM Theory

While a simple RNN uses its hidden variable as a short term memory channel, LSTM uses a second one for long term memory, which, theoretically, preserves significant patterns of the system's behaviour in the model for as long as they persist.

A standard LSTM can be formulated by the following equations, given we already have data up until time $t-1$:

<center>

$f_t = \sigma (W_f \cdot [h_{t-1}, x_t] + b_f)$

$i_t = \sigma (W_i \cdot [h_{t-1}, x_t] + b_i)$

$\bar{C}_t = \text{tanh} (W_C \cdot [h_{t-1}, x_t] + b_C)$

$C_t = f_t \times C_{t-1} + i_t \times \bar{C}_t$

$o_t = \sigma (W_o \cdot [h_{t-1}, x_t] + b_o)$

$h_t = o_t \times \text{tanh}(C_t)$
    
</center>

The first equation represents the forget gate, the perceptron layer responsible for removing any insignificant patterns the long term memory assumed from the last iteration.

The second equation represents the information gate, the layer accountable for recording new potential patterns into the long term memory and strengthen ones that were present before.

The third equation offers a candidate long term memory term, which is corrected by the information gate, as visible in the fourth equation.

The fifth equation is the output gate, the layer for creating the final output that will be used for creating the next short term hidden variable, as shown in the sixth equation.

The $\times$ symbol represents termwise multiplication.

Each term at time $t$ is defined as follows:
- $x_t$ is the data
- $h_t$ is the hidden short term memory variable
- $C_t$ is the hidden long term memory variable
- $\bar{C}_t$ is a candidate for $C_t$
- $f_t$ is the forget vector
- $i_t$ is the information vector
- $o_i$ is the output vector

- All $W$ matricies are the weights that dictate how much of each term in the input contributes to the value of the output
- All $b$ vectors are biases that set the default values of the variables they form

- $\sigma$ is the element-wise sigmoid activator function
- $\text{tanh}$ is the element_wise hyperbolic tangent activator function

LSTM allows for modelling arbitrary patterns in time series or any sequential process becuase of its neural-like nature.

### Application

We define an LSTM model with 50 units, outputting a hidden variable of length 50. A dense perceptron layer with a rectified linear unit activation function combines the outputs at the end to create a single prediction.

The model uses an Adam optimiser and a mean square loss function.

### Evaluation

The LSTM model produced very monotonuous predictions and thus struggled with predicting the variability present in the data. The quality of predictions remained low even after varying different parameters of the network. Even though LSTMs take longer to learn and their setup is more complex, this model couldn't recreate the success that ARIMA and DLM models offer in terms of time series prediction.
