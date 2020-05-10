---
title: "What Factors Actually Affect Your Grades?"
date: 2020-04-19
updated: 2020-04-19
author: "Brandusa Draghici"
contact: "https://www.linkedin.com/in/brandusa-draghici-5b0a84147/"
tags:
- visualization
- data-analysis
- regression
categories:
- [Social Sciences, Education]
languages:
- python
description: "If only there was some way to know how well you'd do in your exams. Well, perhaps data science can get us part way there. Read on to find out how."
cover: /banners/school-success.jpg
---
{% note info %}
**Accessing Post Source**
We are still working on getting this site set up, so source code for this post is not yet available. Check back soon and you'll be able to find it linked here.
{% endnote %}
With exam period approaching fast, every student is wondering how to score the best possible grade. Some factors—like how much sleep you're getting or how healthy you are—seem to have an obvious correlation with your final grade. What about your relationship status? How much should you be studying to achieve the grade you want? Does the subject you're studying influence your final grade? In this article, we will use two datasets containing student math and Portuguese language performance in two different Portuguese schools and see which factors affected student performance the most. 

## Exploratory Data Analysis

### Dataset Overview

The variables are the same for the two datasets:

|  Variable  |           Description           |   Type  |                          Possible Values                          |
|:----------:|:-------------------------------:|:-------:|:-----------------------------------------------------------------:|
|   school   |              School             |  binary |            GP—Gabriel Pereira; MS—Mousinho da Silveira            |
|     sex    |               Sex               |  binary |                          F—female; M—male                         |
|     age    |               Age               | numeric |                          15–22, inclusive                         |
|   address  |           Address type          |  binary |                          U—Urban; R—Rural                         |
|   famsize  |           Family Size           |  binary |          LE3—less than or equal to 3; GE3—greater than 3          |
|   Pstatus  |   Parent's cohabitation status  |  binary |                 T—living together; A—living apart                 |
|    Medu    |        Mother's Education       | ordinal | 0—none; 1—up to 4th grade; 2—5th–9th grade; 3—secondary; 4—higher |
|    Fedu    |        Father's Education       | ordinal | 0—none; 1—up to 4th grade; 2—5th–9th grade; 3—secondary; 4—higher |
|    Mjob    |           Mother's Job          | nominal |  teacher; health(-care related); (civil )services; at home; other |
|    Fjob    |           Father's Job          | nominal |  teacher; health(-care related); (civil )services; at home; other |
|   reason   |    Reason for choosing school   | nominal |  (close to )home; (school )reputation; course(preference); other  |
|  guardian  |        Student's guardian       | nominal |                       mother; father; other                       |
| traveltime |      Travel time to school      | ordinal |       1—<15 min.; 2—15–30 min.; 3—30 min.–1 hour; 4—>1 hour       |
|  studytime |        Weekly study time        | ordinal |         1—<2 hours; 2—2–5 hours; 3—5–10 hours; 4—>10 hours        |
|  failures  |       Past class failures       | numeric |                            0–3, else 4                            |
|  schoolsup |    Extra educational support    |  binary |                              yes; no                              |
|   famsup   |    Family educational support   |  binary |                              yes; no                              |
|    paid    |        Extra paid classes       |  binary |                              yes; no                              |
| activities |   Extra-curricular activities   |  binary |                              yes; no                              |
|   nursery  |          Attend nursery         |  binary |                              yes; no                              |
|   higher   |  Wants to take higher education |  binary |                              yes; no                              |
|  internet  |       Home internet access      |  binary |                              yes; no                              |
|  romantic  |    In a romantic relationship   |  binary |                              yes; no                              |
|   famrel   | Quality of family relationships | ordinal |                     1—very bad to 5—very good                     |
|  freetime  |      Free time after school     | ordinal |                     1—very low to 5—very high                     |
|    goout   |      Going out with friends     | ordinal |                     1—very low to 5—very high                     |
|    Dalc    |   Workday alcohol consumption   | ordinal |                     1—very low to 5—very high                     |
|    Walc    |   Weekend alcohol consumption   | ordinal |                     1—very low to 5—very high                     |
|   health   |      Current health status      | ordinal |                     1—very bad to 5—very good                     |
|  absences  |         Number absences         | numeric |                                0–93                               |
|     G1     |        First Period Grade       | numeric |                                0–20                               |
|     G2     |       Second Period Grade       | numeric |                                0–20                               |
|     G3     |           Final Grade           | numeric |                                0–20                               |

