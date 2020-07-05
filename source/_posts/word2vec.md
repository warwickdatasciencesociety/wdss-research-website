---
title: "Word2Vec: Arithmetic with Words"
date: 2020-07-05
updated: 2020-07-05
author: "Pratyush Ravishankar"
contact: "https://www.linkedin.com/in/pratyush-ravishankar-a5391615a/"
tags:
- lesson
- word-embedding
categories:
- [Computer Science, Natural Language Processing]
languages:
- Python
description: "From a young age we build familarity with the rules for adding and subtracting numbers to and from one another, but how could we go about performing arithmetic with words?"
cover: /banners/word2vec.jpg
---
{% note info %}
**Accessing Post Source**
We are still working on getting this site set up, so source code for this post is not yet available. Check back soon and you'll be able to find it linked here.
{% endnote %}
Unsurprisingly, human language seem intuitive to humans, but that is not the case for a computer. On the other hand, though we can easily determine whether two words share a similar meaning, if asked to give a quantitative reason as to why that is the case, we will may struggle to reach a satisfying answer. Thankfully, our shortcoming is where computers thrive, as they are remarkably good with numbers and tabular data. All this leaves us to do is to translate our problem into such a numeric system. Word embedding is a technique to take language and transform it into this computer-friendly format so we can take advantage of computing power for solving natural language processing tasks.

## Background

### The Need for Word2vec

Initial attempts at solving this problem before word embeddings included one-hot encoding. The essence of this process is to represent our text as a sequence of vectors in a space with number of dimensions equal to the number of words in our corpus. We assign each word its own dimension so that each word vector is orthogonal to the others. Technical details aside, this isn't practical to model anything on the scale of human languages, as the vector dimensions would be the size of the language (and as a results, storage and computational requirements would be astronomical). More importantly, however, this doesn't capture any sort of similarity between two words (since ever vector is mutually orthogonal to the others). As far as this method is concerned, the words 'dolphin' and 'neoliberal' are equally similar to 'shark'. Word2vec aims to solve this problem by providing word embedding which take into account relations between words. In essence, word2vec provides a canvas (albeit a strange multi-dimensional one) where any possible word in the language could lie, and plots points on this canvas for each word in our corpus. How close any two points on this canvas lie (captured mathematically by the cosine distance) should therefore correspond to how likely humans are to describe the respresented words as "similar".


![](/images/word2vec/word2vec_6_0.png)


### Deriving the Word Embeddings

To derive each word embedding, the word2vec model is usually trained using a method called Skipgram with Negative Sampling (SGNS). Essentially, a large corpus (typically billions of words) is fed to the model, and an $n$-sized sliding window is used to capture the words that lie either side of each word in the corpus to determine each word's context. The context for each word is then used to determine the word's embedding vector, with the negative sampling process controlling the rate at which these weights are updated to reduce computation time and produce a more robust result. Because words with a similar context usually have closely-linked meanings, such words will end up having similar embedding vectors too.

![The sliding window used in word2vec training](/images/word2vec/sliding_window.png)
Take the above diagram as an example. On iteration $j$ and $k$, 'fox' and 'bear' have similar contexts, so will end up with relatively close embedding vectors. After many adjustments each time they are found in the corpus, their vectors will provide an increasingly accurate represention of the "fox" and "bear" relation—types of animals. 

