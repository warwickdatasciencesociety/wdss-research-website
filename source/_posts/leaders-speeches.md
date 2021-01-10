---
title: "A Data-Driven Dive into UK Party Conference Leaders' Speeches"
date: 2021-01-04
updated: 2021-01-04
author: "Ewan Yeaxlee"
contact: "https://www.linkedin.com/in/ewan-yeaxlee-7b13a9181/"
tags:
- data-analysis
- visualization
- web-scraping
categories:
- [Computer Science, Natural Language Processing]
- [Social Sciences, Politics]
languages:
- r
description: "Wordclouds, sentiment, and scrabble scores. In this post, we analyse and visualisation a collection Leaders' speeches, using traditional and not-so-traditional text analysis techniques."
cover: /banners/leaders-speeches.jpg
---

{% note info %}
**Accessing Post Source**
We are still working on getting this site set up, so source code for this post is not yet available. Check back soon and you'll be able to find it linked here.
{% endnote %}
Party conferences are a mainstay in British politics whereby politicians, party members and affiliated people descend on a chosen city in order to set the party agenda, raise funds and attempt to get a soundbite into the mainstream media. The hallmark of these conferences are the Leaders' speeches, where the current head of the party aims to appeal to their party base or even attract some new voters through media coverage.

## Data Background