I will be conducting a basic analysis of the dataset followed by visualizations of the correlations between different factors. Finally, I will build a linear regression model for each subject to predict the students' final grades. 

We will start by importing all the necessary packages and load the datasets into a pandas dataframe.


```python
# Import necessary packages
import pandas as pd  
import numpy as np  

import statistics as stats
import statsmodels.api as sm

# Load the dataset from the csv file using pandas
data_m = pd.read_csv(r'data\student-mat.csv', sep=';')
data_p = pd.read_csv(r'data\student-por.csv', sep=';')
```

We can start by taking a look at the first few rows of each dataset.

    First 5 lines of the math performance dataset:
    



<table>
  <thead>
    <tr>
      <th></th>
      <th>school</th>
      <th>sex</th>
      <th>age</th>
      <th>address</th>
      <th>famsize</th>
      <th>Pstatus</th>
      <th>Medu</th>
      <th>Fedu</th>
      <th>Mjob</th>
      <th>Fjob</th>
      <th>reason</th>
      <th>guardian</th>
      <th>traveltime</th>
      <th>studytime</th>
      <th>failures</th>
      <th>schoolsup</th>
      <th>famsup</th>
      <th>paid</th>
      <th>activities</th>
      <th>nursery</th>
      <th>higher</th>
      <th>internet</th>
      <th>romantic</th>
      <th>famrel</th>
      <th>freetime</th>
      <th>goout</th>
      <th>Dalc</th>
      <th>Walc</th>
      <th>health</th>
      <th>absences</th>
      <th>G1</th>
      <th>G2</th>
      <th>G3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GP</td>
      <td>F</td>
      <td>18</td>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>4</td>
      <td>4</td>
      <td>at_home</td>
      <td>teacher</td>
      <td>course</td>
      <td>mother</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>4</td>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>6</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GP</td>
      <td>F</td>
      <td>17</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>1</td>
      <td>1</td>
      <td>at_home</td>
      <td>other</td>
      <td>course</td>
      <td>father</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>no</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>5</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>5</td>
      <td>5</td>
      <td>6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>GP</td>
      <td>F</td>
      <td>15</td>
      <td>U</td>
      <td>LE3</td>
      <td>T</td>
      <td>1</td>
      <td>1</td>
      <td>at_home</td>
      <td>other</td>
      <td>other</td>
      <td>mother</td>
      <td>1</td>
      <td>2</td>
      <td>3</td>
      <td>yes</td>
      <td>no</td>
      <td>yes</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>3</td>
      <td>3</td>
      <td>10</td>
      <td>7</td>
      <td>8</td>
      <td>10</td>
    </tr>
    <tr>
      <th>3</th>
      <td>GP</td>
      <td>F</td>
      <td>15</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>4</td>
      <td>2</td>
      <td>health</td>
      <td>services</td>
      <td>home</td>
      <td>mother</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
      <td>2</td>
      <td>15</td>
      <td>14</td>
      <td>15</td>
    </tr>
    <tr>
      <th>4</th>
      <td>GP</td>
      <td>F</td>
      <td>16</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>3</td>
      <td>3</td>
      <td>other</td>
      <td>other</td>
      <td>home</td>
      <td>father</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>2</td>
      <td>5</td>
      <td>4</td>
      <td>6</td>
      <td>10</td>
      <td>10</td>
    </tr>
  </tbody>
</table>


    First 5 lines of the Portuguese performance dataset:
    



