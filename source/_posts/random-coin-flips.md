---
title: "Random Coin Flips"
date: 2021-10-08
updated: 2021-10-08
authors_plus:
- "Ivan Silajev"
- "Conor Bateman"
contacts_plus:
- "https://www.linkedin.com/in/ivan-silajev-04957a18b/"
- "https://www.linkedin.com/in/conor-bateman-b742131b7/"
editor: "Keeley Ruane"
editor_contact: "https://www.linkedin.com/in/keeley-ruane-6aab4219b/"
tags:
- shiny
- probability
- randomness
categories:
- [Mathematics, Statistics]
languages:
- r
description: "Humans are inherently bad at understanding randomness and probability. The classic example is the coin-flip. In this post use statistical hypothesis testing to show this phenomenon." 
cover: /banners/coin-flip.jpg
---
{% note info %}
This post is the corresponding write-up for a WDSS project in which a pair of students in Statistics collaborated to produce a web app for testing user’s ability to simulate a believable sequence of independent Bernoulli events akin to a series of coin flips. You can view the final product at [this link](https://app.wdss.io/random-coin-flips/).
{% endnote %}
## Project Motivation

Random events happen without an underlying pattern, meaning no consistent algorithm can produce a series of truly random events. 
After numerous psychological tests, scientists found that people often approach the concept of randomness with underlying assumptions about its nature - usually ones that contradict its definition. 
Humans have an inherent tendency to look for predictability in anything they encounter to improve their understanding of it.
Unfortunately, this instinct often leads to a paradox where one attempts to make sense of randomness as something predictable, worsening their understanding of it instead.

With the development of statistical mathematics, we can “measure” the randomness of events with appropriate hypothesis testing methods.
The motivation behind this project is to create a program that, with the help of hypothesis testing theory, grades a user’s ability to create plausible random sequences.
This project is interested only in measuring randomness in human-generated binary sequences.

# Preliminaries

There is not yet an official way to measure randomness, however, there are statistical tests that, when combined, accomplish such a function to a reasonable degree.
The project utilises seven tests deemed to be useful enough for detecting implausible random sequences.
We will justify the usage of the seven tests before explaining how to carry them out. First, let's start with explaining the basics.
{% note info %}
A **binary sequence** is an ordered string consisting of two different symbols only.
Commonly, computers express binary sequences using the symbols **1** and **0**.
An example of such a binary sequence is **100011** and has a length of six because it consists of six symbols.
Numeric sequences, in general, possess a wide range of characteristics expressible as values; binary sequences are no exception.
{% endnote %}
Numerical properties of binary sequences that can be measured include:
* The length of the sequence
* The number of **0**s and **1**s
* The proportion of **0**s or **1**s to the length of the sequence
* The longest run of one symbol (the second-longest, third, etc.)
* The number of runs
* The number of runs of a specified length
* etc. ...

These measures can be used to determine how close a human-generated binary sequence is to a truly *random* binary sequence. Whenever we are dealing with uncertainity about the truth value of a given statement, statisticians will turn to **hypothesis testing**. People cannot fully validate a hypothesis about the properties of an unknown quantity of interest (e.g. mean incomes of a household in the UK, the variation of exam marks at Warwick) without analysing all members of the population related to the variate, which is often impossible. Therefore statisticians use samples, a limited number of members from the population, to yield partial evidence for the properties of a variate.
{% note info %}
A **hypothesis test** is a tool for producing partial evidence for a hypothesis from samples, the performance of which depends on the amount of information available for testing and the nature of the test.
{% endnote %}
A hypothesis test often conveniently gives evidence as a **p-value**, commonly defined as the probability that a variate abiding by its hypothesised properties produced a given sample. The smaller the probability that the hypothesised variate could have produced the sample, the smaller the p-value. By this logic, a p-value of a test can serve as a measure of how closely a series of Bernoulli events can resemble a given binary sequence.
{% note success %}
The level of statistical significance is often expressed as a **p-value** between 0 and 1. The smaller the p-value, the stronger the evidence against the null hypothesis.
{% endnote %}
More information on hypothesis testing and statistical inference can be found in H. Liero, S. Zwanzig (2011), *Introduction to the Theory of Statistical Inference* and G. Casella, R. L. Berger (2002), *Statistical Inference, Second Edition*

# Overiview of the tests

This section explains what the properties and rationale are behind the seven apps implemented in the Shiny R app. For more mathematically involved derivations of each of these tests, refer to [the Theory section](#the-theory). 

The statistical tests used in this project include:
* The Bernoulli Distribution Test
* The Generalised Runs Test
* The Longest Run Length Test
* The Hadamard-Walsh Test
* The Multinomial Test
* The Last Equalisation Test

There exist time-series methods for measuring the predictability of a sequence, of which none were used in the project due to time constraints and limited intellectual resources.
The rest of this document will explain the theory behind each test and the program's design.

## Bernoulli Distribution Test

The standard Bernoulli Distribution Test tests the plausibility that a series of identical, independent Bernoulli events can produce a given binary sequence.
A Bernoulli event is essentially a coin toss with a set bias towards a specified side of the coin.
Based on this interpretation of a Bernoulli event, the Bernoulli Distribution Test is highly appropriate for the project’s purpose.
The test uses the proportion of **1**s to the sequence length as its only input, which carries no information about the arrangement of the sequence.

Thus, a sample with a **1**s to length ratio that strongly deviates from the hypothesised proportion would result in a small p-value upon applying the Bernoulli Distribution Test.
It is necessary to utilise a different set of tests altogether to consider the arrangement of entries in a given sequence.

## Generalised Runs Test

The Generalised Runs Test is a hypothesis test inspired by the non-parametric Wald-Wolfowitz Runs Test.
The Wald-Wolfowitz Runs Test tests the serial independence of entries in a binary sequence of a given length using the number of runs in the series as an input.
Unlike the Wald-Wolfowitz Test, the Generalised Runs Test does not assume that samples come from a finite population and does not assume that the two outcomes are equally likely.

Unfortunately, unlike the Bernoulli Distribution Test, the Generalised Runs Test has an underdeveloped theory.
Statisticians do not yet know the limiting distribution of runs in a Bernoulli trial sequence.
Regardless, the test considers the arrangement of **1**s and **0**s in the series, which the Bernoulli Distribution Test does not.

A sequence with one run is a repetition of one symbol. In contrast, a sequence with maximal runs is a periodic sequence of isolated **1**s and **0**s.
The two possibilities mentioned strongly express patterned behaviour, meaning they are weak contenders for being random sequences.
Therefore, the number of runs in a sequence should be between one and the sequence length to plausibly represent a series of independent Bernoulli events.

## Longest Run Length Test

Similar to the Generalised Runs Test, the Longest Run Test is underdeveloped but less so.
The test uses the length of the longest run in a binary series as its input.
This test also considers the arrangement of **1**s and **0**s in the sequence, though differently this time.

A sequence whose maximum run length is one is a periodic sequence of isolated **1**s and **0**s.
Alternatively, a sequence with a maximum run as long as the series consists of only one symbol.
Again both possibilities are weak contenders for being random sequences for being too patterned.
So, the longest run in a sequence should fall between the two extreme cases to plausibly represent a series of independent Bernoulli events.

## Hadamard-Walsh Test

Similar to how one can decompose functions with continuous domains into a sum of sine and cosine waves with a Fourier transform, one can decompose binary sequences into sums of Walsh functions with a Hadamard-Walsh transform.
A Walsh function is a periodic square wave function that takes one and negative one as its values.
One can decompose any binary sequence into Walsh functions because they constitute a complete set of orthogonal discrete functions.

The transform yields a vector that numerically indicates how strongly a given binary sequence resembles each Walsh function.
The disadvantage of the Hadamard-Walsh transform is it works only with vectors of lengths equal to powers of two, so the project will work only with binary sequences of lengths 32 and 64 to account for the limitation.

Theoretically, a random sequence is more likely to resemble every Walsh function weakly.
The more a sequence resembles a single Walsh function, the more patterned it is.

## Multinomial Test

The natural extension to the Bernoulli Distribution Test is looking at pairs of tosses.
For $p = 1/2$, we expect there to be an equal frequency $n/4$, of Head-Head, Head-Tail, Tail-Head and Tail-Tail pairs.
Generally, the more spread these frequencies have, the more improbable it is that the tosses were independent and came from $Bernoulli( 1/2 )$ distribution. 

For example, having all Head-Tail pairs suggests patterned behaviour, and so are weak contenders for random sequences. 
This test somewhat compliments the Bernoulli distribution test since the series **101010101010** will be given a p-value 1 by the Bernoulli Distribution Test, but a very low p-value for the multinomial test for $p = 1/2$.
This test can be easily extended to $p \neq 1/2$, as has been done in the program.

## Last Equalisation Test

By modelling the coin tosses as a Markov Chain, it is possible to calculate the probability distribution for the last time in which the number of heads will equal the number of tails.
We can then use our binary input to find the last equalisation in our observed sequence.

We define an equalisation in our binary sequence as the time step in which the number of **1**s and **0**s are equal. 
With this distribution and observed statistic, we can calculate the associated p-value of the observed value.

# App Design

All tests mentioned above are incorporated into a single R Shiny app that automatically calculates the required p-values and statistics from an input binary string.

![Screenshot of the app interface](/images/random-coin-flips/screenshot.png)

User can introduce the inputs on the left side of the app (input box) while the relevant outputs appear on the right.

The `Input Coin Flip Series` box accepts binary strings consisting of ones and zeros. 
The program treats any characters that are neither one nor zero as zeros.

The `Input Series Length` box grants the user a choice between an input sample of length 32 or 64.
If the input binary string has the incorrect length, the program will inform the user about the current length of the input string so the user will know how many terms to add or subtract.

The `Input Coin Bias` slider allows the user to set the bias of the Bernoulli distribution fitted to the input sample.
The program will not compute the p-values if the set bias is an integer; the program will warn the user if it is an integer.

The `Run tests` button will generate a table of p-values / metrics, and a KS plot of the p-vector generated by the Walsh-Hadamard test on the output space.

The generated  table shows the p-values all the hypothesis tests and the uniformity metric for the Walsh-Hadamard test.
Overall, the closer the p-values are to one, the better fitted the Bernoulli distribution is to the input sequence.
The closer the red line on the plot is to the black line, the smaller the Walsh-Hadamard test metric is, and the more random the input sequence is.

The app also offers a small guide in the right-hand corner of the screen. 

# The Theory

## Bernoulli Distribution Test Theory

The Bernoulli Distribution Test is derived as follows.

We define a sample $X$ as a vector of $n$ random variables, each representing an entry $X_i$ in a possible binary sequence:<br>

$$X=\left ( X_i \right )^{n}_{i=1}$$

We also define the following statistical model for the sample:<br>

$$ \left ( S,\left \{ 
f(x \mid \theta)
:
\theta \in \Theta
 \right \} \right )
=
\left ( \left \{ 0,1 \right \}^n,
\left \{ 
p^{n \bar{x}}
(1-p)^{n(1- \bar{x})}
:
p \in
\left [ 
0,1 \right ]
\right \}
 \right )$$
 
where $\bar{x}$ is the mean of a realised sample of $X$.

The statistical model explicitly states that the possible outcomes of the sample are binary sequences of zeros and ones.
The distribution fitted to each sample entry is a Bernoulli distribution, each with the same parameter $p$ taking values from zero to one.

By the theorems of sufficient statistics, the sample total $\sum X_i$ is enough to test whether the hypothesised Bernoulli statistical model is a good fit for a given realised sample.
By the theorems of point estimation, the sample total is the best unbiased estimator of the parameter $np$.
We can say the more the sample total deviates from a hypothesised value of $np$, the less likely a Bernoulli variate with parameter $p$ could have produced the sample.
The sample total has a binomial distribution with $n$ trials and parameter $p$.

We can formally state the hypothesis we want to test in terms of $p$ and its hypothesised value $\bar{p}$ bar.<br>

$$\begin{matrix}
H_0 : p=\bar{p}
\\ 
H_1 : p\neq \bar{p}
\end{matrix}$$

The p-value for the hypothesis that a Bernoulli variate with parameter $\bar{p}$ produced a given sample is given by:<br>
$$
p_{value}=\displaystyle\sum\limits_{q(r) \leq q(\sum x_i)} q(r):q(r)=\mathbb{P}\left( \sum X_i=r\right)
$$

## Generalised Runs Test Theory

The Generalised Runs Test is derived as follows.

Instead of fitting the distribution to the sequence, we fit the run distribution of a Bernoulli sample to the number of runs in a given realised sample.
The sample $X$ of coin flips and the statistical model tied to it is the same as before.
The statistic used to calculate the number of runs in a sample is as follows:<br>

$$r(X)=1+\displaystyle\sum\limits^{n-1}_{i=1}\left | X_i - X_{i+1} \right|$$

The distribution of statistic $r(X)$ is calculable through combinatorial deduction.
The pmf of $r(X)$ is given by:
$$
\mathbb{P}(r(X)=r)=\displaystyle\sum\limits^{n}_{h=0}\left ( 
k(n,h,r)+k(n,n-h,r)
 \right )
\cdot
p^h(1-p)^{n-h}
$$

The $k(n, h, r)$ coefficient enumerates the number of binary sequences, starting with a **1**, of length $n$, with $h$ **1**s that have $r$ runs.
The $k$ coefficient has the following formulas for $h \in [1,n-1]_{\mathbb{Z}}$:
$$
k(n,h,2r)=
\left(\begin{array}{c}h-1\\ r-1\end{array}\right)
\left(\begin{array}{c}n-h-1\\ r-1\end{array}\right)
\\
k(n,h,2r+1)=
\left(\begin{array}{c}h-1\\ r\end{array}\right)
\left(\begin{array}{c}n-h-1\\ r-1\end{array}\right)
$$

For $h \in \lbrace 0,n \rbrace$, $k$ is zero, unless if $h$ equals $n$ and $r$ is one.
Sequences consisting only of **1**s can only have one run; therefore $k(n, n, 1)$ is one for all $n$ in the natural numbers.

Since there is no actual runs parameter for the Bernoulli distribution, the best we can do is hypothesise that the sample consists of identically distributed independent Bernoulli variates.
$$
\begin{matrix}
H_0:X_i \mid X_j=X_i\sim Bernoulli(\bar{p}) \: \forall i,j \in \left [ 1,n \right ]_\mathbb{Z}
\\ 
H_1:X_i\nsim Bernoulli(\bar{p}) \: \forall i \in \left [ 1,n \right ]_\mathbb{Z}
\end{matrix}
$$                                
                  
The closer the number of runs is to the extreme cases, the more likely the alternative hypothesis becomes.
Therefore, we calculate the p-value using the classical two-sided approach, given that $p$ is $\bar{p}$:
$$
p_{value}=\displaystyle\sum\limits_{q(r) \leq q(r(x))} q(r):q(r)=\mathbb{P}(r(X)=r)        
$$   

More on the theory of runs can be found in A. M. Mood (1940), *The Distribution Theory of Runs* and J. V. Bradley (1960), *Distribution-Free Statistical Tests*.

## Longest Run Test Theory

The Longest Run Test is derived as follows.

Here, we fit the distribution for the longest run of a Bernoulli sample to the longest run length in a given realised sample.
The statistic used to calculate the run of maximal length in sample $X$ is given by:<br>
$$
m(X)=\max \left \{ k:
\left \{ X_{i+j} \right \}^{k-1}_{j=0}\in 
\left \{ \left \{ 1 \right \},\left \{ 0 \right \} \right \}
\wedge 
i,k \in \left [ 1,n \right ]_{\mathbb{Z}}
 \right \}
$$

The formula for the statistic translates to “the maximum number of consecutive entries in sample $X$ that are all equal to either zero or one”, where sample $X$ still follows the statistical model mentioned before.
The pmf of $m(X)$ is combinatorially more complex than $r(X)$.
$$
\mathbb{P}(m(X)=m)=\displaystyle\sum\limits^{n}_{h=0}\left ( 
t(n,h,m)-t(n,h,m-1)
 \right )
\cdot
p^h(1-p)^{n-h}
$$

The $t(n, h, m)$ coefficient enumerates the number of binary sequences of length $n$, with $h$ **1**s with a maximum run length of  $m$.
The $t$ coefficients follow the following recursive rule:
$$
{
t(n,h,m)=
t(n-1,h,m)
+t(n-1,h-1,m)
+t(n-2m-2,h-m-1,m)
\\
-t(n-m-2,h-1,m)
-t(n-m-2,h-m-1,m)
+e(n,h,m)
}
$$

where the $e$ coefficients are given by:<br>
$$
e(n,h,m)=\begin{cases}
1 & \text{ if } (n,h)=(0,0) \: \text{or} \: (2(m+1),m+1) \\ 
-1 & \text{ if } (n,h)=(m+1,0) \: \text{or} \: (m+1,m+1) \\  
0 & \text{ otherwise }
\end{cases}
$$

Again, there is no maximum run length parameter for the Bernoulli distribution, so we hypothesise that the sample consists of identically distributed independent Bernoulli variates as we did for the generalised runs test.
The closer the maximum run length is to the extreme cases, the more likely the alternative hypothesis becomes.
The p-value is calculated using the two-sided approach, with $p$ given as $\bar{p}$, as last time:<br>
$$
p_{value}=\displaystyle\sum\limits_{q(r) \leq q(m(x))} q(r):q(r)=\mathbb{P}(m(X)=r)    
$$

The derivation of the recursive formula for the $t$ coefficient can be found in M. F. Schilling (1990), ‘Longest Run of Heads’, *The College Mathematics Journal*.

## Walsh-Hadamard Test Theory

The Walsh-Hadamard Test is derived as follows.

The recursive formula for the Hadamard matrix is:<br>
$$
H_{2n}=\begin{pmatrix}
1 & 1\\ 
1 & -1
\end{pmatrix}
\otimes
H_n
:
H_1=(1)
$$

where the cross operator denotes the Kronecker product.

Let $X$ be the sample as before.
The statistic for the Walsh-Hadamard test is given by:<br>
$$
\omega (X)=H_n\cdot X=\left( \omega (X)_i \right )_{i=1}^{n}
$$

As before, we hypothesise that sample $X$ consists of identically distributed independent Bernoulli variates.
We calculate the p-vector (vector of p-values) for this test as follows:<br>
$$
p_{vector}
=(p_i)_{i=1}^{n}
:
p_i=
\begin{cases}
2 \cdot
\left ( 
1-\Phi \left ( 
\frac{\left | \omega(X)_i-n\bar{p} \right |}{
\sqrt{
n\bar{p}(1-\bar{p})
}
}
 \right )
 \right )
 & \text{ if } i=1 \\ 
2 \cdot
\left ( 
1-\Phi \left ( 
\frac{\left | \omega(X)_i \right |}{
\sqrt{
n\bar{p}(1-\bar{p})
}
}
 \right )
 \right )
 & \text{ if } 1 \in \left [ 2,n \right ] _{\mathbb{Z}}
\end{cases}
$$

The first term of the p-vector is just the p-value for the Bernoulli Distribution Test.
We mentioned that the Walsh-Hadamard Test is valid only for orders that are powers of two, so we chose the project to utilise sample sizes of only 32 and 64 - enough to justify using the central limit theorem for the p-vector formula.

We can turn the Walsh-Hadamard Test p-vector into a single metric by checking how closely a sample of values from a standard uniform distribution resembles the p-vector.
The following statistic gives a measure of uniformity of values in the p-vector:<br>
$$
u(p_{vector})=\left | 1-\frac{p'\cdot v}{p'\cdot p'} \right |
:
v=\left ( \frac{i}{n} \right )^{n}_{i=1}
$$

where $p'$ is the p-vector with the order of entries arranged from smallest to largest.

The closer the $u$ statistic is to zero, the better the standard uniform distribution fits the p-vector. Thus, it is more probable that the realised sample consists of identically distributed independent Bernoulli variates.

We derived the $u$ statistic by applying linear regression techniques to a Kolmogorov-Smirnov plot with the p-vector. 
The more the plot resembles the identity function, the better the standard uniform distribution fits the p-vector (the p-vector being the predictor variable).

## Multinomial Test Theory

The multinomial test is derived as follows.
There are four possibilities when tossing two coins, they are: **11**, **10**, **01**, and **00**, where **1** denotes a head, and **0** a tails.
To maintain the independence of the frequencies of these variables, the sum of these frequencies will be $n/2$, by considering the 1st and 2nd, the 3rd and 4th toss and so on.
For example, the sequence **1011** has 1 **10** and 1 **11** for the purpose of this test.

Under individual coin tosses having identical Bernoulli distributions as well as being independent, these 4 possibilities are distributed according to the multinomial distribution.
Allowing $p$ to represent the probability of head in an individual coin toss and $n$ the total number of tosses, we have:<br>
$$
\mathbb{P}(Y_1=y_1,
Y_2=y_2,
Y_3=y_3,
Y_4=y_4
)
=\frac{(n/2)!}{y_1!y_2!y_3!y_4!}
(p^2)^{y_1}
(p(1-p))^{y_2}
((1-p)p)^{y_3}
((1-p)^2)^{y_4}
$$

where $Y_1$, $Y_2$, $Y_3$, $Y_4$ are the random variables representing the number of **11**s, **10**s, **01**s and **00**s respectively.
We the formulate our hypotheses:
$$
\begin{matrix}
H_0: \text{for} \ i \in 
\lbrace
1,2,\dotso,n
\rbrace,
X_i\sim i.i.d(Bernoulli(p))
\\ 
H_1: \text{for} \ i \in 
\lbrace
1,2,\dotso,n
\rbrace,
X_i\nsim i.i.d(Bernoulli(p))
\end{matrix}
$$

We can then generate p-values using the multinomial test.
This test is applicable for this distribution since more 'extreme' values are those with lower probability. Define:
$$
Z=
\left\lbrace
\frac{(n/2)!}{y_1!y_2!y_3!y_4!}
(p^2)^{y_1}
(p(1-p))^{y_2}
((1-p)p)^{y_3}
((1-p)^2)^{y_4}
:
\displaystyle\sum\limits_{i=1}^4 z_i
=n/2
\wedge
z_1,
z_2,
z_3,
z_4
\in
\mathbb{N}_0
\right\rbrace
$$

Then, denoting $y=(y_1,y_2,y_3,y_4)$ as our observed vector, and $pr(y)$ as the probability of having $y$ as our observed value under the null hypothesis define:
$$
p_{value}=\displaystyle\sum\limits_{z \in Z,
z \leq pr(y)} z
$$

Note that for $p=0.5$, there is a more simple representation of the p-value, but this definition is used to encompass all possible values for $p$.

## Last Equalisation Test Theory

The Last Equalisation Test is derived as follows.
Another statistic we can look at is the last time in which the number of head and tail tosses are the same, or in the context of our binary sequence, the last term in which the number of **0**s and **1**s up to and including that term are equal.
For example, the sequence **100111** has its last equalisation on term 4.

Another perspective to take on the last equalisation is considering the $(X_i)^n_{i=1}$ as defined previously as a Markov Process.
However, in this context, it is more useful to assign a value 1 to a head toss and value -1 to a tails toss.
Then, we have a 1-dimensional random walk starting at the origin.
We can define:
$$
p_n(k):=
\mathbb{P}({
    \text{A binary sequence of length n having last equalisation at term k}
)}
$$

For the purpose of the test we will need to calculate the distribution of $p_{32}(k)$ and $p_{64}(k)$ but the general derivation for even $n$ will be given (with the distribution for $n$ and $n+1$ being equivalent for
even $n$, so the odd cases can be easily extracted). 
We note that for odd $k$, $p_n(k) = 0$ since on odd terms either the number of heads will be odd and the number of heads even, or vice versa. 
In either case, the number of heads and tails cannot be equal.
Next, we have that:
$$
p_n(n)=
\binom{n}{n/2}(p(1-p))^{n/2}
$$

This is because for the random walk to end back at the origin after all $n$ steps it is necessary and sufficient to have the same number of head and tail tosses.
We know, since there must be a last equalisation that for $k \geq 1$<
$$
\displaystyle\sum\limits_{i=0}^{n/2} p_n(2k)
=1
$$
and so
$$
p_n(0)=
1-\displaystyle\sum\limits_{i=1}^{n/2} p_n(2k)
$$
We also have that $p_n(2k) = p_{2k}(2k) \cdot p_{n−2k}(0)$ by the Markov Property. 
Using these two identities, we can get the distribution for the last equalisation. 
Our hypotheses remain the same in that the null hypothesis is that our sample consists of independently distributed Bernoulli variates. 
For $p= 1/2$ the distribution for the last equalisation is symmetric, so the p-values for the 2-sided test can be computed quite simply. 
However, for $p \neq 1/2$, we must utilise a different method to calculate our p-values.
We calculate them as follows:
$$
p_{value}=\displaystyle\sum\limits_{k=0,p_n(2k)\leq p_n(y)}^{n/2} p_n(2k)
$$
where $y$ is our observed value of the last equalisation.

# Evaluation & Conclusion

The final project app functions without errors; however, it takes significantly longer to calculate p-values for samples of length 64 than 32.
The excess processing stems from the calculation of the CDFs of the max run test, requiring a large number of computations to complete.
One can reduce the program computation time by deriving the exact formula for the $t$ coefficients, allowing for significantly faster calculations that way.
It would be ideal also to add time series methods to test the independence between sample entries, though time restrictions prevented the realisation of such implementation.
All in all, the project was successful.


# Appendix

The appendix is reserved for explaining the notation used in this post.

Shorthand set notation writes: $\left\lbrace a_1,a_2,\dotso, a_n \right\rbrace$ as $\left\lbrace a_i\right\rbrace_{i=1}^{n}$.

Shorthand vector notation writes: $\left( a_1,a_2,\dotso, a_n \right)$ as $ \left( a_i \right)_{i=1}^{n}$.

Shorthand integer interval writes: $\left\lbrace a,a+1,\dotso, b-1,b \right\rbrace \: a,b \in \mathbb{Z}$ as
$[a,b]_{\mathbb{Z}} = [a,b] \cap \mathbb{Z} = \left\lbrace i \right\rbrace_{i=a}^{b}$.

The $\Phi(x)$ function is the cdf of the standard normal distribution.

The $\mu(X)$ statistic's distribution is expressed with a multinomial coefficient, which can be written in terms of factorials as follows:
$$
\left(\begin{array}{c}n/k\\ z\end{array}\right)=(n/k)! 
\left(
\displaystyle\prod\limits_{i=1}^{2^k} z_i!
\right)^{-1}
$$

# Bibliography
1. I. Fazekas, Z. Karacsony, Z. Libor (2010), ‘Longest runs in coin tossing. Comparison of recursive formulae, asymptotic theorems, computer simulations’, *Acta Universitatis Sapientiae*, Mathematica, Vol 2, No. 2, 215-228

2. M. F. Schilling (1990), ‘Longest Run of Heads’, *The College Mathematics Journal*, Vol 21, Issue 3, 196-207

3. A. M. Mood (1940), ‘The Distribution Theory of Runs’, *Annals of Mathematical Statistics*, Vol 11, No. 4, 367-392

4. M. Bar-Hillel (1991), ‘The perception of randomness’, *Advances in Applied Mathematics*, Vol 12, Issue 4, 428-454

5. J. V. Bradley (1960), *Distribution-Free Statistical Tests*, Ohio, United States Air Force, 195-215

6. A. G. Oprina, A. Popescu, E. Simion, G. Simion (2009), ‘Walsh-Hadamard Randomness Test and New Methods of Test Results Integration’, *Bulletin of the Transilvania University of Brasov*, Series III, Vol 2, No. 51, 93-106

7. H. Liero, S. Zwanzig (2011), *Introduction to the Theory of Statistical Inference*, CRC Press, Taylor & Francis Group

8. T. Read, N. Cressie (1988), *Goodness-of-Fit Statistics for Discrete Multivariate Data*, Springer-Verlag

9. G. Casella, R. L. Berger (2002), *Statistical Inference, Second Edition*, Wadsworth Group, Duxbury, Thompson Learning Inc.


