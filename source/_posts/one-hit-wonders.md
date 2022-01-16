---
title: "One-Hit Wonders"
date: 2022-01-16
updated: 2021-01-16
authors_plus:
- "Aahdi Samarasekara"
- "Marcell Ötvös"
contacts_plus:
- "https://www.linkedin.com/in/wedagesamarasekara"
- "https://www.linkedin.com/in/marcell-ötvös-5a64b020b/"
editor: "Keeley Ruane"
editor_contact: "https://www.linkedin.com/in/keeley-ruane-6aab4219b/"
tags:
- data-analysis
- visualization
- web-scraping
categories:
- [Humanities, Sociology]
languages:
- python
- r
description: "According to Wikipedia, a one-hit wonder is any entity that achieves mainstream popularity, often for only one piece of work, and becomes known among the general public solely for that momentary success. In this project we use the publicly available data from Spotify to find artists in the music industry who can be regarded as one-hit wonders."
cover: /banners/one-hit-wonders.jpg
---

## Introduction 

We have all heard the expression of a "one-hit wonder,” but what is it exactly? Wikipedia sums it up perfectly: "[A] "one-hit wonder" is any entity that achieves mainstream popularity, often for only one piece of work, and becomes known among the general public solely for that momentary success.” Our research regards, examines and presents some of the biggest "one-hit wonders" over the last few decades. For the purposes of this experiment, we have declared an artist a one-hit wonder based upon the number of their Spotify streams.

## Methodology 

We collected data from Spotify via the Spotify API for 20 famous artists who could most likely be considered as “one-hit wonders.” The collected data includes the five most streamed songs of each artist, the number of Spotify streams of each song, and the date and the audio features of the two most streamed songs of each artist. The audio features include different characteristics, such as: "dance-ability," loudness, or tempo. This research will be presented via various sections which aim to enlighten certain aspects of these artists and their songs.
The first section is intending to show that these artists are, indeed, "one-hit wonders."

## Data Analysis


![](/images/one-hit-wonders/one-hit-wonders_3_0.png)


As displayed above, the plot compares the number of Spotify streams of the first and second most popular songs of 10 of the selected artists. Huge differences can be seen for each occasion as none of these artist have ever come close to the success of their biggest hit.


![](/images/one-hit-wonders/one-hit-wonders_5_0.png)


Next, we ranked the five most popular songs of every artist, and then averaged the number of Spotify streams of each rank (which is shown in the next plot). The first ranked songs averaged close to 200 million streams while the second ranked songs stayed below 25 million. 3rd to the 5th ranked songs lag far behind this number. This plot further reinforces that these artist had only one outstanding performance over their career.

We tried to investigate whether there is a difference in the number of "one-hit wonder" artists over the decades, particularly between 1969 and 2000 - the date of the oldest and newest "one-hit wonders" in our research.


![](/images/one-hit-wonders/one-hit-wonders_7_0.png)


We can see that there is not a strong correlation regarding the distribution of such artists over time. While the relatively small number of data can also have an effect upon this result, the obvious explanation is that the prevalence of "one-hit wonders" does not depend on the era as there were, and will always be, such performers.

We may have the assumption that "one-hit wonder" artists generally release their biggest hit early in their career and then they try to recreate it, typically without success. Hence, we checked whether the second most popular songs usually came later than the most popular songs or not.


![](/images/one-hit-wonders/one-hit-wonders_9_0.png)


The plot above lightly supports this claim. The straight line is a y=x line, where y and x are the date of the second most and the most popular songs respectively. We can see that more points are above the line than below, which means that the big hits were most likely to be followed by the second biggest hit rather than vice versa. After we fitted a linear model, we can see that the representative plot line is above the straight line, so the general trend is what we expected.

We investigated the audio features of the songs to figure out why the famous songs became famous and, alteratively, why the other songs of the particular artist didn’t. We compared the audio features of the two most popular songs of each artist, expecting that one feature, i.e.: "dance-ability" will be generally higher for the most popular one than the second most popular one. Surprisingly, we rarely found such patterns.


![](/images/one-hit-wonders/one-hit-wonders_12_0.png)



![](/images/one-hit-wonders/one-hit-wonders_13_0.png)


The closest we got to this hypothesis were in regards to the "liveness" and the "dance-ability" of the songs, of which the most popular ones increasingly had higher scores than the second most popular ones, as seen above. However, the trend is not so strong here, and pure luck could have had an effect. So, it seems that none of the audio features explain the reason behind their success.

Finally, we examined the extent to which each "one-hit wonder" artist technically is a "one-hit wonder," which was a value we got by dividing the Spotify stream count of the most popular songs by the stream count of the second most popular songs from each artist.


![](/images/one-hit-wonders/one-hit-wonders_15_0.png)


As we can see, Norman Greenbaum is a real "one-hit wonder," with a stream count more than 850 times higher for his biggest hit than for his second biggest hit. On the other hand, Billy Paul or Vanilla Ice had other songs which were relatively popular.

## Conclusions

We hope that our project demonstrated some interesting characteristics of 20 of the most famous "one-hit wonder" artists. While most of these artists are not currently active, some of them are, and they may produce another hit and then successfully erase the title “one-hit wonder” from themselves, hence resign their place from our list.