<table>
  <thead>
    <tr>
      <th></th>
      <th>school</th>
      <th>sex</th>
      <th>age</th>
      <th>address</th>
      <th>famsize</th>
      <th>Pstatus</th>
      <th>Medu</th>
      <th>Fedu</th>
      <th>Mjob</th>
      <th>Fjob</th>
      <th>reason</th>
      <th>guardian</th>
      <th>traveltime</th>
      <th>studytime</th>
      <th>failures</th>
      <th>schoolsup</th>
      <th>famsup</th>
      <th>paid</th>
      <th>activities</th>
      <th>nursery</th>
      <th>higher</th>
      <th>internet</th>
      <th>romantic</th>
      <th>famrel</th>
      <th>freetime</th>
      <th>goout</th>
      <th>Dalc</th>
      <th>Walc</th>
      <th>health</th>
      <th>absences</th>
      <th>G1</th>
      <th>G2</th>
      <th>G3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GP</td>
      <td>F</td>
      <td>18</td>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>4</td>
      <td>4</td>
      <td>at_home</td>
      <td>teacher</td>
      <td>course</td>
      <td>mother</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>4</td>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>0</td>
      <td>11</td>
      <td>11</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GP</td>
      <td>F</td>
      <td>17</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>1</td>
      <td>1</td>
      <td>at_home</td>
      <td>other</td>
      <td>course</td>
      <td>father</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>no</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>5</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>2</td>
      <td>9</td>
      <td>11</td>
      <td>11</td>
    </tr>
    <tr>
      <th>2</th>
      <td>GP</td>
      <td>F</td>
      <td>15</td>
      <td>U</td>
      <td>LE3</td>
      <td>T</td>
      <td>1</td>
      <td>1</td>
      <td>at_home</td>
      <td>other</td>
      <td>other</td>
      <td>mother</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>3</td>
      <td>3</td>
      <td>6</td>
      <td>12</td>
      <td>13</td>
      <td>12</td>
    </tr>
    <tr>
      <th>3</th>
      <td>GP</td>
      <td>F</td>
      <td>15</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>4</td>
      <td>2</td>
      <td>health</td>
      <td>services</td>
      <td>home</td>
      <td>mother</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>no</td>
      <td>yes</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>yes</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>5</td>
      <td>0</td>
      <td>14</td>
      <td>14</td>
      <td>14</td>
    </tr>
    <tr>
      <th>4</th>
      <td>GP</td>
      <td>F</td>
      <td>16</td>
      <td>U</td>
      <td>GT3</td>
      <td>T</td>
      <td>3</td>
      <td>3</td>
      <td>other</td>
      <td>other</td>
      <td>home</td>
      <td>father</td>
      <td>1</td>
      <td>2</td>
      <td>0</td>
      <td>no</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>yes</td>
      <td>yes</td>
      <td>no</td>
      <td>no</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>2</td>
      <td>5</td>
      <td>0</td>
      <td>11</td>
      <td>13</td>
      <td>13</td>
    </tr>
  </tbody>
</table>


An important detail to note is that there are 395 high school students in the math dataset and 649 in the Portuguese dataset. The grades of the student are from 0 to 20. Furthermore, there are 16 numerical variables out of 33; the rest of the variables will need to be one-hot encoded when we will analyze correlations and build the regression model. 

Now let's visualize the final grades distributions for both subjects.


![](/images/school-success/school-success_13_0.png)





We can also calculate that the average final grades for math and Portuguese students are 10.42 and 11.91, respectively. This suggests that Portuguese students score higher on average than math students although this comparison could easily have been skewed by the large number of math students scoring zero.



### Finding and Visualizing Correlations for Numerical Variables

We are now going to automatically find the variables with the strongest correlation to the final grades for both datasets. Finding correlations between non-numeric features and the outcome can get a bit messy, so we will focus on testing only the existing numerical values of the datasets at first. To better visualize the insights, we will also use correlation bar plots and heat maps for both datasets.


![](/images/school-success/school-success_17_0.png)