## Application
{% note info %}
The following examples are derived from a word2vec model trained on the [Google News dataset](https://code.google.com/archive/p/word2vec/), featuring over 100 billion words taken from various news articles. The trained model is stored an object called `model` which we can query for results.
{% endnote %}
Once we have trained a word embedding using word2vec, we can apply it in many different ways to extract the relationships between words in the corpus.

For example, we can find the similarity between words based on their cosine distance in the vector space. 


```python
model.similarity('queen', 'throne')
```




    0.45448625




```python
model.similarity('queen', 'forklift')
```




    -0.030027825




```python
model.similarity('Queen', 'Bowie')
```




    0.20833209


{% note warning %}
Since we are measuring similarity using the cosine distance, values will range from -1 to 1. Words with a similarity near 1 are likely to be extremely similar, words with a similarity of 0 have little in common, and words with similarity near -1 _should_ be opposites (though we'll later see that this doesn't always work)
{% endnote %}
As expected, the word 'forklift' is relatively distinct from 'queen', especially when compared to 'throne'. What's fascinating, however, is that multiple facets of the word 'queen' are captured; we see that 'Bowie' is also relatively close to 'Queen' due to the word's relation to the iconic rock band.

Naturally, with vectors come mathematical operations, and the real power of word2vec starts to emerge. Vector differences are the crux behind *analogies*, a concept best explained through examples...


### Analogies

#### Starting With a Classic

The most infamous example of the use of word2vec is answering the question, "Man is to woman, as king is to...what?". As we can see, word2vec takes this puzzle in it's stride.


```python
# king + (woman - man) = ...
print_similar(model.most_similar(positive=['king', 'woman'], negative=['man'], topn=1))
```

    queen (0.712)


This example is rather intuitive; the female version of the male title 'king' is 'queen' and so this is the natural choice to complete the analogy. To get word2vec to return this result, we have to phrase the question in the language of arthimetic; that is, `king + (woman - man)`. In other words, we are taking the word 'king' and asking what the corresponding word would be if added the difference between 'woman' and 'man'. This may seem unituitive—why can't we just add 'woman' to 'king'? The reason for this is that the word 'king' already has 'man' as a component of its vector representation. Therefore, if we simply added 'woman' without first subtracting 'man' we end up with components of both 'woman' and 'man' which confuses the model, leaving us with nonsensical results.


```python
# Invalid approach: king + woman = ...
print_similar(model.most_similar(positive=['king', 'woman'], topn=1))
```

    man (0.663)


### Plurals

We can use this system of analogy solving for finding the singular and plural forms of words. With a rather mundane example such as `gloves + (bike - bikes)`, it's not unsurprising the model returns 'glove'; it could simply be obtained from deciphering that the pattern is removing the trailing 's'—hardly groundbreaking. But when talking about irregular plurals, the required task to output the derived word shifts from spotting a simple pattern to seemingly needing a human-like understanding of the structure and complexities of the English language. Never-the-less, word2vec is up for the challenge.


```python
# foot + (cacti - cactus) = ...
print_similar(model.most_similar(positive=['foot', 'cacti'], negative=['cactus'], topn=1))
```

    feet (0.568)



```python
# child + (sheep - sheep) = ...
print_similar(model.most_similar(positive=['child', 'sheep'], negative=['sheep'], topn=1))
```

    children (0.726)


Here, 'sheep' is both the singular and the plural, meaning the result of the word arithmetic is still 'child'. But since 'child' is such a similar word to 'children', word2vec still manages to come out with the correct answer.

### Geographical analogies

We can use analogies to find cities.


```python
# Portugal + (Moscow - Russia) = ...
print_similar(model.most_similar(positive=['Portugal', 'Moscow'], negative=['Russia'], topn=1))
```

    Lisbon (0.655)


Or we can flip things around to find what country a city resides in.


```python
# Delhi + (Spain - Barcelona) = ...
print_similar(model.most_similar(positive=['Delhi', 'Spain'], negative=['Barcelona'], topn=1))
```

    India (0.626)


Finally, we can go one step up and find the geographic regions of countries.


```python
# Cambodia + (Africa - Egypt) = ...
print_similar(model.most_similar(positive=['Cambodia', 'Africa'], negative=['Egypt'], topn=1))
```

    Southeast_Asia (0.566)


The geographic intelligence of word2vec isn't limited to the form of analogy. Here we see an example in which we perform straight addition.


```python
# Iran + war = ...
print_similar(model.most_similar(positive=['Iran', 'war'],topn=3))
```

    Iraq (0.683)
    Islamic_republic (0.671)
    Syria (0.653)


This example shows how much geographic and political complexity is captured in the model. 'Iraq' and 'Islamic_republic' are most likely referencing the Iran-Iraq war. On the other hand Iraq and Syria, are both war-stricken countries near Iran, which could easily explain this relation.

### Opposites


When a word has a clear opposite, we can use analogy to find it.


```python
# high + (big - small)
print_similar(model.most_similar(positive=['high', 'big'], negative=['small'], topn=1))
```

    low (0.448)


Note however that we can't just negate a word to find its opposite or we obtain gibberish in return.


```python
# -high
print_similar(model.most_similar(negative=['high'], topn=1))
```

    ----------_-----------------------------------------------_GS## (0.321)


The reason for this is that an opposite word in a vector space has to be opposite in every way. Even though we would say that 'high' and 'low' are opposites, they do in fact have components in common, such as how they both represent heights. For that reason the model stubbornly ignores words that are opposites in the way we intend, and instead, tries to find the word that is most dissimilar to 'high', resulting in some strange garble of characters.

### Vector Sums and Differences

As hinted at before, word2vec can solve problems far more general than analogies. Here we look at some examples of generic vector sums and differences.


```python
# death + water = ...
print_similar(model.most_similar(positive=['death', 'water'], topn=3))
```

    drowning (0.556)
    drowing (0.545)
    scalding_bath (0.526)

{% note info %}
It appears that the second most similar term has picked up on a common typo of 'drowning'. The joys of real world data...
{% endnote %}

```python
# death + knife = ...
print_similar(model.most_similar(positive=['death', 'knife'], topn=3))
```

    kitchen_knife (0.644)
    stabbing (0.637)
    murder (0.634)



```python
# girlfriend - love = ...
print_similar(model.most_similar(positive=['girlfriend'], negative=['love'], topn=3))
```

    ex_girlfriend (0.517)
    fiancee (0.479)
    estranged_wife (0.476)


The second result is rather strange. If you have a theory of where this relation might have come from, make sure to comment below.


```python
# colleague + love = ...
print_similar(model.most_similar(positive=['colleage', 'love'], topn=3))
```

    loved (0.580)
    friend (0.551)
    pal (0.542)


With the last example we can see a shortcoming of the word2vec model. It appears that 'love' has a much stronger vector representation than 'collegue'; that is, the term captures more complexity, which makes sense. For this reason, the term 'love' can overpower the sum so that a word similar to 'love', 'loved' can be returned as highly similar even though it doesn't relate much to the word 'collegue'. Despite this, the other two preditions are strong.

### Miscellaneous 

To wrap up our examples, we will look at some miscellaneous analogies involving people and places.


```python
# Obama + (Russia - USA) = ...
print_similar(model.most_similar(positive=['Obama', 'Russia'], negative=['USA'], topn=3))
```

    Medvedev (0.674)
    Putin (0.647)
    Kremlin (0.617)



```python
# UK + (Hitler - Germany) = ...
print_similar(model.most_similar(positive=['UK', 'Hitler'], negative=['Germany'], topn=3))
```

    Tony_Blair (0.522)
    Oliver_Cromwell (0.509)
    Maggie_Thatcher (0.506)


Make of the above what you will...


```python
# Apple + (Gates - Microsoft) = ...
print_similar(model.most_similar(positive=['Apple', 'Gates'], negative=['Microsoft'], topn=1))               
```

    Steve_Jobs (0.523)



```python
# Victoria Beckham + (Barack Obama - Michelle) = ...
print_similar(model.most_similar(positive=['Victoria_Beckham', 'Barack_Obama'], negative=['Michelle'], topn=1))
```

    David_Beckham (0.528)



```python
# Manchester + (Anfield - Liverpool) = ...
print_similar(model.most_similar(positive=['Manchester', 'Anfield'], negative=['Liverpool'], topn=1))
```

    Old_Trafford (0.765)


## Word2Vec in the Wild

Above, we have seen some fairly isolated applications of the word2vec model, but that is not to say that there are not wider reaching use cases. For example, word2vec is often a key step in the production of sentiment analysis models (See: [a WDSS virtual talk on the use of sentiment analysis for predicting presidential approval](https://youtu.be/l40-JFn6F9M?t=1845)), recommender systems, and chat bots. Aside from these ecommerce-centric examples, word2vec has also flurished in scientific applications such as BioNLP, which have utilised word embeddings for advancements in knowledge.

Hopefully, through these examples, the potential power of Word2Vec has been made clear. Thank you reading.
