---
title: "Higher or Lower: Reinventing a Classic Card Game"
date: 2020-06-27
updated: 2020-06-27
author: "Parth Devalia"
contact: "https://www.linkedin.com/in/parthdevalia/"
tags:
- shiny
- web-scraping
- game
categories:
- [Computer Science, Web]
languages:
- python
- r
description: "How well do you know your celebs? This post discusses a web app developed collaboratively with WDSS members to test just this. Have a play and then learn how it was made."
cover: /banners/higher-or-lower.jpg
---
{% note info %}
This post is the corresponding write-up for a WDSS project in which a small team of society members collaborated to produce a web-toy that plays a game of Higher or Lower using the Twitter follower counts of celebrities. You can play this game at [this link](https://shiny.warwickdatascience.com/higher-or-lower/).
{% endnote %}
## Motivation

Sometimes, simplicity is beautiful. Higher or Lower is a game embodying this philosophy. Played solo with a standard deck of cards, play consists of revealing these one at a time after first guessing whether the next card will have a higher or lower value. In recent years, this game has been re-envisioned as a [popular web toy](http://www.higherlowergame.com/), in which card values are replaced by the number of global monthly Google searches for various topics. Not wishing to limit ourselves to search results, we decided to implement our own online version of the classic game based on the follower counts of Twitter celebrities. The final app can be found at the link above, and we will spend the rest of this post looking into the techniques behind our approach as well as reviewing the lessons this project can teach us about collaborative data science at WDSS.

For our purposes, this project is an ideal medium to practise web scraping and creating sharable products for others to enjoy. Web scraping is a way of extracting data from websites, leveraging automation to gather information efficiently and without unnecessary repetition.  In all, three members of WDSS worked on this project, combining their specific skills to develop the final product. [Tim Hargreaves](https://www.linkedin.com/in/tim-hargreaves/), focused on the backbone of the app, [Matthew Bardsley](https://www.linkedin.com/in/mhbardsley/), the visuals of the game, and I ([Parth Devalia](https://www.linkedin.com/in/parthdevalia/)) have responsibility for the communication of results.

## Implementation
{% note info %}
The source code for the web app and scraping scripts have been open-sourced in [this repository](https://github.com/warwickdatascience/higher-or-lower).
{% endnote %}
With 330 million monthly users, Twitter has become an indispensable medium for instant news and opinions from politicians, brands, and of course, celebrities. Manually defining celebrityhood and iterating through matching accounts would be a difficult task, so we decided to look at what existing resources we could take advantage of. We eventually settled on a website called [ProfileRehab](http://profilerehab.com/twitter-help/celebrity_twitter_list). On this site, links to celebrities’ Twitter accounts are sorted into categories. By scraping this information we were able to collect Twitter profile URLs for around five hundred celebrities, matched to their names. We then interfaced with the Twitter API to read their respective follower counts and download their profile pictures. This entire scraping process was performed using Python, to take advantage of the rich ecosystem of web scraping packages the language has.

You may well be asking, “What is an API?”, and so I will take a moment to introduce this term. Application Programming Interfaces (APIs) simply allow applications to communicate with each other and are responsible for much of the connectivity we rely upon. They act as messengers, taking your request, telling the target application what you want to do, and then returning the response. Rather than accessing the application server directly, APIs offer us a dedicated access point, improving security and reliability. A common analogy is that of a restaurant—the API is the waiter, the interface between your table and the kitchen, taking your request and returning the response (the food). 

With regard to our project, we decided to access the data we wanted through an API as Twitter have made recent obfuscations to their website code to make direct scraping more difficult. Use of Twitter’s API, as is often the case, is subject to terms and conditions regarding the usage of the data obtained. Additionally, the company have implemented a rate limit; that is, a maximum number of requests they can handle in a given timespan (just like with a restaurant waiter). Careful examination of these limitations needs to be considered when using an API, but fortunately we found them to be adequate for our needs.

The application is made using Shiny, a package for the R programming language that allows you to build interactive web applications. The framework allows for the development of powerful and flexible web applications with no need for HTML, CSS or JavaScript knowledge. For this reason, Shiny stands out for its unrivalled speed of development. 

Despite its benefits, the raw product of Shiny development is not always the prettiest and can lack strong mobile support. To overcome this, Matthew implemented additional styling using CSS to improve the aesthetics of the final application.

## Takeaways

This project allowed us three WDSS members to work together in creating something that we wouldn’t have done individually. Further, if not for the society, we would not have had the opportunity to work together. This highlights the role of WDSS, bringing people from different backgrounds together to solve challenging problems.

Projects are extremely important in growing your skills and are critical for developing a strong portfolio. Through collaboration, we can see problems from new perspectives, build our professional networks, and gain experience of working in a team. This is in comparison to university work, that is often done alone without using real world data, and usually without a solid final product.

This project leverages infrastructure offered by WDSS, such as our blogging platform and Shiny server. For this reason, alongside the support 
offered by experienced students, working with WDSS to complete research makes it easier to get projects off the ground and showcase what you can do.

Thank you for reading and we hope you enjoy playing our implementation of Higher or Lower.