To interpret correlation bar plots and heat map:
- The darker the bar/square, the stronger the correlation is. 
- Brown represents negative correlations, whereas purple represents positive correlations. 


![](/images/school-success/school-success_19_0.png)


Insights:
- For both datasets, the number of past classes `failures` has a strong negative correlation with `G3`.
- Other common variables with a negative correlation are `age`, frequency of going out with friends (`goout`), `traveltime`, `freetime` and `health`. 
- `G1` and `G2` have very strong positive correlation coefficients for both datasets because student performance usually remains constant throughout the year; we will therefore ignore them. 
- Other common variables with a positive correlation are: `studytime`, education of parents (`Fedu` and `Medu`) and family relationship (`famrel`).

### One-Hot Encoding

In order to get more insight from these datasets, we need to be able to use the categorical variables as well. An example of categorical variable is the `school` variable (the student is either at Gabriel Pereira or Mousinho da Silveira) as there are multiple possible values with no intrinsic ordering. We will use a technique called one-hot encoding, which assigns binary value to each category level indicating whether or not that level was the value of the original predictor. Here is an example of how it would look like for the variable father's job (`Fjob`).

| Father's Job    | Occupation_teacher| Occupation_health | Occupation_services |Occupation_at_home |Occupation_other |
| ----------------|:----------------: |:-----------------:|:------------------: |:----------------: |:---------------: |
| teacher         | 1                 | 0                 | 0                   |0                  |0                 |
| health          | 0                 | 1                 | 0                   |0                  |0                 |
| services        | 0                 | 0                 | 1                   |0                  |0                 |
| at_home         | 0                 | 0                 | 0                   |1                  |0                 |
| other           | 0                 | 0                 | 0                   |0                  |1                 |

{% note warning %}
**Technical Detail**
One-hot encoding is actually slightly more subtle than the description given above. The missing detail is that we often drop the first of the resulting binary columns. The reason we do this is that knowing the value of the other columns is enough to be certain of the value of the first. Indeed, if all of the other columns are zero, then the first column must be one, and vice-versa. Removing the first column is important as the algebra behind linear regression fails we duplicate predictor information.
{% endnote %}

```python
def one_hot_encode(df):
    # Select only categorical variables
    cat_df = df.select_dtypes(include=['object'])
    
    # One-hot encode variables
    dummy_df = pd.get_dummies(cat_df, drop_first=True)
    
    # Add the response back and return
    dummy_df['G3'] = df['G3']
    return dummy_df

# One-hot encode both datasets
dummy_dfm = one_hot_encode(data_m)
dummy_dfp = one_hot_encode(data_p)
```

### Finding and Visualizing Correlations for Encoded Categorical Variables

We can now analyze the correlation coefficients for the final grades of all the variables for both datasets.


![](/images/school-success/school-success_28_0.png)



![](/images/school-success/school-success_29_0.png)


Insights:
- Variables that impact negatively final grades in both datasets: in a romantic relationship (`romantic_yes`), does not want to go to higher education (`higher_no`), lives in a rural area (`address_R`) and has no access to internet (`internet_no`).
- Variables that impact positively final grades in both datasets: not in a romantic relationship (`romantic_no`), wants to go to higher education (`higher_yes`), lives in a urban area (`address_U`), has access to internet (`internet_no`).
- In Portuguese performance dataset, the `school` variable has a very high impact on the final grade (negatively impacted if goes to MS and positively impacted if goes to GP).
- Males seem to score higher in math whereas females score higher in portuguese.

## Visualizing Key Trends

Some of the results are quite unexpected so let's visualize them. 

### Effect of Address Type on Grades


![](/images/school-success/school-success_34_0.png)


Insights: 
- For math performance, there is not too much difference between urban and rural students. However, urban students tend to score slightly more.
- For portuguese performance, we can see that urban students score higher more often than rural students.

### Effect of Relationship Status on Grades


![](/images/school-success/school-success_37_0.png)





