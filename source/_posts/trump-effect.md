---
title: "The Trump Effect: Can Data Explain What We Never Saw Coming?"
date: 2020-08-14
updated: 2020-08-14
author: "Tom Palmer"
contact: "https://www.linkedin.com/in/tom-palmer-61954a177/"
tags:
- data-analysis
- regression
- visualization
categories:
- [Social Sciences, Politics]
languages:
- r
description: "Everyone has their theories on what led to Trump's surprise victory in the 2016 presidential election, but what does data science have to say on the matter?"
cover: /banners/trump-effect.jpg
---
{% note info %}
**Accessing Post Source**
We are still working on getting this site set up, so source code for this post is not yet available. Check back soon and you’ll be able to find it linked here.
{% endnote %}
Looking back four years ago to the United States's 2016 Presidential election, it can be easy to forget how confident people were that Trump couldn't possibly win the race. With the 2020 election fast approaching, it is critical that we can understand what led to his victory and how that might influence the upcoming result. We will do this not by relying on speculation or political opinion, but by showcasing a data-driven regression model that we can use to reliably intuit the primary demographic and socio-economic factors that led to Trump's victory. In doing this, we seek to answer two questions:

1. Despite his overall unpopularity, how did Trump pull off an election victory? 

2. Why did this come as such a surprise?


![Newspaper headlines incorrectly predicting a loss for Trump](/images/trump-effect/newspaper_headlines.jpg)
## How Trump Won (and Lost)
{% note info %}
**A Brief Introduction to the Electoral College**
The Electoral College is the United State’s electoral system, which allocates each of its 50 states plus DC a set number of votes, loosely (though not exactly) based on their populations. The winner of the plurality vote in each state receives that state’s full number of college votes (with the exception of Maine and Nebraska).
{% endnote %}
To address our first question, despite losing the national popular vote, Trump was returned as president in 2016 by the electoral college. That is, despite having less votes overall, the states that he did win were such that he ended up with more college votes allocated to him than Clinton did, and so claimed his victory. This is intuitive when we see that Clinton won heavily in large states, such as California (by a wide 30% margin), giving her 55 college votes, whilst Trump won by less than a percent in Michigan, Pennsylvania, and Wisconsin, as well as taking Florida by 1.2%, winning him 75 college votes for these alone. These small wins count for far more than Clinton blowing Trump away in California, since a state victory leads to the same amount of college votes regardless of the margin.




![](/images/trump-effect/trump-effect_7_0.png)


Since this system is so state-centric, we can pinpoint exactly where Trump won electoral votes that in turn won him the election. There were only six states that changed party, all switching from voting Obama to voting Trump. This can be shown on an electoral map of the US. All states which voted Republican in 2012 and 2016 are in red, whilst blue denotes the same for the Democrats. Greyed states are those which voted Obama, then Trump. Effectively, these 6 states decided the president. 




![State color changes from 2012 to 2016](/images/trump-effect/changing_states.png)
Incredibly, of these 6 states, 4 of them were won by a percent or less. In the others—Ohio and Iowa—Trump saw a huge swing his way, winning both by close to 10%. 
Aside from these margins, the other crucial thing to note is the geographical proximity of 5 of these states. Broadly, these are all part of the midwest, and make up a region known as the “rust belt”. These used to be manufacturing powerhouses of the US, are largely white, and (owing to the US’s departure from a manufacturing economy) have rising unemployment. One of the key outcomes of this project is to demonstrate that Trump’s departure from typical Republican vote shares gave him the perfect coalition of states to win the White House without needing the national popular vote. To understand exactly how these states shot him to victory, we'll need a statistical model to help us grapple with the complexities of election dynamics.


![](/images/trump-effect/trump-effect_11_0.png)

