---
title: "Predicting aqueous solubility with neural networks"
date: 2021-10-19
updated: 2021-10-19
authors_plus:
- "Aleksander Dukaczewski"
- "Annie Stevenson"
- "Escher Luton"
contacts_plus:
- "https://www.linkedin.com/in/aleksander-dukaczewski-2713911b8/"
- "https://www.linkedin.com/in/anniestevenson1/"
editor: "Keeley Ruane"
editor_contact: "https://www.linkedin.com/in/keeley-ruane-6aab4219b/"
tags:
- machine learning
- molecular machine learning
- chemistry
- solubility
- esol
- python
categories:
- [Natural Sciences, Chemistry]
languages:
- python
description: "Predicting aqueous of chemical compounds without the presence of a physical sample would make the process of drug discovery easier. Can machine learning help us achieve this?"
cover: /banners/chemistry-lab.png
---
## Introduction

Aqueous solubility is a key physical property of interest in the medicinal and agrochemical industry. Low aqueous solubility of compounds can be a major problem in drug development, as <a href="https://biomedpharmajournal.org/vol13no2/the-importance-of-solubility-for-new-drug-molecules/">more than 40% of newly developed chemicals are practically insoluble in water.</a> For a drug to be absorbed it needs to be contained in a solution at the site of the absorption and solubility is the main parameter that influences the bioavailability of a molecule. Many drug manufacturers are inclined more to produce oral drug products due to their ease of administration, lack of sterility constraints and high patient compliance, which causes them to prioritise bioavailability and therefore aqueous solubility.

As designing and approving a new drug is an expensive, nearly decade-long process, new methods for the prediction of a compound's aqueous solubility prior to its synthesis could greatly facilitate the process of drug development. Aqueous solubility is also a major factor in the development of insecticides, fungicides and herbicides as highly soluble substances <a href="https://edis.ifas.ufl.edu/publication/PI202">are more likely to move through the soil in water than less-soluble substances</a>, therefore they are able to reach the plants and take effect more easily. This suggests that the agrochemical industry can also greatly benefit from new methods of estimating aqueous solubility of compounds without the presence of a physical sample. 

Machine learning is a branch of computer science that focuses on the use of algorithms and data to imitate the way that humans learn. It allows us to create models that can predict a compound's aqueous solubility straight from its molecular structure without the presence of a physical sample. Not having to run sophisticated and computationally expensive physical simulations can greatly reduce the amount of time and funds spent in the process of drug discovery.

Machine learning algorithms can be grouped into regressive algorithms used to predict a continious value (age, salary, etc.) and classification algorithms used to predict discrete values (male, female, etc.). Predicting a compound's aqueous solubility is a regression problem rather than a classification one and the model can be taught to predict a value based on a set of inputs in a process called supervised learning.

## Methods

The entire project was completed using Python. We used the dataset ESOL, containing the solubilities of 1144 chemical compounds and their structures in the SMILES format. SMILES is a commonly used notation used for describing the structure of chemical compounds with short ASCII strings. The compounds contained in the dataset are mostly pesticide products, low molecular weight organic compounds, and heavy compounds.

The library `rdkit` was used to extract features from the dataset. It provides methods to calculate:
- $logP$ - partition coefficient; measure of differential solubility in a hydrophobic and hydrophilic solvent
- Molecular weight ($MWT$)
- Number of rotatable bonds ($RB$)
- Number of H-bond donors ($HBD$)
- Number of H-bond acceptors ($HBA$)
- Polar surface area - the amount of molecular surface arising from polar atoms ($TPSA$)
- Aromatic proportion - number of atoms in an aromatic ring divided by the number of heavy atoms in the molecule ($AP$)
- Non-carbon proportion - number of non-carbon atoms divided by the number of heavy atoms in the molecule ($NCP$)

## Linear Regression

In order to observe which features have the most predictive power it was decided to train a linear regression model from the library `sklearn` to predict *log(solubility)*. Multiple linear regression is a statistical technique that uses several explanatory variables to predict the outcome of a response variable. The goal of multiple linear regression is to model the **linear** relationship between the explanatory (independent) variables and response (dependent) variables. Data was split into training and testing datasets with 80% of the data used for training the model. Metrics we used to quantify how well a model fits the dataset were *RMSE* and *R-Squared*. 
{% note info %}
- $RMSE = \sqrt{\frac{\Sigma_{i=1}^{N}{\left(y_i - \hat{y}_i\right)^2}}{N}}$. RMSE is the square root of the average of squared residuals / errors. When used on the holdout dataset, RMSE serves to aggregate the magnitudes of the errors in predictions for various data points into a single measure of predictive power. It tells us how far apart predicted values are from those in a dataset (on average). The lower the value, the better the data fits the model. 
- $R^2 = 1 - \frac{\text{RSS}}{\text{TSS}}$, where RSS = sum of squares of residuals, TSS = total sum of squares of the values in the dataset (proportional to the variance of the data). It tells us about the proportion of the variation in the dependent variable that is predictable from the independent variables. $R^2$ takes the values between 0 and 1. An $R^2$ of 1 indicates that the regression predictions perfectly fit the data.
{% endnote %}
After training, this linear regression model resulted in training $RMSE$ and $R^2$ values of approximately $0.964$ and $78.8$%, and testing $RMSE$ and $R^2$ values of approximately $0.993$ and $77.9$%. The predictive power of this simple linear model inspired us to create a more sophisticated neural network model for the same purpose.