Note, that of the 395 math students, 132 (33.4%) were in a relationship. Likewise 239 (36.8%) or of the 649 Portuguese students were in a relationship



Insights: 
- In both datasets, there are more single students than in a relationship (only 33% in math dataset and 36% in portuguese dataset). This might skew results as there is less data to analyze for students in a relationship. We can see that in the Portuguese dataset where there are more values to analyze, the scatter plot shapes tend to look more similar. 
- Not enough data to say if relationship has true impact on math performance. 

### Effect of Sex on Grades


```python
fig, axs = plt.subplots(2, 1, figsize=(12,10))
plt.subplots_adjust(hspace=.25)

def sex_plot(data, ax, subject):
    ax.set_xlim(0, 20)
    sns.kdeplot(data.loc[data['sex'] == 'F', 'G3'], label='Female', shade=True, ax=ax)
    sns.kdeplot(data.loc[data['sex'] == 'M', 'G3'], label='Male', shade=True, ax=ax)
    ax.set_title(f'Female vs Male Students {subject} Performance')
    ax.set_xlabel('Grade')
    ax.set_ylabel('Density')

sex_plot(data_m, axs[0], subject='Math')
sex_plot(data_p, axs[1], subject='Portuguese')
```


![](/images/school-success/school-success_41_0.png)


### Effect of School Choice on Grades


```python
#Analyzing impact of choice of school on Portuguese performance
plt.subplots(figsize=(12,8))
b = sns.swarmplot(x='school', y='G3', data=data_p)
b.axes.set_title('School Choice vs Final Grade Portuguese')
b.set_xlabel('School')
b.set_ylabel('Final Grade');
```


![](/images/school-success/school-success_43_0.png)


Insights: 
- From the available data, MS students (`school_MS`) tend to score less than GP students (`school_GP`) in Portuguese. Maybe GP is specialized in Portuguese and students have access to higher-quality resources.
- However as for the relationship analysis, there are less students going to MS so it might affect results.

## Model-fitting

We are now going to build a multi-linear regression model for both datasets. To avoid the impact of correlated variables, we only use the top twelve most influential predictors. We start with the math scores.


```python
def fit_regression_model(df, dummy_df):
    num_df = df.select_dtypes(exclude=['object'])
    full_df = pd.concat([num_df, dummy_df.drop('G3', axis=1)], axis=1)
    full_df.drop(['G1', 'G2'], axis=1, inplace=True)
    most_inf = np.abs(full_df.corr()['G3']).sort_values()[-13:].index
    red_df = full_df.loc[:, most_inf]

    X = np.array(red_df.drop('G3', axis=1))
    y = np.array(red_df['G3'])

    Z = sm.add_constant(X)
    mod = sm.OLS(y, Z).fit()
    
    results_as_html = mod.summary().tables[1].as_html()
    coeffs = pd.read_html(results_as_html, header=0, index_col=0)[0]
    coeffs = coeffs.set_index(pd.Index(['intercept']).append(red_df.drop('G3', axis=1).columns))
    
    return mod.rsquared, coeffs
```


```python
r2_m, coeffs_m = fit_regression_model(data_m, dummy_dfm)

print(f"Model R^2: {r2_m:.02f}")
display(coeffs_m)
```

    Model R^2: 0.20
    