{% note success %}
You will likely notice the outlying state of Utah, coloured purple. We explain the cause of this deviation in our [section on model outliers](#outliers).
{% endnote %}
## Modelling the Problem

In order to understand what led to Trump's victory, we needed to develop a model that can capture the complex relationships between voter attributes and election outcomes. After trawling the web for relevant data sources, we ended up with enough fine-grained data to model the problem at a county level. This included demographic and socio-economic breakdowns for each county, as well as the presidential election vote counts for the years 2008, 2012, and 2016.
{% note info %}
**Data Sources & Variable List**
A summary of the data sources used for this analysis can be found at [this link](https://github.com/warwickdatascience/wdss-research-website/tree/master/content/trump-effect/data/sources.yml) and a list of included variables can be found in [the post appendix](#appendix).
{% endnote %}
We took this data and formed a model in which we aimed to predict, for each county, the difference in Republican vote share from 2008/2012 to 2016 based on the descriptors we had available. By inspecting the coefficients of this model, we would then be able to intuit the impact that various demographic and socio-economic factors had on Trump's victory. 

This framework of modeling is highly complex, with a large number of correlated inputs and two correlated outputs (the 2008/16 and 20012/16 differences). A naïve approach would be to fit a multivariate [OLS model](https://statisticsbyjim.com/glossary/ordinary-least-squares/), but this would almost certainly suffer from [multicolinearity](https://statisticsbyjim.com/regression/multicollinearity-in-regression-analysis/). This is a phenomenon in linear modelling that occurs when combinations of predictions are highly correlated with others. This can have a severe impact on our regression coefficients, making it near impossible to determine which factors actually influenced the outcome.

A common workaround is to implement [principal component regression (PCR)](https://learnche.org/pid/latent-variable-modelling/principal-components-regression), which prevents multicolinearity by first projecting the input predictors to a lower dimensional space in which all variables are orthogonal. This method still has its drawbacks, however; namely, the projection is chosen to maximise variance in the predictor space only, not taking into account which combinations of predictors are actually good for predicting. This could easily lead to scenarios in which valuable input variables are discarded in the projection because they don't express much variance.

To combat this issue, we decided to use a slightly more complex model known as [partial least squares (PLS) regression](https://stats.idre.ucla.edu/wp-content/uploads/2016/02/pls.pdf). This is a model used heavily in cheminformatics and signal processing for its ability to robustly handle highly-correlated predictors and responses without sacrificing predictive accuracy. The model is trained using a simple interative procedure, resulting in standardized coefficients, giving the predicted impact of each input factor on the response. In our case, we can use these coefficients to understand which demographic and socio-economic factors had the largest impact in Trump's victory.

By using a statistical model such as PLS regression, we are able to capture relations that are unlikely to be detected with a simple model or by rudimentary data visualisation. This allows us to draw detailed political insight, in the knowledge that our results are backed by data and rigourous statistical methods. This is the power that data science brings to this analysis, letting us answer old questions in new, insightful ways.
{% note info %}
**Code Attributions**
Data scraping and initial model development was performed by [Janique Krasnowska](https://www.linkedin.com/in/janique-krasnowska-94a1a0195/), with support, final tweaks and statistical write-up by [Tim Hargreaves](https://www.linkedin.com/in/tim-hargreaves/). The intial modelling framework and data sources were suggested by [Tom Palmer](https://www.linkedin.com/in/tom-palmer-61954a177/), the author of this post.
{% endnote %}{% note success %}
**Further Reading**
If you wish to learn more about PLS regression and its implementation in R, the [following vignette](https://cran.r-project.org/web/packages/pls/vignettes/pls-manual.pdf) is a great starting point.
{% endnote %}
## Explaining Trump's Victory
{% note danger %}
**Risk of Misinterpretation**
To avoid misuse of our models, it is important to highlight two key facts:
- All patterns shown in this post are correlations, not causations. By combining these trends with political theory and performing appropriate tests on our model, we can be more more confident in the causal nature of such patterns, but we can never be sure
- The standardised coefficents from the model shown below do not directly relate to the impact of different factors on Trump's swing, but rather give relative values more appropriate for comparison. Our PLS has the potential to give absolute coefficients, but we have omitted these in this post for simplicity and clarity.
{% endnote %}
### Age

We began our exploration by testing the theory that support for Trump largely grows with increasing demographic age. Interestingly, our results support a more nuanced view, suggesting that his appeal is more generational, and that Trump's main gain was from an older, yet still working age, demographic.
{% note warning %}
**Understanding Standarised Coefficient Plots**
This section contains several visualisations of the standardised coefficients from our model. These show the influence of a given predictor on the likelihood of Trump gaining a vote over a previous Republican candidate. In other words, a large positive coefficient means that a certain factor in a population led to Trump gaining votes, a large negative coefficent relates to Trump losing votes, and a small coefficient implies the factor had little impact.
{% endnote %}

![](/images/trump-effect/trump-effect_28_0.png)


This is an unusual finding, and we take two conclusions from this. Firstly, the generational divide in politics does exist. In terms of Trump-populism, there is no linear adage we can apply, such as "the older you get, the more conservative you become". Instead the trends are highly generational (think baby boomers, Generation Z, millennials, etc.). This cyclic nature of history is supported by [Peter Turchin's recent work](https://www.theguardian.com/technology/2019/nov/12/history-as-a-giant-data-set-how-analysing-the-past-could-help-save-the-future) suggesting that many historical and political trends can be modelled surprisingly well using periodic systems. Secondly, a key base of Trump’s was the older working population; people in full-time work, but pre-retirement seemed to be particularly enamored with Trump's message compared with previous Republicans'.

### Industry

With the knowledge that Trump swung five “rust belt” states his way, and that these are known for their waning manufacturing industries, it was critical that we included industry breakdowns in our model formulation. From this, we found a strong positive swing to Trump from production workers, corroborating the theory that this is how he swung these particular states. Clearly, this played a huge part of his campaign, aiming rhetoric at returning jobs to America and backing American manufacturing.


![](/images/trump-effect/trump-effect_32_0.png)


This massive shift in voter base was essential for Trump’s win, as it allowed him to unexpectedly take the midwest, with it's large proportion of production workers.


![](/images/trump-effect/trump-effect_34_0.png)


### Race

The graph above also hints that race played a large role in Trump's victory. Our model confirms this, highlighting in particular that white people swung heavily towards Trump, whereas black and hispanic people swung away. This is particularly relevant to the midwest, since it is one of the whiter areas of the US, meaning Trump’s success here, and therefore in the election at large, can be partially attributed to his success in winning over white people.


![](/images/trump-effect/trump-effect_36_0.png)


In fact, our data had a higher fidelity than race alone, including the intersection of common races and sexes. This allows us to also note, perhaps unsurprisingly, that Trump gained more male votes than female, regardless of race.


![](/images/trump-effect/trump-effect_38_0.png)


### Religion

Effectively coding religious demography proved challenging, as there are a huge range of denominations, many having relatively few adherents. Our goal was to balance out religous fidelity with introducing too many variables as to add noise to the model. In the end, we separated Evangelical groups into their own category, as there was (and still is) [a lot of speculation](https://play.acast.com/s/intelligencesquared/whydoevangelicalsworshipatthealtarofdonaldtrump-withsarahposnerandbrianklaas) that they played a crucial role in his victory. Despite this, the data strongly suggests that this variable is largely unimportant, as Trump seemed to lose Evangelical votes, but still performed well enough to win in Republican heartlands. The swing against Trump in the “bible belt” was minor, and insufficient to change the election outcome. This a fascinating example of how data science lets us see past our preconceptions and biases, to understand problems with greater clarity.


![](/images/trump-effect/trump-effect_41_0.png)


For reference, the religious distributions for both the midwest and remaining US are shown below.


![](/images/trump-effect/trump-effect_43_0.png)


### Education & Income

The crucial findings in this area show us both how different Trump was as a candidate compared to previous Republicans, and also how largely unimportant certain swings were. In terms of education, Trump was incredibly unpopular, facing a large negative swing from bachelor's degree holders. However, this did little to impact his success. One explanation for this is that educational attainment is concentrated in areas where Democrats are already successful, so in the “winner takes all” system of the US, a further loss was largely irrelevant.

Conversely, unemployment and poverty correlated positively with Trump voters, further backing our argument of him taking traditional Democrat voter groups.


![](/images/trump-effect/trump-effect_45_0.png)


The impact of the change in Trump's appeal towards bachelor's degree holders is easily seen when we plot a heatmap of bachelor degree attainment; a dark patch is centred lower midwest where key swing states are located.


![](/images/trump-effect/trump-effect_47_0.png)


### Outliers

Overall, we believe that our model is a strong success. Not only does it provide evidence for several previously speculative theories, it also casts doubt on some unproven beliefs. Our model captures a good proportion of the variability of the response with a desirable error distribution.


![](/images/trump-effect/trump-effect_50_0.png)


As with all models, outliers exist, but these can be easily explained. On one end (marked blue), we overpredicted the swing from several counties in Utah and Idaho. That is, based on the trends we saw elsewhere, our model suggested he should have performed better than he did. This deviation from our predictions can be explained in one word—Mormons. Many counties in this region of the US were settled by the Church of Latter Day Saints, leading to a third Mormon candidate, Evan MacMullin, claiming a sizeable share of votes (20% in Utah, 6% in Idaho) largely from Trump, leading to this minor discrepancy in our model.

On the other end of the spectrum, we have areas such as Laporte County, Indiana (marked green) which we underpredicted. In other words, Trump did better in these areas than our model predicted. This is partially explained by Trump choosing Mike Pence to be his running mate. VP candidates are often hand-picked to help “deliver” a region. In this case, Pence was a longterm governor from a rust belt state. The model does not have a way to account for the running mate effect (though this could be introduced with manual feature engineering), hence underpredicted the swing Trump will have obtained from choosing Indiana-favourite Pence as running mate. 
{% note success %}
Although we've only showed the 2008–2016 differences here, the outliers for 2012 are largely similar, though exacerbated even further by the fact that Utah was 2012 Republican candidate Mitt Romney's home state.
{% endnote %}
## Conclusion

With that, we conclude our whirlwind tour of Trump's 2016 presidential victory. Our model has cast light on Trump’s effect and dependence on a unique coalition of states in order to pull off his unexpected win. Upon analysing trends in historical patterns, we find that traditional left/right distributions (such as income and religion) were largely unimportant in this election, particularly compared to education levels and industry distributions. 

Our work also highlights the groups that Trump must retain in order to win again in 2020. Much is made of his performance with evangelical groups—traditionally bastions of the Republican party—but our data-driven approach shows that this is largely a side factor, contrary to popular speculation. To win again, Trump doesn’t need more votes in evangelical areas—the "bible belt” as it is usually known—but instead, he must retain workers in the production industry, and the older working generation. This enabled him to win the midwest states that were sufficient to edge him into the White House and could quite possibly keep him there.

This project showcases data science at its best, bringing together statistics, computer science, and domain expertise to solve an old problem in a new way. With this collaboration of disiplines, such conclusions would not be possible: political speculation and theory would lack supportive evidence that can only be derived through advanced statistical modelling; on the other hand, without the ability to tie model results to reality using domain knowledge and insight, the practicality and real-life validity of a statistical model can rarely be relied upon. This project was only facilitated by Warwick Data Science Society's community of students and the infrastructure they provide for blogging. We hope that this post inspires fellow students to consider the insight that data science can bring to their field and to engage with WDSS to produce similar works. Thank you for reading.

## Appendix
{% note success %}
For a circle of correlations, please see the source notebook.
{% endnote %}
    Table of Standardized Coefficients
    ==================================
    
                     diff0816 diff1216
    0to4                0.029    0.025
    10to14             -0.060   -0.080
    15to19             -0.057   -0.066
    20to24              0.000    0.007
    25to29              0.023    0.040
    30to34              0.002    0.011
    35to39             -0.023   -0.028
    40to44             -0.025   -0.034
    45to49              0.029    0.031
    5to9               -0.027   -0.040
    50to54              0.097    0.107
    55to59              0.072    0.075
    60to64              0.019    0.020
    65to69             -0.043   -0.045
    70to74             -0.064   -0.065
    75to79             -0.020   -0.020
    80to84              0.047    0.052
    85+                 0.080    0.084
    AsianF             -0.011   -0.001
    AsianM             -0.002    0.009
    BlackF             -0.115   -0.085
    BlackM             -0.098   -0.067
    HispanicF          -0.086   -0.081
    HispanicM          -0.077   -0.072
    WhiteF              0.099    0.067
    WhiteM              0.115    0.084
    UnemploymentRate    0.068    0.090
    IncomeLog          -0.080   -0.095
    Poverty             0.058    0.090
    Professional       -0.110   -0.122
    Service             0.028    0.051
    Office             -0.049   -0.045
    Construction       -0.001   -0.009
    Production          0.132    0.136
    popsqmile           0.024    0.036
    High School        -0.036   -0.057
    Bachelor           -0.228   -0.250
    Mainline            0.178    0.183
    Evangelical        -0.054   -0.050
    Catholic            0.124    0.137
    Black Prot         -0.067   -0.039