This analysis would not have been possible without the transcripts provided by [British Political Speech](http://www.britishpoliticalspeech.org/speech-archive.htm). They describe themselves as "an online archive of British political speech and a place for the discussion, analysis, and critical appreciation of political rhetoric" and produce speeches dating back to 1895.

For my study, I aim to observe the nuances of party conference leadership speeches from 2010 to 2018. These dates were chosen as they coincide with a change in the British political landscape, following the 2010 election whilst still providing us with enough data to conduct meaningful analysis. For this study, I will only observe the three 'mainstay' political parties: the Conservatives, the Labour Party and the Liberal Democrats.

Upon importing and tidying the data, we can observe the 5 most used words within the speeches.


<table>
<caption>A tibble: 5 × 2</caption>
<thead>
	<tr><th scope=col>Word</th><th scope=col>Count</th></tr>
	<tr><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;int&gt;</th></tr>
</thead>
<tbody>
	<tr><td>the</td><td>8777</td></tr>
	<tr><td>to </td><td>5279</td></tr>
	<tr><td>and</td><td>5033</td></tr>
	<tr><td>of </td><td>3898</td></tr>
	<tr><td>a  </td><td>3470</td></tr>
</tbody>
</table>



There are no surprises here. In fact, the top 5 most used words here are from the top 6 most used words in the English language according to the [Oxford English Corpus](https://enacademic.com/dic.nsf/enwiki/2822326), a text corpus comprising over 2 billion words.

Carrying on our analysis with these common words would create a dull analysis, so to counteract this, we will temporarily remove them. We do this using the `tidytext` package in R, which contains a comprehensive list of [stop words](https://rdrr.io/cran/tidytext/man/stop_words.html). These are common words in the English language which would add nothing to certain parts of our analysis if they were to be included. A separate dataframe was created to store the non-stopwords which totalled 56,989 words, meaning that 105,883 words were removed.
{% note info %}
It is worth noting, that there is no definitive list of stopwords. Instead, different words would be considered stopwords depending on the context, although we have just used a generic list for simplicity. We will see later in the post, a more nuanced way of handling uninformative words called TF-IDF.
{% endnote %}
We can now observe the most used 5 non-stopwords.


<table>
<caption>A tibble: 5 × 2</caption>
<thead>
	<tr><th scope=col>Word</th><th scope=col>Count</th></tr>
	<tr><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;int&gt;</th></tr>
</thead>
<tbody>
	<tr><td>people    </td><td>1207</td></tr>
	<tr><td>country   </td><td> 684</td></tr>
	<tr><td>government</td><td> 598</td></tr>
	<tr><td>party     </td><td> 577</td></tr>
	<tr><td>britain   </td><td> 568</td></tr>
</tbody>
</table>



This is more like what we would have expected the vocabulary of a Leader's speech to look like.

We can go further and visualise the set of each party's 100 most commonly used non-stopwords through wordclouds. This is done below in each party's traditional colour. (Blue for Conservative, Red for Labour, Yellow for Liberal Democrat).


![](/images/leaders-speeches/leaders-speeches_16_0.png)


We can see that the words identified to be most common before appear most often in these wordclouds too (denoted by their large size). The only visible differences are the party's names, particularly visible for both Labour and the Liberal Democrats. Here we see the obvious flaws in word clouds, they barely allow us to observe any differences between the parties and provide no numerical insight. We will aim to address this weakness later with different methods.

Before we dive into some more detailed text analysis, we could have a quick exploration of the word count for each Leader's speech.


![](/images/leaders-speeches/leaders-speeches_20_0.png)


From this, we can see that Ed Miliband can be quite the rambler at times.

## Text Analysis

### Analysing Sentiment

Basic counts and summaries are great, but with modern data science techniques, we can go much further. For example, we can infer the sentiment (loosely, how positive or negative in tone) each speech is.

We do this by referencing the contents of each speech against the AFINN lexicon, created by Finn Arup Neilson. This lexicon assigns an integer value from -5 to 5 to a vast number English words with negative numbers indicating negative sentiment and positive numbers indicating positive sentiment. Here we list a random word for each sentiment value.


<table>
<caption>A grouped_df: 11 × 2</caption>
<thead>
	<tr><th scope=col>Word</th><th scope=col>Value</th></tr>
	<tr><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>son-of-a-bitch</td><td>-5</td></tr>
	<tr><td>fraudulence   </td><td>-4</td></tr>
	<tr><td>lunatics      </td><td>-3</td></tr>
	<tr><td>lethargy      </td><td>-2</td></tr>
	<tr><td>manipulation  </td><td>-1</td></tr>
	<tr><td>some kind     </td><td> 0</td></tr>
	<tr><td>cool          </td><td> 1</td></tr>
	<tr><td>courtesy      </td><td> 2</td></tr>
	<tr><td>cheery        </td><td> 3</td></tr>
	<tr><td>winner        </td><td> 4</td></tr>
	<tr><td>superb        </td><td> 5</td></tr>
</tbody>
</table>



We can then take an average of the sentiments over all word in each speech and visualise it to see the trend of speech sentiment over time. This is conducted on the dataset with stopwords included, otherwise it could distort the sentiment (though note that most stopwords have a neutral sentiment).


![](/images/leaders-speeches/leaders-speeches_28_0.png)


As we can see, the speeches are overwhelmingly positive, with the only negative score being Jeremy Corbyn's 2018 speech to the Labour Party conference. Other notable values include David Cameron's consistency between 2010 and 2015 for the Conservative Party and the significant jump in positivity when Theresa May took over the Conservative Leadership in 2016.

### Term Frequency and Zipf's Law

We have seen that raw word counts on their own aren't particularly useful. One flaw of many is that longer texts will naturally have higher word counts for all words. Instead, a more useful metric is how often a certain word (also called a term) appears as a proportion of all words. This is known as _term frequency_ and defined as

$$\text{Term Frequency} = \frac{\#\{\text{Occurrences of Term}\}}{\#\{\text{Occurrences of All Words}\}}$$

So that we can compare across parties, we will look at term frequencies as a proportion of the occurrences of each term in all speeches by the party the term came from. We start by looking at the distribution of term frequencies for each party.


![](/images/leaders-speeches/leaders-speeches_35_0.png)

{% note warning %}
It should be noted that there are longer tails for these graphs that have not been shown. Instead, we have truncated the the really popular words such as 'the', 'and' and 'to' to make it easier to see the main body of the plot.
{% endnote %}
The plots all display a similar distribution for each party with many 'rare' words and fewer popular words.

It turns out that these long-tailed distributions are common in almost every occurrence of natural language. In fact, George Zipf, a 20th century American linguist created _Zipf's law_. This formalises the above observation, stating that the frequency that a word appears in a text is inversely proportional to its rank.

$$
\text{Term Frequency} \propto \frac{1}{\text{Rank}}
$$

Put simply, the most frequent word will appear at twice the rate of the second most frequent word and at three times that of the third most frequent word. 

Zipf's law is largely accurate for many natural languages, including English (though as always, there are exceptions). For example, in the Brown Corpus of American English text, which contains slightly over 1 million words: 'the' appears the most times at ~70000 times, 'of' the second most at ~36000 times and 'and' the third most at ~29000, as would be roughly expected according to Zipf's law.

We can attempt to visualise this law for our own text by plotting rank on the x-axis and term frequency on the y-axis, both on log scales.
{% note info %}
**Why the logs?**
By definition, if two values $x$ and $y$ are inversely proportional, then we can find a constant $a$ such that $y = \frac{a}{x}$. Taking logarithms and rearranging gives $\log(y) = log(a) - log(x)$. In other words, $x$ and $y$ are inversely proportional if and only if their logarithms lie on a straight line with a negative slope.
{% endnote %}

![](/images/leaders-speeches/leaders-speeches_41_0.png)


We can see that all three parties have similar text structures largely obey Zipf's Law. That said, we can see that our curve deviates from a straight line at the lower rank tail, suggesting that the most popular words in the speeches are being used more often than they would in a natural language. Additionally, we would expect a slope of approximately $-1$; by fitting a linear model (shown in grey), we obtain a coefficient which is close to this value.

### TF-IDF Analysis

We've seen that we can use a list of stop words to filter our data to leave only meaningful words. However, this list is fixed and not linked to our data in any way. We've already seen that 'people' is used very commonly in our speeches and so doesn't provide that meaningful of an insight to us. Could construct a value that helped us to see the relative frequency of a term among our speeches, in order to see how important a word is to a specific speech compared to the others?

We can indeed. In fact the work has already been done for us in the form of a value value called the TF-IDF. It is calculated by multiplying the term frequency (TF) from earlier by a new value called the inverse document frequency (IDF).

$$TF\cdot{IDF} = \left(\frac{\#\{\text{Occurrences of Term}\}}{\#\{\text{Occurrences of All Words}\}}\right) \cdot \log \left(\frac{\#\{\text{Documents}\}}{\#\{\text{Documents Containing Term}\}}\right)$$

Loosely speaking, TF-IDF asks two questions:
- Is the specific term used more than expected in a given speech?
- Is it rare for a speech to contain a the specific term?
If the answer to both of these questions is "yes", then TF-IDF is large, an the term is considered to be relatively important.

We can calculate the TF-IDF score for each word in each speech before using these to find the most 'important' word in each speech.


<table>
<caption>A grouped_df: 9 × 4</caption>
<thead>
	<tr><th scope=col>year</th><th scope=col>Conservative</th><th scope=col>Labour</th><th scope=col>Liberal Democrat</th></tr>
	<tr><th scope=col>&lt;int&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th></tr>
</thead>
<tbody>
	<tr><td>2010</td><td>harry    </td><td>recognises </td><td>plural </td></tr>
	<tr><td>2011</td><td>euro     </td><td>bargain    </td><td>barons </td></tr>
	<tr><td>2012</td><td>rise     </td><td>succeeded  </td><td>maurice</td></tr>
	<tr><td>2013</td><td>finish   </td><td>race       </td><td>liberal</td></tr>
	<tr><td>2014</td><td>40p      </td><td>ethic      </td><td>dems   </td></tr>
	<tr><td>2015</td><td>extremism</td><td>kinder     </td><td>liberal</td></tr>
	<tr><td>2016</td><td>plays    </td><td>migrants   </td><td>brexit </td></tr>
	<tr><td>2017</td><td>dream    </td><td>grenfell   </td><td>brexit </td></tr>
	<tr><td>2018</td><td>proposal </td><td>palestinian</td><td>brexit </td></tr>
</tbody>
</table>



We obtain some interesting results here. For example, it's clear to see the Liberal Democrats' sharp pivot to a anti-Brexit strategy following the referendum of 2016. Or how in 2014, the Conservatives announced their plan to increase the 40% income tax threshold (known as the 40p tax rate). We also see Jeremy Corbyn's plan for a 'kinder' politics emerge in his first conference speech as leader in 2015, alongside the Grenfell Tower disaster mentioned in 2017.

The names such as 'Harry' and 'Maurice' that crop up here were intriguing at first glance. These were in reference to 'Harry Beckough' and 'Maurice Reeves', who were, respectively, a longstanding Conservative member and a furniture shop owner whose premises was burned to the ground during the London riots.

### Complexity Consideration

There are a number of ways that we can observe the complexity of a text, or in this case a speech. For this piece we choose the average number of syllables per word. The data for this was taken from the `quanteda` package and we can visualise the results as so.


![](/images/leaders-speeches/leaders-speeches_54_0.png)


We can see profound variations between different leaders in this plot. Ed Miliband and David Cameron, the leaders of Labour and the Conservatives who gave speeches between 2010-2014 and 2010-2015, respectively, had a much lower complexity than the most recent leaders such as Jeremy Corbyn of Labour and Vince Cable of the Liberal Democrats, who together count for the top 6 most complex speeches.
{% note success %}
We used mean syllable count in this piece as a metric for speech complexity as it is simple for a layperson to understand. That said, there are many more subtle and interesting complexity measures available through `quanteda`, such as the Flesch–Kincaid readability score.
{% endnote %}
### A Different Way of Deciding Elections?

The [First Past the Post system](https://www.electoral-reform.org.uk/voting-systems/types-of-voting-system/first-past-the-post/) is often bemoaned in the UK as being unsuitable for modern-day politics. Now, it is not my place to comment on this system but if pushed to suggest another system, the aforementioned `Quanteda` package does give us another option...

We can calculate the mean scrabble score per word of the leader's party conference speech each year! First let us observe the most impressive efforts that the politicians managed:


<table>
<caption>A tibble: 5 × 5</caption>
<thead>
	<tr><th scope=col>Party</th><th scope=col>Year</th><th scope=col>Leader</th><th scope=col>Word</th><th scope=col>Scrabble Score</th></tr>
	<tr><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>Conservative    </td><td>2018</td><td>Theresa May  </td><td>czechoslovakia </td><td>37</td></tr>
	<tr><td>Liberal Democrat</td><td>2013</td><td>Nick Clegg   </td><td>unequivocally  </td><td>30</td></tr>
	<tr><td>Labour          </td><td>2017</td><td>Jeremy Corbyn</td><td>overwhelmingly </td><td>29</td></tr>
	<tr><td>Labour          </td><td>2017</td><td>Jeremy Corbyn</td><td>democratization</td><td>29</td></tr>
	<tr><td>Labour          </td><td>2015</td><td>Jeremy Corbyn</td><td>fizzing        </td><td>29</td></tr>
</tbody>
</table>



Theresa May managed an incredible score of 37 in 2018 with 'Czechoslovakia' but this would of course be disqualified for being a proper noun. As a result, Nick Clegg holds the record with 30 points scored for 'unequivocally'! We can also visualise the mean score per word as follows.


![](/images/leaders-speeches/leaders-speeches_60_0.png)


As we can see, the Conservatives, who have been in power since 2010 would not win a single year should it be decided by Scrabble. In fact, the Liberal Democrats would win 6 out of the 9 years we have studied with Labour, under Jeremy Corbyn, taking the other 3 years—I'm sure both parties would be happy with that in hindsight!

Just in case anyone was under any illusion, of course mean Scrabble score is a poor way of deciding elections and I am not endorsing its use—at the very least, a game of Pictionary would be more appropriate...

## Takeaways

With that, I end my brief incursion into British political speeches. While I have barely begun to scratch the surface of Natural Language Processing (NLP) methods, I hope that I have shown the power of the ways that these techniques can be used to summarise large pieces of text through sentiment, TF-IDF and syllable complexity. 

I had minimal experience with NLP methods upon embarking on this project and would like to thank WDSS (in particular, Janique Krasnowska) for supporting me until completion. I feel like I've learned a lot and certainly furthered my knowledge and experience. I would suggest anyone who would like to conduct some data science studies outside their degree looks out for research opportunites with WDSS and seizes them with both hands—I will certainly be looking out for more chances!

## Appendix: Summary Table of All Speech Metrics


<table>
<caption>A tibble: 27 × 8</caption>
<thead>
	<tr><th scope=col>Party</th><th scope=col>Year</th><th scope=col>Leader</th><th scope=col>Number of Words</th><th scope=col>Mean Sentiment</th><th scope=col>Top TF-IDF Word</th><th scope=col>Mean Word Syllables</th><th scope=col>Mean Scrabble Score</th></tr>
	<tr><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;int&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;chr&gt;</th><th scope=col>&lt;dbl&gt;</th><th scope=col>&lt;dbl&gt;</th></tr>
</thead>
<tbody>
	<tr><td>Conservative    </td><td>2010</td><td>David Cameron</td><td>6247</td><td> 0.38866397</td><td>harry      </td><td>1.439020</td><td>7.435761</td></tr>
	<tr><td>Conservative    </td><td>2011</td><td>David Cameron</td><td>6132</td><td> 0.40983607</td><td>euro       </td><td>1.450808</td><td>7.538034</td></tr>
	<tr><td>Conservative    </td><td>2012</td><td>David Cameron</td><td>6070</td><td> 0.47016706</td><td>rise       </td><td>1.403032</td><td>7.367087</td></tr>
	<tr><td>Conservative    </td><td>2013</td><td>David Cameron</td><td>5917</td><td> 0.45477387</td><td>finish     </td><td>1.400913</td><td>7.401018</td></tr>
	<tr><td>Conservative    </td><td>2014</td><td>David Cameron</td><td>6104</td><td> 0.49638554</td><td>40p        </td><td>1.378480</td><td>7.304463</td></tr>
	<tr><td>Conservative    </td><td>2015</td><td>David Cameron</td><td>6676</td><td> 0.45546559</td><td>extremism  </td><td>1.443745</td><td>7.463356</td></tr>
	<tr><td>Conservative    </td><td>2016</td><td>Theresa May  </td><td>7187</td><td> 0.88888889</td><td>plays      </td><td>1.476137</td><td>7.568521</td></tr>
	<tr><td>Conservative    </td><td>2017</td><td>Theresa May  </td><td>7113</td><td> 0.63288719</td><td>dream      </td><td>1.485799</td><td>7.432207</td></tr>
	<tr><td>Conservative    </td><td>2018</td><td>Theresa May  </td><td>7120</td><td> 0.54709419</td><td>proposal   </td><td>1.483296</td><td>7.571831</td></tr>
	<tr><td>Labour          </td><td>2010</td><td>Ed Miliband  </td><td>6168</td><td> 0.40265487</td><td>recognises </td><td>1.480791</td><td>7.348780</td></tr>
	<tr><td>Labour          </td><td>2011</td><td>Ed Miliband  </td><td>5891</td><td> 0.56207675</td><td>bargain    </td><td>1.393482</td><td>7.288363</td></tr>
	<tr><td>Labour          </td><td>2012</td><td>Ed Miliband  </td><td>7390</td><td> 0.40898345</td><td>succeeded  </td><td>1.388167</td><td>7.134647</td></tr>
	<tr><td>Labour          </td><td>2013</td><td>Ed Miliband  </td><td>7954</td><td> 0.74186992</td><td>race       </td><td>1.370724</td><td>7.068717</td></tr>
	<tr><td>Labour          </td><td>2014</td><td>Ed Miliband  </td><td>5697</td><td> 0.79874214</td><td>ethic      </td><td>1.437664</td><td>7.322393</td></tr>
	<tr><td>Labour          </td><td>2015</td><td>Jeremy Corbyn</td><td>7178</td><td> 0.47313692</td><td>kinder     </td><td>1.530257</td><td>7.609025</td></tr>
	<tr><td>Labour          </td><td>2016</td><td>Jeremy Corbyn</td><td>5894</td><td> 0.43455497</td><td>migrants   </td><td>1.569805</td><td>7.809402</td></tr>
	<tr><td>Labour          </td><td>2017</td><td>Jeremy Corbyn</td><td>5965</td><td> 0.08439898</td><td>grenfell   </td><td>1.585235</td><td>7.864050</td></tr>
	<tr><td>Labour          </td><td>2018</td><td>Jeremy Corbyn</td><td>5703</td><td>-0.04136253</td><td>palestinian</td><td>1.564188</td><td>7.706432</td></tr>
	<tr><td>Liberal Democrat</td><td>2010</td><td>Nick Clegg   </td><td>4354</td><td> 0.16060606</td><td>plural     </td><td>1.457425</td><td>7.571065</td></tr>
	<tr><td>Liberal Democrat</td><td>2011</td><td>Nick Clegg   </td><td>4257</td><td> 0.06571429</td><td>barons     </td><td>1.471583</td><td>7.604947</td></tr>
	<tr><td>Liberal Democrat</td><td>2012</td><td>Nick Clegg   </td><td>4328</td><td> 0.33333333</td><td>maurice    </td><td>1.468837</td><td>7.439471</td></tr>
	<tr><td>Liberal Democrat</td><td>2013</td><td>Nick Clegg   </td><td>5927</td><td> 0.49206349</td><td>liberal    </td><td>1.475379</td><td>7.538670</td></tr>
	<tr><td>Liberal Democrat</td><td>2014</td><td>Nick Clegg   </td><td>6241</td><td> 0.33682008</td><td>dems       </td><td>1.494074</td><td>7.640180</td></tr>
	<tr><td>Liberal Democrat</td><td>2015</td><td>Tim Farron   </td><td>5804</td><td> 0.12616822</td><td>liberal    </td><td>1.462427</td><td>7.327490</td></tr>
	<tr><td>Liberal Democrat</td><td>2016</td><td>Tim Farron   </td><td>6178</td><td> 0.21428571</td><td>brexit     </td><td>1.454840</td><td>7.391953</td></tr>
	<tr><td>Liberal Democrat</td><td>2017</td><td>Vince Cable  </td><td>5139</td><td> 0.20505618</td><td>brexit     </td><td>1.574762</td><td>7.818679</td></tr>
	<tr><td>Liberal Democrat</td><td>2018</td><td>Vince Cable  </td><td>4364</td><td> 0.08626198</td><td>brexit     </td><td>1.544255</td><td>7.863584</td></tr>
</tbody>
</table>