<table>
  <thead>
    <tr>
      <th></th>
      <th>coef</th>
      <th>std err</th>
      <th>t</th>
      <th>P&gt;|t|</th>
      <th>[0.025</th>
      <th>0.975]</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>intercept</th>
      <td>10.2932</td>
      <td>3.454</td>
      <td>2.981</td>
      <td>0.003</td>
      <td>3.503</td>
      <td>17.083</td>
    </tr>
    <tr>
      <th>paid_yes</th>
      <td>0.2347</td>
      <td>0.439</td>
      <td>0.534</td>
      <td>0.593</td>
      <td>-0.629</td>
      <td>1.099</td>
    </tr>
    <tr>
      <th>sex_M</th>
      <td>1.1617</td>
      <td>0.436</td>
      <td>2.665</td>
      <td>0.008</td>
      <td>0.305</td>
      <td>2.019</td>
    </tr>
    <tr>
      <th>address_U</th>
      <td>0.5889</td>
      <td>0.543</td>
      <td>1.084</td>
      <td>0.279</td>
      <td>-0.479</td>
      <td>1.657</td>
    </tr>
    <tr>
      <th>Mjob_health</th>
      <td>1.1831</td>
      <td>0.779</td>
      <td>1.519</td>
      <td>0.130</td>
      <td>-0.349</td>
      <td>2.715</td>
    </tr>
    <tr>
      <th>traveltime</th>
      <td>-0.2877</td>
      <td>0.324</td>
      <td>-0.887</td>
      <td>0.376</td>
      <td>-0.926</td>
      <td>0.350</td>
    </tr>
    <tr>
      <th>romantic_yes</th>
      <td>-0.8371</td>
      <td>0.458</td>
      <td>-1.829</td>
      <td>0.068</td>
      <td>-1.737</td>
      <td>0.063</td>
    </tr>
    <tr>
      <th>goout</th>
      <td>-0.4753</td>
      <td>0.194</td>
      <td>-2.450</td>
      <td>0.015</td>
      <td>-0.857</td>
      <td>-0.094</td>
    </tr>
    <tr>
      <th>Fedu</th>
      <td>-0.1004</td>
      <td>0.251</td>
      <td>-0.400</td>
      <td>0.689</td>
      <td>-0.594</td>
      <td>0.393</td>
    </tr>
    <tr>
      <th>age</th>
      <td>-0.0467</td>
      <td>0.178</td>
      <td>-0.263</td>
      <td>0.793</td>
      <td>-0.396</td>
      <td>0.302</td>
    </tr>
    <tr>
      <th>higher_yes</th>
      <td>1.4442</td>
      <td>1.044</td>
      <td>1.383</td>
      <td>0.167</td>
      <td>-0.608</td>
      <td>3.497</td>
    </tr>
    <tr>
      <th>Medu</th>
      <td>0.4811</td>
      <td>0.259</td>
      <td>1.861</td>
      <td>0.064</td>
      <td>-0.027</td>
      <td>0.989</td>
    </tr>
    <tr>
      <th>failures</th>
      <td>-1.7399</td>
      <td>0.314</td>
      <td>-5.547</td>
      <td>0.000</td>
      <td>-2.357</td>
      <td>-1.123</td>
    </tr>
  </tbody>
</table>


Insights for math data set linear regression model:
- Our model explains explains 20% of the inputs into the final grade (`G3`), however it could still be improve if the goal of this article would be pure accuracy. 
- We can see that the willingness of the student to go into higher education (`higher_yes`) is a variable with one of the largest absolute coefficients. If the student is willing to go into higher education, their score will increase, on average, by 1.44 points. 
- There are other statistically significant coefficients such as `failures`, `sex_M`, and `goout`. 
- For example, `failures` plays a decisive role in student performance: for each class the student has failed in the past, they can roughly except a decrease of 1.74 in their final score. 

And now for the Portuguese scores.


```python
r2_p, coeffs_p = fit_regression_model(data_p, dummy_dfp)

print(f"Model R^2: {r2_p:.03f}")
display(coeffs_p)
```

    Model R^2: 0.305
    