The final equation given by the trained model is 
$$LogS = 0.12 -0.78logP -0.0065 MWT + 0.0158 RB -0.05 HBD + 0.20 HBA  -0.02 TPSA  -0.25 AP + 1.16 NCP$$
The coefficients of the linear model can help us identify which features might have the most predictive power. From the above equation we deduce that these are non-carbon proportion and aromatic proportion.

![linear_results](/images/chemical-properties/plot_horizontal_logS.png)

These two-dimmensional plots represent how the equation fits the data points from the training and testing datasets respectively. The line is a graph of the equation and the dots represent entries from the datasets.
{% note warning %}
The linear regression model is only able to capture linear relationships between the independent variables and the target variable. If the relationship between the variables is non-linear, features should be additionally transformed, for example by taking the logarithm of the predictor variables or introducing higher order polynomial terms.
{% endnote %}
## Neural Network

Artificial neural networks are machine learning models designed to loosely model neural networks present in animal brains. They are collections of nodes called artificial neurons, which are models that imitate neurons in real brains. In contrast to linear regression, neural networks can model more complex, non-linear relationships between predictive variables and the response variable without assuming that a fixed equation can fit the model.

A neural network model was created using `keras` and `tensorflow`. To build a neural network we first need to investigate the following features: vectors, layers and linear regression. Our data source has been stored in vectors and with the help of python can be converted into multidimensional arrays. These arrays are then used to calculate the dot product, which tells us how similar the data is in terms of direction. Weights and bias vectors are the main type of vectors present inside a neural network; these are used to predict outputs by comparing input data to previously seen inputs. Layers have been added to the neural network to extract representations found in the previous data, hidden layers are also present to take a set of weighted inputs and produce an output through an activation function. Linear regression can be thought of as a neural network consisting of just one layer, as every input is connected to every output. This layer can be seen as fully connected and can be used within the neural network.


```python
from keras.models import Sequential
from keras.layers import Dense
ann = Sequential()
ann.add(Dense(60, input_dim=8, activation='tanh'))
ann.add(Dense(40, input_dim=60, activation='tanh'))
ann.add(Dense(20, input_dim=40, activation='tanh'))
ann.add(Dense(7, input_dim=20, activation='tanh'))
ann.add(Dense(1, input_dim=7, activation='linear'))

tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.99)
ann.compile(loss='mean_squared_error', optimizer='adam', metrics='mse')
ann.summary

#Fitting/ tuning the model 
ann.fit(X_train, Y_train, epochs=100, batch_size=32, validation_split=0.10, verbose=True)

#Applying the model to the training data set 
ann_Y_train_pred = ann.predict(X_train)

```

The artificial neural network was evaluated like the linear regression model and achieved better metric scores, with training $RMSE$ and $R^2$ values of approximately $0.721$ and $88.1$%, and testing $RMSE$ and $R^2$ values of approximately $0.722$ and $88.1$%.
</br>

## Results

The neural network model resulted in lower values of root-mean-square error ($RMSE$) than the linear regression model, meaning that the values predicted by the linear regression model were farther apart. The neural network model also got higher values of the coefficient of determination ($R^2$), which also means that the model fits the dataset better. The models can be compared using this graph, showing the distribution of measured molecule solubility and predicted molecule solubility of both models.

![comparison](/images/chemical-properties/models_comparison.png)

As our problem is classed as regression, we needed to replace the categorical variables within the neural network to numeric dependent variables. Otherwise, the model would try categorise outputs. There are several limitations to using neural networks on regression problems which are mainly related to the data source properties and their optimalisation, these include:
- Dataset size – how many training examples are present 
- Data dimension
- Data structure -  structured/ unstructured

To stabilise the model, a large dataset is required. Our dataset is well structure however, it is relatively small with only a 1000 plus records. Combining our dataset with other solubility data would increase the number of inputs and therefore improve the models ability to predict. As a further develop we could also investigate different validation methods such as cross validation, as our method reduced the size of the training dataset as holdout validation was used. Our models results proved more useful than those of the linear regression model; yet, improvements could still be made for better performance and other machine learning models should be investigated. This includes researching gradient boosted decision trees, which are said to work well in similar regression problems. 

## Conclusions
Molecular machine learning methods for the prediction of chemical properties can have far-reaching benefits for industries relating to chemistry. They could greatly reduce the cost and time used in the process of drug development. Methods similar to ours can also be used to predict other chemical properties like lipophilicity or solvation free energy. 
While the accuracy of these methods may not always be perfect, they can still prove to be useful by giving researchers suggestions about whether the compounds they're researching fit their criteria. Until sophisticated and reliable molecular learning methods are widely recognised we can't greatly depend on them in research, however they can still serve as advisory tools. Conducting synthesis and running sophisticated tests isn't always the most viable option, therefore these methods can prove to be useful where time and budget is limited.