<table>
  <thead>
    <tr>
      <th></th>
      <th>coef</th>
      <th>std err</th>
      <th>t</th>
      <th>P&gt;|t|</th>
      <th>[0.025</th>
      <th>0.975]</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>intercept</th>
      <td>9.8593</td>
      <td>0.612</td>
      <td>16.114</td>
      <td>0.000</td>
      <td>8.658</td>
      <td>11.061</td>
    </tr>
    <tr>
      <th>Mjob_teacher</th>
      <td>0.2976</td>
      <td>0.384</td>
      <td>0.776</td>
      <td>0.438</td>
      <td>-0.456</td>
      <td>1.051</td>
    </tr>
    <tr>
      <th>internet_yes</th>
      <td>0.3248</td>
      <td>0.269</td>
      <td>1.207</td>
      <td>0.228</td>
      <td>-0.204</td>
      <td>0.853</td>
    </tr>
    <tr>
      <th>address_U</th>
      <td>0.3521</td>
      <td>0.252</td>
      <td>1.397</td>
      <td>0.163</td>
      <td>-0.143</td>
      <td>0.847</td>
    </tr>
    <tr>
      <th>reason_reputation</th>
      <td>0.4602</td>
      <td>0.270</td>
      <td>1.704</td>
      <td>0.089</td>
      <td>-0.070</td>
      <td>0.990</td>
    </tr>
    <tr>
      <th>Walc</th>
      <td>-0.1570</td>
      <td>0.108</td>
      <td>-1.455</td>
      <td>0.146</td>
      <td>-0.369</td>
      <td>0.055</td>
    </tr>
    <tr>
      <th>Dalc</th>
      <td>-0.3119</td>
      <td>0.149</td>
      <td>-2.098</td>
      <td>0.036</td>
      <td>-0.604</td>
      <td>-0.020</td>
    </tr>
    <tr>
      <th>Fedu</th>
      <td>0.1503</td>
      <td>0.129</td>
      <td>1.169</td>
      <td>0.243</td>
      <td>-0.102</td>
      <td>0.403</td>
    </tr>
    <tr>
      <th>Medu</th>
      <td>0.0980</td>
      <td>0.137</td>
      <td>0.718</td>
      <td>0.473</td>
      <td>-0.170</td>
      <td>0.366</td>
    </tr>
    <tr>
      <th>studytime</th>
      <td>0.4366</td>
      <td>0.137</td>
      <td>3.192</td>
      <td>0.001</td>
      <td>0.168</td>
      <td>0.705</td>
    </tr>
    <tr>
      <th>school_MS</th>
      <td>-1.0299</td>
      <td>0.252</td>
      <td>-4.087</td>
      <td>0.000</td>
      <td>-1.525</td>
      <td>-0.535</td>
    </tr>
    <tr>
      <th>higher_yes</th>
      <td>1.6627</td>
      <td>0.376</td>
      <td>4.421</td>
      <td>0.000</td>
      <td>0.924</td>
      <td>2.401</td>
    </tr>
    <tr>
      <th>failures</th>
      <td>-1.4374</td>
      <td>0.193</td>
      <td>-7.449</td>
      <td>0.000</td>
      <td>-1.816</td>
      <td>-1.058</td>
    </tr>
  </tbody>
</table>


Insights for the portuguese data set linear regression model:
- Our model explains explains 30.5% of the inputs into the final grade (`G3`), better than the math model but still leaving room for improvement.
- We again see that the desire to go into higher education and the number of previous failures are highly influential when determining a student's final grade.
- There are other statistically significant coefficients such as `school_MS`, `failures` and `studytime`. 
- In fact, the influence of going to Mousinho da Silveira is strong, with an expected decrease in one mark in a student's Portuguese grade

## Conclusion

We have seen that many factors can influence your final grades, the strongest of which typically being socio-economic characteristics (address, parent's education, family relationship, etc.) that cannot be changed. Those factors can also depend on the potential biases of the dataset. For example, maybe the mother's unemployment status has a bigger cultural impact on Portuguese student than on UK students. However, some variables that are controllable by the student such as `studytime`, going out (`goout`), consumption of alcohol (`Dalc` and `Walc`) and potentially relationship status (`romantic`) have been proved to have an impact on the final grade (`G3`) of students in these datasets. 

Although valuable insights have been gleaned from this dataset it is clear from our poorly fitting regression model that linear interactions alone are insufficient for capturing a system as complicated as a student's school performance. If a purely performative model is what we desired, then moving towards a tree-based model or including carefully chosen interaction terms would be advised.
